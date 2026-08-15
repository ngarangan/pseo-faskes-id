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

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

FASKES_DIR = os.path.join(
    DATA_DIR,
    "faskes"
)

PROGRESS_FILE = os.path.join(
    DATA_DIR,
    "scraper-progress.json"
)

MASTER_FILE = os.path.join(
    DATA_DIR,
    "database_faskes.json"
)

# Maksimal kabupaten/kota setiap GitHub Actions
MAX_AREAS_PER_RUN = 20

# Timeout per request
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
# 38 PROVINSI INDONESIA
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
# PREPARE DIRECTORY
# ============================================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

os.makedirs(
    FASKES_DIR,
    exist_ok=True
)


# ============================================================
# HELPER
# ============================================================

def province_file(code):

    return os.path.join(
        FASKES_DIR,
        f"{code.lower()}.json"
    )


def load_json(path, default):

    if not os.path.exists(path):
        return default

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        print(
            f"âš ï¸ Gagal membaca {path}: {e}"
        )

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

    os.replace(
        temp,
        path
    )


# ============================================================
# PROGRESS
# ============================================================

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
        datetime.utcnow().isoformat()
        + "Z"
    )

    atomic_save_json(
        PROGRESS_FILE,
        progress
    )


# ============================================================
# REPORT / DATA QUALITY
# ============================================================

REPORT_FILE = os.path.join(
    DATA_DIR,
    "scraper-report.json"
)


def build_report(progress):
    """
    Membuat laporan coverage dan kualitas database.
    Tidak mengubah data scraper.
    """

    database = load_json(MASTER_FILE, [])

    if not isinstance(database, list):
        database = []

    total_provinces = len(PROVINCES)

    completed_provinces = min(
        int(progress.get("province_index", 0)),
        total_provinces
    )

    total_areas = 0
    completed_areas = 0
    province_stats = []

    areas_state = progress.get("areas", {})

    for code, province_name in PROVINCES:

        state = areas_state.get(code, {})
        area_list = state.get("list", []) or []
        completed = state.get("completed", []) or []

        total = len(area_list)
        done = len(set(str(x) for x in completed))

        total_areas += total
        completed_areas += min(done, total)

        province_file_data = load_province_data(code)

        if not isinstance(province_file_data, list):
            province_file_data = []

        province_stats.append({
            "code": code,
            "name": province_name,
            "areas": {
                "completed": min(done, total),
                "total": total,
                "complete": total > 0 and done >= total
            },
            "facilities": len(province_file_data)
        })

    def non_empty(item, field):
        value = item.get(field)
        return value not in (None, "", [], {})

    total = len(database)

    hospitals = sum(
        1 for x in database
        if x.get("tipe") == "Rumah Sakit"
    )

    clinics = sum(
        1 for x in database
        if x.get("tipe") == "Klinik"
    )

    doctors = sum(
        1 for x in database
        if x.get("tipe") == "Praktek Dokter"
    )

    coordinates = sum(
        1 for x in database
        if x.get("latitude") is not None
        and x.get("longitude") is not None
    )

    addresses = sum(
        1 for x in database
        if non_empty(x, "alamat")
    )

    phones = sum(
        1 for x in database
        if non_empty(x, "telepon")
    )

    websites = sum(
        1 for x in database
        if non_empty(x, "website")
    )

    names = sum(
        1 for x in database
        if non_empty(x, "nama")
    )

    ids = [
        str(x.get("id"))
        for x in database
        if x.get("id")
    ]

    duplicate_ids = len(ids) - len(set(ids))

    coverage_complete = (
        completed_provinces >= total_provinces
        and total_areas > 0
        and completed_areas >= total_areas
    )

    report = {
        "status": (
            "completed"
            if coverage_complete
            else "running"
        ),

        "updated_at": (
            datetime.utcnow().isoformat()
            + "Z"
        ),

        "coverage": {
            "provinces_completed": completed_provinces,
            "provinces_total": total_provinces,
            "provinces_percent": round(
                completed_provinces / total_provinces * 100,
                2
            ) if total_provinces else 0,

            "areas_completed": completed_areas,
            "areas_total": total_areas,
            "areas_percent": round(
                completed_areas / total_areas * 100,
                2
            ) if total_areas else 0
        },

        "database": {
            "total_facilities": total,
            "hospitals": hospitals,
            "clinics": clinics,
            "doctors": doctors,
            "other": max(
                0,
                total - hospitals - clinics - doctors
            )
        },

        "quality": {
            "with_name": names,
            "with_coordinates": coordinates,
            "with_address": addresses,
            "with_phone": phones,
            "with_website": websites,
            "duplicate_ids": duplicate_ids
        },

        "province_stats": province_stats
    }

    atomic_save_json(
        REPORT_FILE,
        report
    )

    print()
    print("=" * 60)
    print("ðŸ“Š DATABASE REPORT")
    print("=" * 60)
    print(
        f"ðŸ›ï¸ Provinsi : "
        f"{completed_provinces}/{total_provinces}"
    )
    print(
        f"ðŸ™ï¸ Kab/Kota : "
        f"{completed_areas}/{total_areas}"
    )
    print(
        f"ðŸ¥ Faskes   : "
        f"{total}"
    )
    print(
        f"ðŸ“ Koordinat: "
        f"{coordinates}/{total}"
    )
    print(
        f"ðŸ  Alamat   : "
        f"{addresses}/{total}"
    )
    print(
        f"ðŸ“ž Telepon  : "
        f"{phones}/{total}"
    )
    print(
        f"ðŸŒ Website  : "
        f"{websites}/{total}"
    )
    print(
        f"â™»ï¸ Duplikat : "
        f"{duplicate_ids}"
    )

    if coverage_complete:
        print()
        print("ðŸŽ‰ STATUS: DATABASE INDONESIA SELESAI")
    else:
        print()
        print("â³ STATUS: MASIH BERJALAN")

    print(
        f"ðŸ’¾ Report  : {REPORT_FILE}"
    )
    print("=" * 60)

    return report


