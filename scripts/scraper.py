```python
import requests
import json
import os
import sys
import time
import re
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
FASKES_DIR = os.path.join(DATA_DIR, "faskes")

PROGRESS_FILE = os.path.join(DATA_DIR, "scraper-progress.json")
MASTER_FILE = os.path.join(DATA_DIR, "database_faskes.json")

# Jumlah kabupaten/kota yang diproses setiap GitHub Action
MAX_AREAS_PER_RUN = 5

REQUEST_TIMEOUT = 120

HEADERS = {
    "User-Agent": (
        "CariFaskesID-pSEO-Bot/1.0 "
        "(contact: admin@carifaskes.id)"
    ),
    "Accept": "application/json"
}


# ============================================================
# OVERPASS MIRRORS
# ============================================================

OVERPASS_SERVERS = [
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]


# ============================================================
# 38 PROVINCES
# ISO 3166-2 Indonesia
# ============================================================

PROVINCES = [
    ("ID-AC", "Aceh"),
    ("ID-SU", "Sumatera Utara"),
    ("ID-SB", "Sumatera Barat"),
    ("ID-RI", "Riau"),
    ("ID-JA", "Jambi"),
    ("ID-SS", "Sumatera Selatan"),
    ("ID-BE", "Bengkulu"),
    ("ID-LA", "Lampung"),
    ("ID-BB", "Kepulauan Bangka Belitung"),
    ("ID-KR", "Kepulauan Riau"),

    ("ID-JK", "DKI Jakarta"),
    ("ID-JB", "Jawa Barat"),
    ("ID-JT", "Jawa Tengah"),
    ("ID-YO", "DI Yogyakarta"),
    ("ID-JI", "Jawa Timur"),
    ("ID-BT", "Banten"),

    ("ID-BA", "Bali"),
    ("ID-NB", "Nusa Tenggara Barat"),
    ("ID-NT", "Nusa Tenggara Timur"),

    ("ID-KB", "Kalimantan Barat"),
    ("ID-KT", "Kalimantan Tengah"),
    ("ID-KS", "Kalimantan Selatan"),
    ("ID-KI", "Kalimantan Timur"),
    ("ID-KU", "Kalimantan Utara"),

    ("ID-SA", "Sulawesi Utara"),
    ("ID-ST", "Sulawesi Tengah"),
    ("ID-SN", "Sulawesi Selatan"),
    ("ID-SG", "Sulawesi Tenggara"),
    ("ID-GO", "Gorontalo"),
    ("ID-SR", "Sulawesi Barat"),

    ("ID-MA", "Maluku"),
    ("ID-MU", "Maluku Utara"),

    ("ID-PB", "Papua Barat"),
    ("ID-PA", "Papua"),
    ("ID-PE", "Papua Pegunungan"),
    ("ID-PS", "Papua Selatan"),
    ("ID-PT", "Papua Tengah"),
    ("ID-PD", "Papua Barat Daya")
]


# ============================================================
# DIRECTORY
# ============================================================

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FASKES_DIR, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def province_file(code):
    return os.path.join(
        FASKES_DIR,
        f"{code.lower()}.json"
    )


def load_json(path, default):
    if not os.path.exists(path):
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def atomic_save_json(path, data):

    temp = path + ".tmp"

    with open(
        temp,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    os.replace(temp, path)


def load_progress():

    default = {
        "province_index": 0,
        "areas": {},
        "last_run": None
    }

    return load_json(
        PROGRESS_FILE,
        default
    )


def save_progress(progress):

    progress["last_run"] = (
        datetime.utcnow().isoformat() + "Z"
    )

    atomic_save_json(
        PROGRESS_FILE,
        progress
    )


# ============================================================
# OVERPASS REQUEST
# ============================================================

def overpass_request(query, label="query"):

    for server in OVERPASS_SERVERS:

        print()
        print(f"🌐 Overpass: {server}")

        for attempt in range(1, 4):

            try:

                print(
                    f"🔄 {label} | "
                    f"attempt {attempt}/3"
                )

                start = time.time()

                response = requests.post(
                    server,
                    data={"data": query},
                    headers=HEADERS,
                    timeout=REQUEST_TIMEOUT
                )

                elapsed = round(
                    time.time() - start,
                    2
                )

                print(
                    f"⏱️ {elapsed}s | "
                    f"HTTP {response.status_code} | "
                    f"{len(response.content)} bytes"
                )

                if response.status_code == 200:

                    try:

                        return response.json()

                    except Exception:

                        print(
                            "❌ Response bukan JSON."
                        )

                if response.status_code in (
                    429,
                    502,
                    503,
                    504
                ):

                    print(
                        "⚠️ Overpass sedang sibuk."
                    )

                    time.sleep(
                        5 * attempt
                    )

                    continue

                print(
                    "❌ HTTP error:",
                    response.status_code
                )

                print(
                    response.text[:500]
                )

                break

            except requests.exceptions.Timeout:

                print(
                    "⏰ Timeout."
                )

                time.sleep(
                    5 * attempt
                )

            except requests.exceptions.RequestException as e:

                print(
                    "❌ Request error:",
                    e
                )

                time.sleep(
                    5 * attempt
                )

        print(
            "➡️ Mencoba mirror berikutnya..."
        )

    return None


# ============================================================
# GET KABUPATEN / KOTA
# ============================================================

def get_areas(province_code):

    query = f"""
[out:json][timeout:60];

area["ISO3166-2"="{province_code}"][admin_level=4]->.province;

rel
    ["boundary"="administrative"]
    ["admin_level"="5"]
    (area.province);

out tags;
"""

    result = overpass_request(
        query,
        f"ambil kab/kota {province_code}"
    )

    if not result:
        return None

    areas = []

    for el in result.get("elements", []):

        tags = el.get("tags", {})

        osm_id = el.get("id")
        name = tags.get("name")

        if not osm_id or not name:
            continue

        areas.append({
            "osm_id": osm_id,
            "name": name
        })

    # Deduplicate
    unique = {}

    for area in areas:
        unique[area["osm_id"]] = area

    areas = list(
        unique.values()
    )

    areas.sort(
        key=lambda x: x["name"].lower()
    )

    print()
    print(
        f"📍 Ditemukan {len(areas)} kab/kota."
    )

    return areas


# ============================================================
# FETCH FASKES FROM ONE KAB/KOTA
# ============================================================

def fetch_area_faskes(area_osm_id):

    # Area ID dari relation OSM:
    # 3600000000 + relation id

    area_id = (
        3600000000 + int(area_osm_id)
    )

    query = f"""
[out:json][timeout:90];

area({area_id})->.searchArea;

(
    nwr["amenity"="hospital"](area.searchArea);
    nwr["amenity"="clinic"](area.searchArea);
    nwr["amenity"="doctors"](area.searchArea);
);

out center tags;
"""

    result = overpass_request(
        query,
        f"faskes area {area_osm_id}"
    )

    if result is None:
        return None

    return parse_faskes(
        result.get("elements", [])
    )


# ============================================================
# PARSE FASKES
# ============================================================

def parse_faskes(elements):

    result = {}

    for el in elements:

        tags = el.get(
            "tags",
            {}
        )

        nama = tags.get(
            "name"
        )

        if not nama:
            continue

        osm_type = el.get(
            "type",
            ""
        )

        osm_id = el.get(
            "id"
        )

        if not osm_id:
            continue

        # Coordinates

        if osm_type == "node":

            latitude = el.get(
                "lat"
            )

            longitude = el.get(
                "lon"
            )

        else:

            center = el.get(
                "center",
                {}
            )

            latitude = center.get(
                "lat"
            )

            longitude = center.get(
                "lon"
            )

        # Type

        amenity = tags.get(
            "amenity",
            "faskes"
        )

        if amenity == "hospital":

            tipe = "Rumah Sakit"

        elif amenity == "clinic":

            tipe = "Klinik"

        elif amenity == "doctors":

            tipe = "Praktek Dokter"

        else:

            tipe = "Fasilitas Kesehatan"

        item = {

            "id": (
                f"osm-{osm_type}-{osm_id}"
            ),

            "nama": nama,

            "tipe": tipe,

            "kota": (
                tags.get("addr:city")
                or tags.get("addr:town")
                or tags.get("addr:municipality")
                or tags.get("addr:district")
                or ""
            ),

            "kecamatan": (
                tags.get("addr:subdistrict")
                or tags.get("addr:district")
                or ""
            ),

            "provinsi": (
                tags.get("addr:state")
                or tags.get("addr:province")
                or ""
            ),

            "alamat": (
                tags.get("addr:full")
                or tags.get("addr:street")
                or tags.get("addr:place")
                or ""
            ),

            "telepon": (
                tags.get("phone")
                or tags.get("contact:phone")
                or ""
            ),

            "website": (
                tags.get("website")
                or tags.get("contact:website")
                or ""
            ),

            "latitude": latitude,

            "longitude": longitude,

            "osm_type": osm_type,

            "osm_id": osm_id

        }

        key = item["id"]

        result[key] = item

    return list(
        result.values()
    )


# ============================================================
# LOAD PROVINCE DATA
# ============================================================

def load_province_data(code):

    path = province_file(
        code
    )

    data = load_json(
        path,
        []
    )

    unique = {}

    for item in data:

        key = item.get(
            "id"
        )

        if key:
            unique[key] = item

    return list(
        unique.values()
    )


# ============================================================
# SAVE PROVINCE DATA
# ============================================================

def save_province_data(
    code,
    data
):

    path = province_file(
        code
    )

    atomic_save_json(
        path,
        data
    )

    print()
    print(
        f"💾 {path}"
    )

    print(
        f"📊 {len(data)} faskes"
    )


# ============================================================
# REBUILD MASTER DATABASE
# ============================================================

def rebuild_master():

    print()
    print(
        "🔨 Rebuilding database_faskes.json..."
    )

    database = {}

    for code, name in PROVINCES:

        path = province_file(
            code
        )

        if not os.path.exists(path):
            continue

        data = load_json(
            path,
            []
        )

        for item in data:

            key = item.get(
                "id"
            )

            if key:

                database[key] = item

    final_data = list(
        database.values()
    )

    final_data.sort(
        key=lambda x: (
            x.get("provinsi", ""),
            x.get("kota", ""),
            x.get("nama", "")
        )
    )

    atomic_save_json(
        MASTER_FILE,
        final_data
    )

    print(
        f"📊 Total master: "
        f"{len(final_data)}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("🇮🇩 CARI FASKES ID - INCREMENTAL SCRAPER")
    print("=" * 60)

    progress = load_progress()

    province_index = progress.get(
        "province_index",
        0
    )

    # --------------------------------------------------------
    # Cari provinsi aktif
    # --------------------------------------------------------

    if province_index >= len(PROVINCES):

        print()
        print(
            "🎉 Semua provinsi selesai."
        )

        rebuild_master()

        return

    province_code, province_name = PROVINCES[
        province_index
    ]

    print()
    print(
        f"📍 Provinsi: "
        f"{province_name}"
    )

    print(
        f"📊 Progress provinsi: "
        f"{province_index + 1}/"
        f"{len(PROVINCES)}"
    )

    # --------------------------------------------------------
    # Area list
    # --------------------------------------------------------

    province_state = progress[
        "areas"
    ].get(
        province_code,
        {}
    )

    areas = province_state.get(
        "list"
    )

    if areas is None:

        print()
        print(
            "📡 Mengambil daftar kab/kota..."
        )

        areas = get_areas(
            province_code
        )

        if areas is None:

            print(
                "❌ Gagal mengambil daftar "
                "kab/kota."
            )

            sys.exit(1)

        province_state = {
            "list": areas,
            "index": 0
        }

        progress[
            "areas"
        ][province_code] = province_state

        save_progress(
            progress
        )

    area_index = province_state.get(
        "index",
        0
    )

    # --------------------------------------------------------
    # Semua area provinsi selesai
    # --------------------------------------------------------

    if area_index >= len(areas):

        print()
        print(
            f"🎉 {province_name} selesai."
        )

        province_index += 1

        progress[
            "province_index"
        ] = province_index

        save_progress(
            progress
        )

        rebuild_master()

        return

    # --------------------------------------------------------
    # Process MAX areas
    # --------------------------------------------------------

    province_data = load_province_data(
        province_code
    )

    processed = 0

    while (
        area_index < len(areas)
        and processed < MAX_AREAS_PER_RUN
    ):

        area = areas[
            area_index
        ]

        area_id = str(
            area["osm_id"]
        )

        area_name = area[
            "name"
        ]

        print()
        print("-" * 60)

        print(
            f"🏙️ {area_name}"
        )

        print(
            f"📌 {area_index + 1}/"
            f"{len(areas)}"
        )

        # ----------------------------------------------------
        # Check if this area was already completed
        # ----------------------------------------------------

        completed = province_state.get(
            "completed",
            []
        )

        if area_id in completed:

            print(
                "⏭️ Sudah selesai, skip."
            )

            area_index += 1
            processed += 1
            continue

        # ----------------------------------------------------
        # Fetch
        # ----------------------------------------------------

        data = fetch_area_faskes(
            area_id
        )

        if data is None:

            print()
            print(
                "⚠️ Area gagal."
            )

            print(
                "➡️ Progress disimpan."
            )

            province_state[
                "index"
            ] = area_index

            progress[
                "areas"
            ][province_code] = province_state

            save_progress(
                progress
            )

            # Jangan exit error setelah ada progress.
            # GitHub tetap harus commit progress/data.

            break

        print(
            f"✅ Ditemukan "
            f"{len(data)} faskes"
        )

        # ----------------------------------------------------
        # Merge
        # ----------------------------------------------------

        for item in data:

            province_data[
                item["id"]
            ] = item

        # ----------------------------------------------------
        # SAVE AFTER EVERY AREA
        # ----------------------------------------------------

        province_data_list = list(
            province_data.values()
        )

        save_province_data(
            province_code,
            province_data_list
        )

        # ----------------------------------------------------
        # Mark completed
        # ----------------------------------------------------

        completed = province_state.setdefault(
            "completed",
            []
        )

        if area_id not in completed:

            completed.append(
                area_id
            )

        area_index += 1

        province_state[
            "index"
        ] = area_index

        progress[
            "areas"
        ][province_code] = province_state

        save_progress(
            progress
        )

        processed += 1

    # --------------------------------------------------------
    # Province finished after batch
    # --------------------------------------------------------

    if area_index >= len(areas):

        print()
        print(
            f"🎉 {province_name} "
            f"SELESAI!"
        )

        progress[
            "province_index"
        ] = province_index + 1

        save_progress(
            progress
        )

    # --------------------------------------------------------
    # Rebuild master
    # --------------------------------------------------------

    rebuild_master()

    print()
    print("=" * 60)

    print(
        f"✅ Batch selesai: "
        f"{processed} area"
    )

    print(
        f"📍 Provinsi: "
        f"{province_name}"
    )

    print(
        f"📊 Area berikutnya: "
        f"{area_index + 1}/"
        f"{len(areas)}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
```
