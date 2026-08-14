import requests
import json
import os
import sys
import time

OVERPASS_URL = "https://overpass.private.coffee/api/interpreter"

OUTPUT_FILE = "data/database_faskes.json"

HEADERS = {
    "User-Agent": "CariFaskesID-pSEO-Bot/1.0 (contact: admin@carifaskes.id)",
    "Accept": "application/json"
}


def fetch_faskes():

    print("========================================")
    print("   SCRAPER FASKES INDONESIA")
    print("========================================")
    print()

    query = r"""
    [out:json][timeout:180];

    area["ISO3166-1"="ID"]->.searchArea;

    (
        nwr["amenity"="hospital"](area.searchArea);
        nwr["amenity"="clinic"](area.searchArea);
        nwr["amenity"="doctors"](area.searchArea);
    );

    out center tags;
    """

    print("🌐 Overpass URL:")
    print(OVERPASS_URL)
    print()

    print("📡 Mengirim query ke Overpass...")
    print()

    try:

        start = time.time()

        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers=HEADERS,
            timeout=210
        )

        elapsed = round(time.time() - start, 2)

        print(f"⏱️ Response time: {elapsed} detik")
        print(f"📊 HTTP status: {response.status_code}")
        print(f"📦 Response size: {len(response.content)} bytes")
        print()

        response.raise_for_status()

        # Debug kalau server ternyata mengembalikan HTML/text error
        content_type = response.headers.get("content-type", "")

        print(f"Content-Type: {content_type}")
        print()

        try:
            result = response.json()

        except Exception:

            print("❌ Response bukan JSON!")
            print()
            print("Response awal:")
            print(response.text[:2000])

            return []

        elements = result.get("elements", [])

        print(f"✅ API berhasil.")
        print(f"📍 Total element: {len(elements)}")
        print()

        data_faskes = []

        for el in elements:

            tags = el.get("tags", {})

            nama = tags.get("name")

            if not nama:
                continue

            osm_type = el.get("type", "")
            osm_id = el.get("id", "")

            # Koordinat
            if osm_type == "node":

                lat = el.get("lat")
                lon = el.get("lon")

            else:

                center = el.get("center", {})

                lat = center.get("lat")
                lon = center.get("lon")

            # Kota
            kota = (
                tags.get("addr:city")
                or tags.get("addr:town")
                or tags.get("addr:municipality")
                or tags.get("addr:district")
                or tags.get("addr:subdistrict")
                or tags.get("is_in:city")
                or tags.get("is_in:town")
                or tags.get("is_in:district")
                or "Indonesia"
            )

            # Provinsi
            provinsi = (
                tags.get("addr:state")
                or tags.get("addr:province")
                or tags.get("is_in:state")
                or tags.get("is_in:province")
                or ""
            )

            # Alamat
            alamat = (
                tags.get("addr:full")
                or tags.get("addr:street")
                or tags.get("addr:place")
                or ""
            )

            # Nomor telepon
            telepon = (
                tags.get("phone")
                or tags.get("contact:phone")
                or ""
            )

            # Website
            website = (
                tags.get("website")
                or tags.get("contact:website")
                or ""
            )

            tipe_raw = tags.get("amenity", "faskes")

            if tipe_raw == "hospital":
                tipe = "Rumah Sakit"

            elif tipe_raw == "clinic":
                tipe = "Klinik"

            elif tipe_raw == "doctors":
                tipe = "Praktek Dokter"

            else:
                tipe = "Fasilitas Kesehatan"

            data_faskes.append({

                "id": f"osm-{osm_type}-{osm_id}",

                "nama": nama,

                "tipe": tipe,

                "kota": kota,

                "provinsi": provinsi,

                "alamat": alamat,

                "telepon": telepon,

                "website": website,

                "latitude": lat,

                "longitude": lon,

                "osm_type": osm_type,

                "osm_id": osm_id

            })

        return data_faskes

    except requests.exceptions.Timeout:

        print("❌ REQUEST TIMEOUT")
        print("Server Overpass terlalu lama merespons.")

        return []

    except requests.exceptions.HTTPError as e:

        print("❌ HTTP ERROR")
        print(e)

        print()
        print("Response:")
        print(response.text[:3000])

        return []

    except requests.exceptions.RequestException as e:

        print("❌ REQUEST ERROR")
        print(e)

        return []

    except Exception as e:

        print("❌ ERROR TIDAK TERDUGA")
        print(type(e).__name__)
        print(e)

        return []


def save_json(data):

    print()
    print("💾 Menyimpan JSON...")

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    try:

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

        print()
        print("========================================")
        print("✅ SELESAI")
        print("========================================")
        print(f"📁 File : {OUTPUT_FILE}")
        print(f"📊 Data : {len(data)}")
        print()

        return True

    except Exception as e:

        print("❌ GAGAL MENULIS JSON")
        print(type(e).__name__)
        print(e)

        return False


def main():

    data = fetch_faskes()

    if not data:

        print()
        print("⚠️ Tidak ada data yang diperoleh.")
        print("❌ JSON TIDAK akan ditimpa.")
        print()

        sys.exit(1)

    print()
    print(f"🔎 Data valid: {len(data)}")

    save_json(data)


if __name__ == "__main__":
    main()