# ============================================================
# OVERPASS REQUEST
# ============================================================

def overpass_request(
    query,
    label="query"
):

    for server in OVERPASS_SERVERS:

        print()
        print(
            f"ðŸŒ Overpass: {server}"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"ðŸ”„ {label} | "
                    f"attempt {attempt}/3"
                )

                start = time.time()

                response = requests.post(
                    server,
                    data={
                        "data": query
                    },
                    headers=HEADERS,
                    timeout=REQUEST_TIMEOUT
                )

                elapsed = round(
                    time.time() - start,
                    2
                )

                print(
                    f"â±ï¸ {elapsed}s | "
                    f"HTTP {response.status_code} | "
                    f"{len(response.content)} bytes"
                )

                # SUCCESS

                if response.status_code == 200:

                    try:

                        return response.json()

                    except Exception:

                        print(
                            "âŒ Response bukan JSON."
                        )

                        print(
                            response.text[:1000]
                        )

                # BUSY / RATE LIMIT / GATEWAY

                if response.status_code in (
                    429,
                    502,
                    503,
                    504
                ):

                    print(
                        "âš ï¸ Overpass sedang sibuk."
                    )

                    time.sleep(
                        5 * attempt
                    )

                    continue

                print(
                    "âŒ HTTP ERROR:",
                    response.status_code
                )

                print(
                    response.text[:1000]
                )

                break

            except requests.exceptions.Timeout:

                print(
                    "â° REQUEST TIMEOUT"
                )

                time.sleep(
                    5 * attempt
                )

            except requests.exceptions.RequestException as e:

                print(
                    "âŒ REQUEST ERROR:",
                    e
                )

                time.sleep(
                    5 * attempt
                )

        print()
        print(
            "âž¡ï¸ Mencoba mirror berikutnya..."
        )

    return None


