'use client';

import { useState } from 'react';
import faskesData from '../data/database_faskes.json';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  // Ambil total data faskes yang ada di JSON
  const totalFaskes = Array.isArray(faskesData) ? faskesData.length : 0;

  const handleSearch = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const searchTerm = query.toLowerCase();
    
    // Cari berdasarkan nama faskes, kota, atau jenis faskes
    const filtered = (faskesData || []).filter((item) => {
      const nameMatch = item.name?.toLowerCase().includes(searchTerm);
      const cityMatch = item.city?.toLowerCase().includes(searchTerm);
      const typeMatch = item.type?.toLowerCase().includes(searchTerm);
      return nameMatch || cityMatch || typeMatch;
    });

    setResults(filtered.slice(0, 20)); // Tampilkan 20 hasil pertama dulu
    setHasSearched(true);
  };

  const categories = [
    { name: 'Puskesmas', icon: '🏥' },
    { name: 'Rumah Sakit', icon: '🩺' },
    { name: 'Klinik Pratama', icon: '💊' },
    { name: 'Apotek & Farmasi', icon: '💉' },
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
      <section style={{ padding: '2.5rem 1.5rem 1.5rem', textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
        <span style={{ backgroundColor: '#e0f2fe', color: '#0369a1', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.875rem', fontWeight: '600' }}>
          Direktori Kesehatan Indonesia
        </span>
        <h1 style={{ fontSize: '1.8rem', fontWeight: '800', marginTop: '1rem', marginBottom: '0.5rem', lineHeight: '1.2' }}>
          Cari Fasilitas Kesehatan Terdekat & Terlengkap
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.95rem', marginBottom: '1.5rem' }}>
          Terdata <strong>{totalFaskes.toLocaleString('id-ID')}</strong> lokasi faskes siap dicari.
        </p>

        {/* Search Bar Input */}
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', maxWidth: '500px', margin: '0 auto' }}>
          <input 
            type="text" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ketik nama kota (ex: Sambas), atau jenis faskes..." 
            style={{ flex: 1, padding: '0.75rem 1rem', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', fontSize: '0.95rem' }}
          />
          <button type="submit" style={{ backgroundColor: '#0284c7', color: '#fff', border: 'none', padding: '0.75rem 1.25rem', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' }}>
            Cari
          </button>
        </form>
      </section>

      {/* Hasil Pencarian */}
      {hasSearched && (
        <section style={{ maxWidth: '800px', margin: '0 auto 2rem', padding: '0 1.5rem' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem' }}>
            Hasil Pencarian untuk "{query}" ({results.length} ditemukan)
          </h2>
          
          {results.length === 0 ? (
            <p style={{ color: '#64748b', textAlign: 'center', padding: '2rem', backgroundColor: '#fff', borderRadius: '8px' }}>
              Tidak ada fasilitas kesehatan yang cocok dengan kata kunci tersebut.
            </p>
          ) : (
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              {results.map((item, idx) => (
                <div key={idx} style={{ backgroundColor: '#ffffff', padding: '1rem 1.25rem', borderRadius: '10px', border: '1px solid #e2e8f0' }}>
                  <h3 style={{ fontSize: '1.05rem', margin: '0 0 0.25rem 0', color: '#0284c7' }}>{item.name || 'Fasilitas Kesehatan'}</h3>
                  <p style={{ margin: 0, fontSize: '0.875rem', color: '#475569' }}>📍 {item.city || item.address || 'Indonesia'}</p>
                  {item.type && <span style={{ display: 'inline-block', marginTop: '0.5rem', fontSize: '0.75rem', backgroundColor: '#f1f5f9', padding: '0.15rem 0.5rem', borderRadius: '4px', color: '#64748b' }}>{item.type}</span>}
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      {/* Grid Kategori Faskes */}
      {!hasSearched && (
        <section style={{ maxWidth: '800px', margin: '1.5rem auto', padding: '0 1.5rem' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '1rem' }}>Kategori Fasilitas</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '0.75rem' }}>
            {categories.map((cat, idx) => (
              <div key={idx} style={{ backgroundColor: '#ffffff', padding: '1rem', borderRadius: '12px', border: '1px solid #e2e8f0', textAlign: 'center' }}>
                <div style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>{cat.icon}</div>
                <h3 style={{ fontSize: '0.95rem', margin: 0 }}>{cat.name}</h3>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Footer */}
      <footer style={{ borderTop: '1px solid #e2e8f0', backgroundColor: '#ffffff', padding: '1.5rem', textAlign: 'center', color: '#94a3b8', fontSize: '0.85rem', marginTop: '3rem' }}>
        <p>© 2026 CariFaskes.id — pSEO Engine for Open Health Data</p>
      </footer>
    </div>
  );
}
