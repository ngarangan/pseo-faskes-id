'use client';

import { useState } from 'react';
import faskesData from '../data/database_faskes.json';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  // Ambil data faskes
  const data = Array.isArray(faskesData) ? faskesData : [];

  const handleSearch = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const q = query.toLowerCase().trim();
    const filtered = data.filter((item) => {
      const nama = (item.nama || item.name || '').toLowerCase();
      const kota = (item.kota || item.city || '').toLowerCase();
      const alamat = (item.alamat || item.address || '').toLowerCase();
      return nama.includes(q) || kota.includes(q) || alamat.includes(q);
    });

    setResults(filtered);
    setHasSearched(true);
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8fafc', color: '#0f172a', fontFamily: 'system-ui, sans-serif' }}>
      {/* Header */}
      <header style={{ borderBottom: '1px solid #e2e8f0', backgroundColor: '#ffffff', padding: '1rem 1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span style={{ fontSize: '1.5rem' }}>🛡️</span>
        <span style={{ fontWeight: 'bold', fontSize: '1.25rem', color: '#0284c7' }}>CariFaskes<span style={{ color: '#0f172a' }}>.id</span></span>
      </header>

      {/* Main Content */}
      <main style={{ padding: '2rem 1rem', maxWidth: '700px', margin: '0 auto' }}>
        <section style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '800', margin: '0 0 0.5rem 0' }}>Cari Fasilitas Kesehatan</h1>
          <p style={{ color: '#64748b', fontSize: '0.95rem', margin: 0 }}>
            Terdata <strong style={{ color: '#0284c7' }}>{data.length}</strong> faskes terdaftar
          </p>
        </section>

        {/* Form Search */}
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', marginBottom: '2rem' }}>
          <input 
            type="text" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Cari kota/faskes (contoh: Sambas)..." 
            style={{ flex: 1, padding: '0.75rem 1rem', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', fontSize: '1rem' }}
          />
          <button type="submit" style={{ backgroundColor: '#0284c7', color: '#fff', border: 'none', padding: '0.75rem 1.25rem', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' }}>
            Cari
          </button>
        </form>

        {/* Hasil Pencarian */}
        {hasSearched && (
          <section>
            <h2 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem' }}>
              Hasil untuk "{query}" ({results.length} ditemukan)
            </h2>

            {results.length === 0 ? (
              <p style={{ color: '#64748b', textAlign: 'center', padding: '1.5rem', backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                Tidak ditemukan data untuk kata kunci "{query}".
              </p>
            ) : (
              <div style={{ display: 'grid', gap: '0.75rem' }}>
                {results.map((item, idx) => (
                  <div key={idx} style={{ backgroundColor: '#ffffff', padding: '1rem 1.25rem', borderRadius: '10px', border: '1px solid #e2e8f0' }}>
                    <h3 style={{ fontSize: '1.05rem', margin: '0 0 0.25rem 0', color: '#0284c7' }}>{item.nama || item.name}</h3>
                    <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.875rem', color: '#475569' }}>📍 {item.kota || item.city}</p>
                    <p style={{ margin: 0, fontSize: '0.8rem', color: '#94a3b8' }}>{item.alamat || item.address}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