# ============================================================
# GET KABUPATEN / KOTA
# ============================================================

def get_areas(
    province_code
):

    query = f"""
[out:json][timeout:60];

area
    ["ISO3166-2"="{province_code}"]
    ["admin_level"="4"]
    ->.province;

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

    if result is None:

        return None

    areas = []

    for element in result.get(
        "elements",
        []
    ):

        tags = element.get(
            "tags",
            {}
        )

        osm_id = element.get(
            "id"
        )

        name = tags.get(
            "name"
        )

        if not osm_id or not name:
            continue

        areas.append({

            "osm_id": str(
                osm_id
            ),

            "name": name

        })

    # Deduplicate

    unique = {}

    for area in areas:

        unique[
            area["osm_id"]
        ] = area

    areas = list(
        unique.values()
    )

    areas.sort(
        key=lambda x:
        x["name"].lower()
    )

    print()
    print(
        f"ðŸ“ Ditemukan "
        f"{len(areas)} kab/kota."
    )

    return areas


# ============================================================
# FETCH FASKES
# ============================================================

def fetch_area_faskes(
    area_osm_id
):

    area_id = (
        3600000000
        + int(area_osm_id)
    )

    query = f"""
[out:json][timeout:90];

area({area_id})->.searchArea;

(
    nwr["amenity"="hospital"]
        (area.searchArea);

    nwr["amenity"="clinic"]
        (area.searchArea);

    nwr["amenity"="doctors"]
        (area.searchArea);
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
        result.get(
            "elements",
            []
        )
    )


# ============================================================
# PARSE FASKES
# ============================================================

def parse_faskes(
    elements
):

    result = {}

    for element in elements:

        tags = element.get(
            "tags",
            {}
        )

        nama = tags.get(
            "name"
        )

        if not nama:
            continue

        osm_type = element.get(
            "type",
            ""
        )

        osm_id = element.get(
            "id"
        )

        if not osm_id:
            continue

        # Coordinates

        if osm_type == "node":

            latitude = element.get(
                "lat"
            )

            longitude = element.get(
                "lon"
            )

        else:

            center = element.get(
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

            "id":
                f"osm-{osm_type}-{osm_id}",

            "nama":
                nama,

            "tipe":
                tipe,

            "kota":
                (
                    tags.get("addr:city")
                    or tags.get("addr:town")
                    or tags.get("addr:municipality")
                    or tags.get("addr:district")
                    or ""
                ),

            "kecamatan":
                (
                    tags.get("addr:subdistrict")
                    or tags.get("addr:district")
                    or ""
                ),

            "provinsi":
                (
                    tags.get("addr:state")
                    or tags.get("addr:province")
                    or ""
                ),

            "alamat":
                (
                    tags.get("addr:full")
                    or tags.get("addr:street")
                    or tags.get("addr:place")
                    or ""
                ),

            "telepon":
                (
                    tags.get("phone")
                    or tags.get("contact:phone")
                    or ""
                ),

            "website":
                (
                    tags.get("website")
                    or tags.get("contact:website")
                    or ""
                ),

            "latitude":
                latitude,

            "longitude":
                longitude,

            "osm_type":
                osm_type,

            "osm_id":
                osm_id
        }

        result[
            item["id"]
        ] = item

    return list(
        result.values()
    )


# ============================================================
# LOAD PROVINCE DATA
# ============================================================

def load_province_data(
    code
):

    path = province_file(
        code
    )

    data = load_json(
        path,
        []
    )

    if not isinstance(
        data,
        list
    ):

        print(
            "âš ï¸ Format province JSON "
            "bukan list. Reset."
        )

        data = []

    # IMPORTANT:
    # Selalu return LIST.
    # Merge dilakukan di main() menggunakan dictionary.

    return data


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
        f"ðŸ’¾ File: {path}"
    )

    print(
        f"ðŸ“Š Data provinsi: "
        f"{len(data)}"
    )


