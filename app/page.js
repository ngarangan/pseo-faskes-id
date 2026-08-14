'use client';

import { useState } from 'react';
import faskesData from '../data/database_faskes.json';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  const data = Array.isArray(faskesData) ? faskesData : [];

  const handleSearch = (e) => {
    e.preventDefault();

    const q = query.toLowerCase().trim();

    if (!q) {
      setResults([]);
      setHasSearched(false);
      return;
    }

    const filtered = data.filter((item) => {
      const searchable = [
        item.nama,
        item.tipe,
        item.kota,
        item.provinsi,
        item.alamat,
        item.telepon,
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();

      return searchable.includes(q);
    });

    setResults(filtered);
    setHasSearched(true);
  };

  const formatPhone = (phone) => {
    if (!phone) return null;

    return (
      <a
        href={`tel:${phone}`}
        style={{
          color: '#0284c7',
          textDecoration: 'none',
        }}
      >
        {phone}
      </a>
    );
  };

  const formatWebsite = (website) => {
    if (!website) return null;

    let url = website;

    if (!/^https?:\/\//i.test(url)) {
      url = `https://${url}`;
    }

    return (
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        style={{
          color: '#0284c7',
          textDecoration: 'none',
          wordBreak: 'break-all',
        }}
      >
        {website}
      </a>
    );
  };

  const getMapUrl = (item) => {
    if (!item.latitude || !item.longitude) return null;

    return `https://www.openstreetmap.org/?mlat=${item.latitude}&mlon=${item.longitude}#map=18/${item.latitude}/${item.longitude}`;
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#f8fafc',
        color: '#0f172a',
        fontFamily:
          'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      }}
    >
      {/* HEADER */}
      <header
        style={{
          borderBottom: '1px solid #e2e8f0',
          backgroundColor: '#ffffff',
          padding: '1rem 1.25rem',
        }}
      >
        <div
          style={{
            maxWidth: '1000px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            gap: '0.55rem',
          }}
        >
          <span style={{ fontSize: '1.5rem' }}>🛡️</span>

          <span
            style={{
              fontWeight: '800',
              fontSize: '1.25rem',
              color: '#0284c7',
            }}
          >
            CariFaskes
            <span style={{ color: '#0f172a' }}>.id</span>
          </span>
        </div>
      </header>

      {/* MAIN */}
      <main
        style={{
          width: '100%',
          maxWidth: '900px',
          margin: '0 auto',
          padding: '2.5rem 1rem 4rem',
          boxSizing: 'border-box',
        }}
      >
        {/* HERO */}
        <section
          style={{
            textAlign: 'center',
            marginBottom: '2rem',
          }}
        >
          <h1
            style={{
              fontSize: 'clamp(1.7rem, 5vw, 2.25rem)',
              lineHeight: '1.2',
              fontWeight: '800',
              margin: '0 0 0.65rem',
            }}
          >
            Cari Fasilitas Kesehatan di Indonesia
          </h1>

          <p
            style={{
              color: '#64748b',
              fontSize: '0.95rem',
              lineHeight: '1.6',
              margin: '0 auto',
              maxWidth: '650px',
            }}
          >
            Temukan rumah sakit, klinik, praktik dokter, dan fasilitas
            kesehatan berdasarkan nama, kota, provinsi, atau alamat.
          </p>

          <div
            style={{
              marginTop: '0.75rem',
              fontSize: '0.9rem',
              color: '#64748b',
            }}
          >
            Terdata{' '}
            <strong style={{ color: '#0284c7' }}>
              {data.length.toLocaleString('id-ID')}
            </strong>{' '}
            faskes
          </div>
        </section>

        {/* SEARCH */}
        <form
          onSubmit={handleSearch}
          style={{
            display: 'flex',
            gap: '0.5rem',
            marginBottom: '2rem',
            width: '100%',
          }}
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Cari nama faskes, kota, provinsi, atau alamat..."
            style={{
              flex: 1,
              minWidth: 0,
              padding: '0.85rem 1rem',
              borderRadius: '9px',
              border: '1px solid #cbd5e1',
              outline: 'none',
              fontSize: '1rem',
              backgroundColor: '#ffffff',
              color: '#0f172a',
              boxSizing: 'border-box',
            }}
          />

          <button
            type="submit"
            style={{
              backgroundColor: '#0284c7',
              color: '#ffffff',
              border: 'none',
              padding: '0.85rem 1.25rem',
              borderRadius: '9px',
              fontWeight: '700',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
            }}
          >
            Cari
          </button>
        </form>

        {/* SEARCH RESULT */}
        {hasSearched && (
          <section>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: '1rem',
                marginBottom: '1rem',
                flexWrap: 'wrap',
              }}
            >
              <h2
                style={{
                  fontSize: '1.15rem',
                  fontWeight: '700',
                  margin: 0,
                }}
              >
                Hasil pencarian
              </h2>

              <span
                style={{
                  color: '#64748b',
                  fontSize: '0.85rem',
                }}
              >
                {results.length.toLocaleString('id-ID')} ditemukan
              </span>
            </div>

            {results.length === 0 ? (
              <div
                style={{
                  backgroundColor: '#ffffff',
                  borderRadius: '10px',
                  border: '1px solid #e2e8f0',
                  padding: '2rem 1.25rem',
                  textAlign: 'center',
                }}
              >
                <div
                  style={{
                    fontSize: '2rem',
                    marginBottom: '0.5rem',
                  }}
                >
                  🔍
                </div>

                <p
                  style={{
                    margin: '0 0 0.4rem',
                    fontWeight: '700',
                  }}
                >
                  Data tidak ditemukan
                </p>

                <p
                  style={{
                    margin: 0,
                    color: '#64748b',
                    fontSize: '0.9rem',
                  }}
                >
                  Tidak ditemukan faskes untuk pencarian "{query}".
                </p>
              </div>
            ) : (
              <div
                style={{
                  display: 'grid',
                  gap: '0.85rem',
                }}
              >
                {results.map((item, idx) => {
                  const mapUrl = getMapUrl(item);

                  return (
                    <article
                      key={
                        item.id ||
                        `${item.osm_type || 'osm'}-${item.osm_id || idx}`
                      }
                      style={{
                        backgroundColor: '#ffffff',
                        padding: '1.1rem 1.2rem',
                        borderRadius: '10px',
                        border: '1px solid #e2e8f0',
                      }}
                    >
                      {/* NAME */}
                      <h3
                        style={{
                          fontSize: '1.08rem',
                          lineHeight: '1.4',
                          margin: '0 0 0.4rem',
                          color: '#0284c7',
                        }}
                      >
                        {item.nama || 'Nama faskes tidak tersedia'}
                      </h3>

                      {/* TYPE */}
                      {item.tipe && (
                        <div
                          style={{
                            display: 'inline-block',
                            backgroundColor: '#e0f2fe',
                            color: '#0369a1',
                            fontSize: '0.75rem',
                            fontWeight: '700',
                            padding: '0.25rem 0.55rem',
                            borderRadius: '999px',
                            marginBottom: '0.65rem',
                          }}
                        >
                          {item.tipe}
                        </div>
                      )}

                      {/* LOCATION */}
                      {(item.kota || item.provinsi) && (
                        <p
                          style={{
                            margin: '0 0 0.35rem',
                            fontSize: '0.88rem',
                            color: '#475569',
                          }}
                        >
                          📍{' '}
                          {[item.kota, item.provinsi]
                            .filter(Boolean)
                            .join(', ')}
                        </p>
                      )}

                      {/* ADDRESS */}
                      {item.alamat && (
                        <p
                          style={{
                            margin: '0 0 0.5rem',
                            fontSize: '0.85rem',
                            lineHeight: '1.5',
                            color: '#64748b',
                          }}
                        >
                          {item.alamat}
                        </p>
                      )}

                      {/* PHONE */}
                      {item.telepon && (
                        <p
                          style={{
                            margin: '0 0 0.35rem',
                            fontSize: '0.85rem',
                            color: '#475569',
                          }}
                        >
                          ☎️ {formatPhone(item.telepon)}
                        </p>
                      )}

                      {/* WEBSITE */}
                      {item.website && (
                        <p
                          style={{
                            margin: '0 0 0.65rem',
                            fontSize: '0.85rem',
                            color: '#475569',
                          }}
                        >
                          🌐 {formatWebsite(item.website)}
                        </p>
                      )}

                      {/* COORDINATE */}
                      {item.latitude && item.longitude && (
                        <p
                          style={{
                            margin: '0 0 0.75rem',
                            fontSize: '0.78rem',
                            color: '#94a3b8',
                          }}
                        >
                          Koordinat: {item.latitude}, {item.longitude}
                        </p>
                      )}

                      {/* MAP */}
                      {mapUrl && (
                        <a
                          href={mapUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{
                            display: 'inline-block',
                            backgroundColor: '#f0f9ff',
                            color: '#0369a1',
                            border: '1px solid #bae6fd',
                            padding: '0.5rem 0.75rem',
                            borderRadius: '7px',
                            textDecoration: 'none',
                            fontSize: '0.8rem',
                            fontWeight: '700',
                          }}
                        >
                          📍 Lihat lokasi
                        </a>
                      )}
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        )}

        {/* INITIAL STATE */}
        {!hasSearched && (
          <section
            style={{
              backgroundColor: '#ffffff',
              border: '1px solid #e2e8f0',
              borderRadius: '10px',
              padding: '1.5rem',
              textAlign: 'center',
            }}
          >
            <div
              style={{
                fontSize: '2rem',
                marginBottom: '0.5rem',
              }}
            >
              🏥
            </div>

            <h2
              style={{
                fontSize: '1rem',
                margin: '0 0 0.4rem',
              }}
            >
              Cari faskes berdasarkan lokasi
            </h2>

            <p
              style={{
                margin: 0,
                color: '#64748b',
                fontSize: '0.85rem',
                lineHeight: '1.6',
              }}
            >
              Masukkan nama rumah sakit, klinik, dokter, kota, kabupaten,
              provinsi, atau alamat pada kolom pencarian.
            </p>
          </section>
        )}
      </main>

      {/* FOOTER */}
      <footer
        style={{
          borderTop: '1px solid #e2e8f0',
          backgroundColor: '#ffffff',
          padding: '1.5rem 1rem',
          textAlign: 'center',
        }}
      >
        <p
          style={{
            margin: 0,
            color: '#94a3b8',
            fontSize: '0.78rem',
            lineHeight: '1.5',
          }}
        >
          CariFaskes.id — Direktori fasilitas kesehatan Indonesia
        </p>
      </footer>
    </div>
  );
}
