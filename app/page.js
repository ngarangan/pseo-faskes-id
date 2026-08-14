import faskesData from '../data/database_faskes.json';

export default function Home() {
  // Menghitung estimasi total faskes yang terkumpul
  const totalFaskes = faskesData ? faskesData.length : 0;

  return (
    
      
        🏥 CariFaskes.id
        Direktori Fasilitas Kesehatan Terlengkap di Indonesia
      

      
        Status Otomatisasi pSEO
        ✅ Database terhubung secara otomatis dari GitHub Actions.
        📊 Total Fasilitas Kesehatan Terdata: {totalFaskes.toLocaleString('id-ID')} faskes
      

      
        © 2026 CariFaskes.id — Powered by OpenStreetMap & Next.js
      
    
  );
}
