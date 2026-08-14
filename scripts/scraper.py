import requests
import json
import os

def fetch_data():
    """
    Fungsi untuk mengambil data. 
    Ganti URL_TARGET dengan API yang kamu gunakan.
    """
    URL_TARGET = "https://example-api-faskes.com/v1/data" 
    
    try:
        # Menambahkan timeout agar tidak menggantung di GitHub Actions
        response = requests.get(URL_TARGET, timeout=30)
        response.raise_for_status() # Langsung error kalau status bukan 200
        
        raw_data = response.json()
        
        # Proses cleaning/mapping data agar sesuai dengan format frontend
        processed_data = []
        for item in raw_data:
            processed_data.append({
                "id": item.get("id"),
                "nama": item.get("nama_faskes", "Unknown"),
                "tipe": item.get("jenis", "Lainnya"),
                "kota": item.get("kota", "Unknown"),
                "alamat": item.get("alamat", "-")
            })
            
        return processed_data

    except Exception as e:
        print(f"Error saat scraping: {e}")
        return None

def main():
    data = fetch_data()
    
    if data:
        # Simpan ke file
        os.makedirs('data', exist_ok=True)
        with open('data/database_faskes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Sukses! {len(data)} data disimpan.")
    else:
        print("Gagal mengambil data, file tidak diupdate.")
        exit(1) # Penting agar GitHub Actions tau bahwa ini gagal

if __name__ == "__main__":
    main()
