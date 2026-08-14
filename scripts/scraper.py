import requests
import json
import os
import sys

def fetch_faskes_osm():
    print("Mulai mengambil data faskes dari OpenStreetMap...")
    
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query difokuskan ke Kalimantan Barat (agar cepat & anti-timeout)
    overpass_query = """
    [out:json][timeout:30];
    area["ISO3166-2"="ID-KB"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      node["amenity"="clinic"](area.searchArea);
      node["amenity"="pharmacy"](area.searchArea);
      way["amenity"="hospital"](area.searchArea);
    );
    out center 300;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=45)
        response.raise_for_status()
        result = response.json()
        
        elements = result.get('elements', [])
        print(f"Ditemukan {len(elements)} elemen dari OSM.")
        
        data_faskes = []
        for idx, el in enumerate(elements):
            tags = el.get('tags', {})
            nama = tags.get('name')
            if not nama:
                continue
                
            kota = tags.get('addr:city') or tags.get('addr:district') or tags.get('is_in:municipality') or 'Kalimantan Barat'
            alamat = tags.get('addr:street') or tags.get('addr:full') or 'Alamat tidak tertera'
            tipe_raw = tags.get('amenity', 'faskes')
            
            tipe = "Rumah Sakit" if tipe_raw == "hospital" else ("Klinik" if tipe_raw == "clinic" else "Apotek/Farmasi")
            
            data_faskes.append({
                "id": f"faskes-{idx+1}",
                "nama": nama,
                "tipe": tipe,
                "kota": kota,
                "alamat": alamat
            })
            
        return data_faskes

    except Exception as e:
        print(f"Error saat mengambil data dari Overpass API: {e}")
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
        print("Data tidak ditemukan atau request timeout.")
        sys.exit(1)

if __name__ == "__main__":
    main()