# ============================================================
# REBUILD MASTER DATABASE
# ============================================================

def rebuild_master():

    print()
    print(
        "ðŸ”¨ Rebuilding database_faskes.json..."
    )

    database = {}

    for code, province_name in PROVINCES:

        path = province_file(
            code
        )

        if not os.path.exists(
            path
        ):

            continue

        data = load_json(
            path,
            []
        )

        if not isinstance(
            data,
            list
        ):

            continue

        for item in data:

            key = item.get(
                "id"
            )

            if key:

                database[
                    key
                ] = item

    final_data = list(
        database.values()
    )

    final_data.sort(
        key=lambda x: (
            x.get(
                "provinsi",
                ""
            ),

            x.get(
                "kota",
                ""
            ),

            x.get(
                "nama",
                ""
            )
        )
    )

    atomic_save_json(
        MASTER_FILE,
        final_data
    )

    print()
    print(
        f"ðŸ“Š Total database: "
        f"{len(final_data)}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        "=" * 60
    )

    print(
        "ðŸ‡®ðŸ‡© CARI FASKES ID"
    )

    print(
        "INCREMENTAL SCRAPER"
    )

    print(
        "=" * 60
    )

    progress = load_progress()

    province_index = progress.get(
        "province_index",
        0
    )

    # --------------------------------------------------------
    # ALL PROVINCES DONE
    # --------------------------------------------------------

    if province_index >= len(
        PROVINCES
    ):

        print()
        print(
            "ðŸŽ‰ Semua provinsi sudah selesai."
        )

        rebuild_master()
        build_report(progress)

        return

    # --------------------------------------------------------
    # CURRENT PROVINCE
    # --------------------------------------------------------

    province_code, province_name = (
        PROVINCES[
            province_index
        ]
    )

    print()
    print(
        f"ðŸ“ Provinsi: "
        f"{province_name}"
    )

    print(
        f"ðŸ“Š Progress provinsi: "
        f"{province_index + 1}/"
        f"{len(PROVINCES)}"
    )

    # --------------------------------------------------------
    # LOAD PROVINCE STATE
    # --------------------------------------------------------

    province_state = (
        progress
        .setdefault(
            "areas",
            {}
        )
        .setdefault(
            province_code,
            {}
        )
    )

    # --------------------------------------------------------
    # GET AREA LIST
    # --------------------------------------------------------

    areas = province_state.get(
        "list"
    )

    if areas is None:

        print()
        print(
            "ðŸ“¡ Mengambil daftar "
            "kabupaten/kota..."
        )

        areas = get_areas(
            province_code
        )

        if areas is None:

            print(
                "âŒ Gagal mendapatkan "
                "daftar kab/kota."
            )

            save_progress(
                progress
            )

            sys.exit(1)

        province_state[
            "list"
        ] = areas

        province_state[
            "index"
        ] = 0

        province_state[
            "completed"
        ] = []

        save_progress(
            progress
        )

    # --------------------------------------------------------
    # CURRENT AREA INDEX
    # --------------------------------------------------------

    area_index = province_state.get(
        "index",
        0
    )

    completed = province_state.get(
        "completed",
        []
    )

    # --------------------------------------------------------
    # PROVINCE FINISHED
    # --------------------------------------------------------

    if area_index >= len(
        areas
    ):

        print()
        print(
            f"ðŸŽ‰ {province_name} selesai."
        )

        progress[
            "province_index"
        ] = province_index + 1

        save_progress(
            progress
        )

        rebuild_master()

        return

    # --------------------------------------------------------
    # LOAD EXISTING PROVINCE DATA
    # --------------------------------------------------------

    province_data = load_province_data(
        province_code
    )

    # --------------------------------------------------------
    # CONVERT LIST -> DICT
    #
    # Ini yang memperbaiki error:
    #
    # TypeError:
    # list indices must be integers...
    # --------------------------------------------------------

    province_data_dict = {}

    for item in province_data:

        if not isinstance(
            item,
            dict
        ):

            continue

        item_id = item.get(
            "id"
        )

        if item_id:

            province_data_dict[
                item_id
            ] = item

    # --------------------------------------------------------
    # PROCESS BATCH
    # --------------------------------------------------------

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
        print(
            "-" * 60
        )

        print(
            f"ðŸ™ï¸ {area_name}"
        )

        print(
            f"ðŸ“Œ Area: "
            f"{area_index + 1}/"
            f"{len(areas)}"
        )

        # ----------------------------------------------------
        # ALREADY COMPLETED
        # ----------------------------------------------------

        if area_id in completed:

            print(
                "â­ï¸ Sudah selesai. Skip."
            )

            area_index += 1

            processed += 1

            continue

        # ----------------------------------------------------
        # FETCH
        # ----------------------------------------------------

        data = fetch_area_faskes(
            area_id
        )

        # ----------------------------------------------------
        # FAILED
        # ----------------------------------------------------

        if data is None:

            print()
            print(
                "âŒ Gagal mengambil area."
            )

            print(
                "ðŸ’¾ Progress tetap disimpan."
            )

            province_state[
                "index"
            ] = area_index

            province_state[
                "completed"
            ] = completed

            progress[
                "areas"
            ][province_code] = (
                province_state
            )

            save_progress(
                progress
            )

            rebuild_master()
            build_report(progress)

            # Jangan lanjut ke area berikutnya
            break

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print()
        print(
            f"âœ… Ditemukan "
            f"{len(data)} faskes"
        )

        # ----------------------------------------------------
        # MERGE
        # ----------------------------------------------------

        for item in data:

            item_id = item.get(
                "id"
            )

            if item_id:

                province_data_dict[
                    item_id
                ] = item

        # ----------------------------------------------------
        # CONVERT DICT -> LIST
        # ----------------------------------------------------

        province_data = list(
            province_data_dict.values()
        )

        # ----------------------------------------------------
        # SAVE IMMEDIATELY
        # ----------------------------------------------------

        save_province_data(
            province_code,
            province_data
        )

        # ----------------------------------------------------
        # MARK COMPLETED
        # ----------------------------------------------------

        if area_id not in completed:

            completed.append(
                area_id
            )

        area_index += 1

        processed += 1

        province_state[
            "index"
        ] = area_index

        province_state[
            "completed"
        ] = completed

        progress[
            "areas"
        ][province_code] = (
            province_state
        )

        save_progress(
            progress
        )

        print(
            f"ðŸ’¾ Progress: "
            f"{area_index}/"
            f"{len(areas)}"
        )

    # --------------------------------------------------------
    # CHECK PROVINCE COMPLETION
    # --------------------------------------------------------

    if area_index >= len(
        areas
    ):

        print()
        print(
            f"ðŸŽ‰ {province_name} "
            f"SELESAI!"
        )

        progress[
            "province_index"
        ] = province_index + 1

        save_progress(
            progress
        )

    # --------------------------------------------------------
    # REBUILD MASTER
    # --------------------------------------------------------

    rebuild_master()
    build_report(progress)

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print(
        "=" * 60
    )

    print(
        f"âœ… Batch selesai"
    )

    print(
        f"ðŸ“Š Area diproses: "
        f"{processed}"
    )

    print(
        f"ðŸ“ Provinsi: "
        f"{province_name}"
    )

    print(
        f"ðŸ“Œ Posisi berikutnya: "
        f"{area_index + 1}/"
        f"{len(areas)}"
    )

    print(
        f"ðŸ“Š Faskes provinsi: "
        f"{len(province_data)}"
    )

    print(
        "=" * 60
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
