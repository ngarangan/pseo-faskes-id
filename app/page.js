export default function Home() {
  const categories = [
    { name: 'Puskesmas', icon: '🏥', count: '10,000+' },
    { name: 'Rumah Sakit', icon: '🩺', count: '3,000+' },
    { name: 'Klinik Pratama', icon: '💊', count: '15,000+' },
    { name: 'Apotek & Farmasi', icon: '💉', count: '20,000+' },
  ];

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8fafc', color: '#0f172a' }}>
      {/* Header / Navbar */}
      <header style={{ borderBottom: '1px solid #e2e8f0', backgroundColor: '#ffffff', padding: '1rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '1.5rem' }}>🛡️</span>
          <span style={{ fontWeight: 'bold', fontSize: '1.25rem', color: '#0284c7' }}>CariFaskes<span style={{ color: '#0f172a' }}>.id</span></span>
        </div>
      </header>

      {/* Hero Section */}
      <section style={{ padding: '3rem 1.5rem 2rem', textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
        <span style={{ backgroundColor: '#e0f2fe', color: '#0369a1', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.875rem', fontWeight: '600' }}>
          Direktori Kesehatan Indonesia
        </span>
        <h1 style={{ fontSize: '2rem', fontWeight: '800', marginTop: '1rem', marginBottom: '0.5rem', lineHeight: '1.2' }}>
          Cari Fasilitas Kesehatan Terdekat & Terlengkap
        </h1>
        <p style={{ color: '#64748b', fontSize: '1rem', marginBottom: '2rem' }}>
          Temukan lokasi, kontak, dan informasi Puskesmas, Rumah Sakit, hingga Klinik di seluruh Indonesia secara cepat.
        </p>

        {/* Search Bar Input */}
        <div style={{ display: 'flex', gap: '0.5rem', maxWidth: '500px', margin: '0 auto' }}>
          <input 
            type="text" 
            placeholder="Ketik nama kota, kecamatan, atau faskes..." 
            style={{ flex: 1, padding: '0.75rem 1rem', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', fontSize: '0.95rem' }}
          />
          <button style={{ backgroundColor: '#0284c7', color: '#fff', border: 'none', padding: '0.75rem 1.25rem', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' }}>
            Cari
          </button>
        </div>
      </section>

      {/* Grid Kategori Faskes */}
      <section style={{ maxWidth: '800px', margin: '2rem auto', padding: '0 1.5rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '1rem' }}>Kategori Fasilitas</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem' }}>
          {categories.map((cat, idx) => (
            <div key={idx} style={{ backgroundColor: '#ffffff', padding: '1.25rem', borderRadius: '12px', border: '1px solid #e2e8f0', textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{cat.icon}</div>
              <h3 style={{ fontSize: '1rem', margin: '0 0 0.25rem 0' }}>{cat.name}</h3>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>{cat.count} lokasi</span>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid #e2e8f0', backgroundColor: '#ffffff', padding: '1.5rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.875rem', marginTop: '4rem' }}>
        <p>© 2026 CariFaskes.id — pSEO Engine for Open Health Data</p>
      </footer>
    </div>
  );
}
