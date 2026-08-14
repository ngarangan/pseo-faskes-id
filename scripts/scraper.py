import requests
import json
import os
import time

def fetch_all_indonesia():
    print("Mulai mengambil data faskes seluruh Indonesia...")
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Daftar Kode ISO 3166-2 Provinsi di Indonesia
    provinsi_list = [
        {"kode": "ID-JK", "nama": "DKI Jakarta"},
        {"kode": "ID-JB", "nama": "Jawa Barat"},
        {"kode": "ID-JT", "nama": "Jawa Tengah"},
        {"kode": "ID-JI", "nama": "Jawa Timur"},
        {"kode": "ID-BT", "nama": "Banten"},
        {"kode": "ID-YO", "nama": "DI Yogyakarta"},
        {"kode": "ID-BA", "nama": "Bali"},
        {"kode": "ID-SU", "nama": "Sumatera Utara"},
        {"kode": "ID-SB", "nama": "Sumatera Barat"},
        {"kode": "ID-RI", "nama": "Riau"},
        {"kode": "ID-KR", "nama": "Kepulauan Riau"},
        {"kode": "ID-JA", "nama": "Jambi"},
        {"kode": "ID-SS", "nama": "Sumatera Selatan"},
        {"kode": "ID-BB", "nama": "Bangka Belitung"},
        {"kode": "ID-BE", "nama": "Bengkulu"},
        {"kode": "ID-LA", "nama": "Lampung"},
        {"kode": "ID-AC", "nama": "Aceh"},
        {"kode": "ID-KB", "nama": "Kalimantan Barat"},
        {"kode": "ID-KT", "nama": "Kalimantan Tengah"},
        {"kode": "ID-KS", "nama": "Kalimantan Selatan"},
        {"kode": "ID-KI", "nama": "Kalimantan Timur"},
        {"kode": "ID-KU", "nama": "Kalimantan Utara"},
        {"kode": "ID-SA", "nama": "Sulawesi Utara"},
        {"kode": "ID-ST", "nama": "Sulawesi Tengah"},
        {"kode": "ID-SG", "nama": "Sulawesi Tenggara"},
        {"kode": "ID-SR", "nama": "Sulawesi Barat"},
        {"kode": "ID-SN", "nama": "Sulawesi Selatan"},
        {"kode": "ID-GO", "nama": "Gorontalo"},
        {"kode": "ID-NB", "nama": "Nusa Tenggara Barat"},
        {"kode": "ID-NT", "nama": "Nusa Tenggara Timur"},
        {"kode": "ID-MA", "nama": "Maluku"},
        {"kode": "ID-MU", "nama": "Maluku Utara"},
        {"kode": "ID-PA", "nama": "Papua"},
        {"kode": "ID-PB", "nama": "Papua Barat"},
    ]
    
    all_elements = []

    for prov in provinsi_list:
        print(f"Sedang mengunduh data: {prov['nama']} ({prov['kode']})...")
        
        query = f"""
        [out:json][timeout:60];
        area["ISO3166-2"="{prov['kode']}"]->.searchArea;
        (
          node["amenity"="clinic"](area.searchArea);
          node["healthcare"="hospital"](area.searchArea);
        );
        out body;
        """
        
        try:
            response = requests.get(overpass_url, params={'data': query}, timeout=60)
            if response.status_code == 200:
                data = response.json()
                elements = data.get('elements', [])
                print(f"  -> Ditemukan {len(elements)} data.")
                all_elements.extend(elements)
            else:
                print(f"  -> Gagal/Timeout di {prov['nama']}, dilewati.")
        except Exception as e:
            print(f"  -> Error pada {prov['nama']}: {e}")
            
        # Jeda 2 detik per provinsi agar tidak membebani server Overpass
        time.sleep(2)

    print(f"\nTOTAL DATA TERKUMPUL: {len(all_elements)} faskes se-Indonesia!")
    
    # Simpan hasil gabungan ke data/database_faskes.json
    os.makedirs('data', exist_ok=True)
    with open('data/database_faskes.json', 'w', encoding='utf-8') as f:
        json.dump(all_elements, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_all_indonesia()
