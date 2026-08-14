import requests
import json
import os
import sys

def fetch_faskes_osm():
    print("Mulai mengambil data faskes dari OpenStreetMap...")
    
    # Query Overpass API untuk mencari hospital, clinic, dan doctors di Indonesia
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json][timeout:60];
    area["ISO3166-1"="ID"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      node["amenity"="clinic"](area.searchArea);
      node["amenity"="doctors"](area.searchArea);
      way["amenity"="hospital"](area.searchArea);
      way["amenity"="clinic"](area.searchArea);
    );
    out center 500;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=90)
        response.raise_for_status()
        result = response.json()
        
        elements = result.get('elements', [])
        print(f"Ditemukan {len(elements)} elemen mentah.")
        
        data_faskes = []
        for idx, el in enumerate(elements):
            tags = el.get('tags', {})
            nama = tags.get('name')
            if not nama:
                continue
                
            kota = tags.get('addr:city') or tags.get('addr:district') or tags.get('is_in:municipality') or 'Indonesia'
            alamat = tags.get('addr:street') or tags.get('addr:full') or 'Alamat tidak tertera'
            tipe_raw = tags.get('amenity', 'faskes')
            
            tipe = "Rumah Sakit" if tipe_raw == "hospital" else ("Klinik" if tipe_raw == "clinic" else "Fasilitas Kesehatan")
            
            data_faskes.append({
                "id": f"faskes-{idx+1}",
                "nama": nama,
                "tipe": tipe,
                "kota": kota,
                "alamat": alamat
            })
            
        return data_faskes

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    data = fetch_faskes_osm()
    
    if data and len(data) > 0:
        os.makedirs('data', exist_ok=True)
        path = 'data/database_faskes.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Berhasil! {len(data)} data faskes disimpan ke {path}.")
    else:
        print("Gagal mengambil data atau data kosong.")
        sys.exit(1)

if __name__ == "__main__":
    main()
