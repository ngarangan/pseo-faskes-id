import requests
import json
import os

def fetch_faskes_osm():
    print("Mencoba mengambil data faskes dari OpenStreetMap Mirror...")
    
    # Menggunakan server mirror Kumi.systems yang lebih stabil untuk GitHub Actions
    overpass_url = "https://overpass.kumi.systems/api/interpreter"
    
    # Query difokuskan ke fasilitas kesehatan di Indonesia
    overpass_query = """
    [out:json][timeout:30];
    area["ISO3166-1"="ID"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      node["amenity"="clinic"](area.searchArea);
      node["amenity"="pharmacy"](area.searchArea);
    );
    out center 200;
    """
    
    headers = {
        'User-Agent': 'CariFaskesID-pSEO-Scraper/1.0 (contact: admin@carifaskes.id)'
    }
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, headers=headers, timeout=35)
        response.raise_for_status()
        result = response.json()
        
        elements = result.get('elements', [])
        print(f"Berhasil terhubung! Ditemukan {len(elements)} data faskes asli dari OSM.")
        
        data_faskes = []
        for idx, el in enumerate(elements):
            tags = el.get('tags', {})
            nama = tags.get('name')
            if not nama:
                continue
                
            kota = tags.get('addr:city') or tags.get('addr:district') or tags.get('is_in:municipality') or 'Indonesia'
            alamat = tags.get('addr:street') or tags.get('addr:full') or 'Alamat tidak tertera'
            tipe_raw = tags.get('amenity', 'faskes')
            
            tipe = "Rumah Sakit" if tipe_raw == "hospital" else ("Klinik" if tipe_raw == "clinic" else "Apotek/Farmasi")
            
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
            print("Data OSM kosong, mempertahankan data sampel.")
            return get_fallback_data()

    except Exception as e:
        print(f"Peringatan: Gagal koneksi ke OSM ({e}). Memakai data fallback.")
        return get_fallback_data()

def get_fallback_data():
    return [
        {"id": "faskes-1", "nama": "RSUD Dokter Soedarso", "tipe": "Rumah Sakit", "kota": "Kota Pontianak", "alamat": "Jl. Kom Yos Sudarso, Pontianak"},
        {"id": "faskes-2", "nama": "RSUD Sambas", "tipe": "Rumah Sakit", "kota": "Kabupaten Sambas", "alamat": "Jl. Siami, Tumuk Manggis, Kec. Sambas"},
        {"id": "faskes-3", "nama": "Puskesmas Sambas", "tipe": "Puskesmas", "kota": "Kabupaten Sambas", "alamat": "Jl. Pembangunan, Kec. Sambas"},
        {"id": "faskes-4", "nama": "Puskesmas Tebas", "tipe": "Puskesmas", "kota": "Kabupaten Sambas", "alamat": "Jl. Raya Tebas, Kec. Tebas"}
    ]

def main():
    data = fetch_faskes_osm()
    
    os.makedirs('data', exist_ok=True)
    path = 'data/database_faskes.json'
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Selesai! {len(data)} data faskes berhasil disimpan ke {path}.")

if __name__ == "__main__":
    main()
