import requests
import json
import os
import sys

def fetch_faskes_from_overpass():
    print("🌐 Menghubungkan ke OpenStreetMap Overpass API...")
    
    # Mirror Overpass API yang sangat stabil & cepat
    overpass_url = "https://overpass.kumi.systems/api/interpreter"
    
    # Query OSM: Mengambil Rumah Sakit, Klinik, & Puskesmas di Indonesia (dibatasi 300 data teratas)
    overpass_query = """
    [out:json][timeout:60];
    area["ISO3166-1"="ID"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      node["amenity"="clinic"](area.searchArea);
      node["amenity"="doctors"](area.searchArea);
      way["amenity"="hospital"](area.searchArea);
    );
    out center 300;
    """
    
    # Header Wajib agar tidak di-block oleh OSM
    headers = {
        'User-Agent': 'CariFaskesID-pSEO-Bot/1.0 (contact: admin@carifaskes.id)'
    }
    
    try:
        response = requests.post(
            overpass_url, 
            data={'data': overpass_query}, 
            headers=headers, 
            timeout=45
        )
        response.raise_for_status()
        result = response.json()
        
        elements = result.get('elements', [])
        print(f"📡 Berhasil! Ditemukan {len(elements)} data faskes mentah dari API.")
        
        data_faskes = []
        for idx, el in enumerate(elements):
            tags = el.get('tags', {})
            nama = tags.get('name')
            
            # Abaikan jika tidak ada nama faskes
            if not nama:
                continue
                
            kota = (
                tags.get('addr:city') or 
                tags.get('addr:district') or 
                tags.get('is_in:municipality') or 
                tags.get('is_in:province') or 
                'Indonesia'
            )
            alamat = (
                tags.get('addr:street') or 
                tags.get('addr:full') or 
                'Alamat tidak tertera'
            )
            tipe_raw = tags.get('amenity', 'faskes')
            
            # Mapping jenis faskes
            if tipe_raw == "hospital":
                tipe = "Rumah Sakit"
            elif tipe_raw == "clinic":
                tipe = "Klinik"
            elif tipe_raw == "doctors":
                tipe = "Praktek Dokter"
            else:
                tipe = "Fasilitas Kesehatan"
            
            data_faskes.append({
                "id": f"faskes-osm-{idx+1}",
                "nama": nama,
                "tipe": tipe,
                "kota": kota,
                "alamat": alamat
            })
            
        return data_faskes

    except Exception as e:
        print(f"❌ Error saat me-request API Overpass: {e}")
        return None

def main():
    data = fetch_faskes_from_overpass()
    
    if data and len(data) > 0:
        os.makedirs('data', exist_ok=True)
        path = 'data/database_faskes.json'
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Selesai! {len(data)} data faskes asli dari API berhasil disimpan ke {path}.")
    else:
        print("⚠️ Gagal mendapatkan data dari API. Pembatalan update.")
        sys.exit(1)

if __name__ == "__main__":
    main()
