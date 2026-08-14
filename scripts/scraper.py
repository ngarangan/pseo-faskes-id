import requests
import json
import os
import sys

def get_fallback_data():
    """Data cadangan valid agar build tidak pernah gagal jika API publik offline/timeout"""
    return [
        {"id": "faskes-1", "nama": "RSUD Dokter Soedarso", "tipe": "Rumah Sakit", "kota": "Kota Pontianak", "alamat": "Jl. Kom Yos Sudarso, Pontianak"},
        {"id": "faskes-2", "nama": "RSUD Sambas", "tipe": "Rumah Sakit", "kota": "Kabupaten Sambas", "alamat": "Jl. Siami, Tumuk Manggis, Kec. Sambas"},
        {"id": "faskes-3", "nama": "Puskesmas Sambas", "tipe": "Puskesmas", "kota": "Kabupaten Sambas", "alamat": "Jl. Pembangunan, Kec. Sambas"},
        {"id": "faskes-4", "nama": "Puskesmas Tebas", "tipe": "Puskesmas", "kota": "Kabupaten Sambas", "alamat": "Jl. Raya Tebas, Kec. Tebas"},
        {"id": "faskes-5", "nama": "RSUD Abdul Aziz Singkawang", "tipe": "Rumah Sakit", "kota": "Kota Singkawang", "alamat": "Jl. Dr. Sutomo No.28, Singkawang"}
    ]

def fetch_faskes_osm():
    print("Mencoba mengambil data faskes dari OpenStreetMap...")
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    overpass_query = """
    [out:json][timeout:15];
    area["ISO3166-2"="ID-KB"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      node["amenity"="clinic"](area.searchArea);
    );
    out center 100;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=20)
        response.raise_for_status()
        result = response.json()
        
        elements = result.get('elements', [])
        print(f"Berhasil terhubung! Ditemukan {len(elements)} data dari OSM.")
        
        data_faskes = []
        for idx, el in enumerate(elements):
            tags = el.get('tags', {})
            nama = tags.get('name')
            if not nama:
                continue
                
            kota = tags.get('addr:city') or tags.get('addr:district') or 'Kalimantan Barat'
            alamat = tags.get('addr:street') or tags.get('addr:full') or 'Alamat tidak tertera'
            tipe_raw = tags.get('amenity', 'faskes')
            tipe = "Rumah Sakit" if tipe_raw == "hospital" else "Klinik"
            
            data_faskes.append({
                "id": f"faskes-osm-{idx+1}",
                "nama": nama,
                "tipe": tipe,
                "kota": kota,
                "alamat": alamat
            })
            
        if len(data_faskes) > 0:
            return data_faskes
        else:
            print("Pencarian OSM kosong, menggunakan data fallback.")
            return get_fallback_data()

    except Exception as e:
        print(f"Peringatan: Overpass API error/timeout ({e}). Menggunakan data fallback aman.")
        return get_fallback_data()

def main():
    data = fetch_faskes_osm()
    
    os.makedirs('data', exist_ok=True)
    path = 'data/database_faskes.json'
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Selesai! {len(data)} data faskes berhasil disimpan ke {path}.")

if __name__ == "__main__":
    main()
