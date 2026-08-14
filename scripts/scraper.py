import requests
import json
import os

def fetch_data():
    print("Mulai mengambil data faskes dari Overpass API...")
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Query mengambil data Klinik & Puskesmas di Indonesia
    query = """
    [out:json][timeout:90];
    area["ISO3166-1"="ID"]->.searchArea;
    (
      node["amenity"="clinic"](area.searchArea);
      node["healthcare"="hospital"](area.searchArea);
    );
    out body;
    """
    
    try:
        response = requests.get(overpass_url, params={'data': query})
        data = response.json()
        elements = data.get('elements', [])
        print(f"Berhasil mengunduh {len(elements)} data fasilitas kesehatan!")
        
        # Buat folder 'data' jika belum ada
        os.makedirs('data', exist_ok=True)
        
        # Simpan hasil ke data/database_faskes.json
        with open('data/database_faskes.json', 'w', encoding='utf-8') as f:
            json.dump(elements, f, ensure_ascii=False, indent=2)
            
        print("File data/database_faskes.json berhasil disimpan!")

    except Exception as e:
        print(f"Error saat mengambil data: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_data()
