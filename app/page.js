'use client';

import { useState } from 'react';
import faskesData from '../data/database_faskes.json';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [expandedId, setExpandedId] = useState(null);

  // =========================================================
  // DATA
  // =========================================================

  const data = Array.isArray(faskesData) ? faskesData : [];

  // =========================================================
  // SEARCH
  // =========================================================

  const handleSearch = (e) => {
    e.preventDefault();

    const q = query.trim().toLowerCase();

    if (!q) {
      setResults([]);
      setHasSearched(false);
      setExpandedId(null);
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
        item.website,
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();

      return searchable.includes(q);
    });

    setResults(filtered);
    setHasSearched(true);
    setExpandedId(null);
  };

  // =========================================================
  // GOOGLE MAPS
  // =========================================================

  const getGoogleMapsUrl = (item) => {
    if (
      item.latitude === undefined ||
      item.longitude === undefined ||
      item.latitude === null ||
      item.longitude === null
    ) {
      return null;
    }

    if (item.latitude === '' || item.longitude === '') {
      return null;
    }

    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
      `${item.latitude},${item.longitude}`
    )}`;
  };

  // =========================================================
  // WEBSITE
  // =========================================================

  const getWebsiteUrl = (website) => {
    if (!website) return null;

    if (/^https?:\/\//i.test(website)) {
      return website;
    }

    return `https://${website}`;
  };

  // =========================================================
  // TELEPHONE
  // =========================================================

  const getPhoneUrl = (phone) => {
    if (!phone) return null;

    const cleaned = String(phone).replace(/[^\d+]/g, '');

    return `tel:${cleaned}`;
  };

  // =========================================================
  // FORMAT LOCATION
  // =========================================================

  const getLocation = (item) => {
    return [item.kota, item.provinsi]
      .filter(Boolean)
      .join(', ');
  };

  // =========================================================
  // RESULT LIMIT
  // =========================================================

  const visibleResults = results.slice(0, 50);

  // =========================================================
  // RENDER
  // =========================================================

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

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header
        style={{
          backgroundColor: '#ffffff',
          borderBottom: '1px solid #e2e8f0',
          padding: '1rem',
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
          <span style={{ fontSize: '1.45rem' }}>🏥</span>

          <div>
            <div
              style={{
                fontWeight: '800',
                fontSize: '1.2rem',
                color: '#0284c7',
                lineHeight: 1.1,
              }}
            >
              CariFaskes
              <span style={{ color: '#0f172a' }}>.id</span>
            </div>

            <div
              style={{
                fontSize: '0.7rem',
                color: '#94a3b8',
                marginTop: '0.15rem',
              }}
            >
              Direktori Fasilitas Kesehatan Indonesia
            </div>
          </div>
        </div>
      </header>

      {/* =====================================================
          MAIN
      ===================================================== */}

      <main
        style={{
          width: '100%',
          maxWidth: '900px',
          margin: '0 auto',
          padding: '2.5rem 1rem 4rem',
          boxSizing: 'border-box',
        }}
      >

        {/* ===================================================
            HERO
        =================================================== */}

        <section
          style={{
            textAlign: 'center',
            marginBottom: '2rem',
          }}
        >
          <h1
            style={{
              fontSize: 'clamp(1.7rem, 5vw, 2.3rem)',
              lineHeight: 1.2,
              fontWeight: '800',
              margin: '0 0 0.7rem',
            }}
          >
            Cari Fasilitas Kesehatan di Indonesia
          </h1>

          <p
            style={{
              maxWidth: '680px',
              margin: '0 auto',
              color: '#64748b',
              fontSize: '0.95rem',
              lineHeight: 1.6,
            }}
          >
            Temukan rumah sakit, klinik, praktik dokter, dan fasilitas
            kesehatan berdasarkan nama, lokasi, atau alamat.
          </p>

          <div
            style={{
              marginTop: '0.8rem',
              color: '#64748b',
              fontSize: '0.9rem',
            }}
          >
            Database saat ini:{' '}
            <strong style={{ color: '#0284c7' }}>
              {data.length.toLocaleString('id-ID')}
            </strong>{' '}
            faskes
          </div>
        </section>

        {/* ===================================================
            SEARCH BOX
        =================================================== */}

        <form
          onSubmit={handleSearch}
          style={{
            display: 'flex',
            gap: '0.55rem',
            width: '100%',
            marginBottom: '2rem',
          }}
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Contoh: Aceh, Bandung, RSUD, klinik..."
            aria-label="Cari fasilitas kesehatan"
            style={{
              flex: 1,
              minWidth: 0,
              padding: '0.9rem 1rem',
              borderRadius: '10px',
              border: '1px solid #cbd5e1',
              backgroundColor: '#ffffff',
              color: '#0f172a',
              fontSize: '1rem',
              outline: 'none',
              boxSizing: 'border-box',
            }}
          />

          <button
            type="submit"
            style={{
              border: 'none',
              borderRadius: '10px',
              padding: '0.9rem 1.3rem',
              backgroundColor: '#0284c7',
              color: '#ffffff',
              fontSize: '0.95rem',
              fontWeight: '700',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
            }}
          >
            Cari
          </button>
        </form>

        {/* ===================================================
            INITIAL STATE
        =================================================== */}

        {!hasSearched && (
          <section
            style={{
              backgroundColor: '#ffffff',
              border: '1px solid #e2e8f0',
              borderRadius: '12px',
              padding: '2rem 1.25rem',
              textAlign: 'center',
            }}
          >
            <div
              style={{
                fontSize: '2.5rem',
                marginBottom: '0.6rem',
              }}
            >
              🔎
            </div>

            <h2
              style={{
                margin: '0 0 0.45rem',
                fontSize: '1.05rem',
              }}
            >
              Cari faskes berdasarkan lokasi atau nama
            </h2>

            <p
              style={{
                margin: 0,
                color: '#64748b',
                fontSize: '0.85rem',
                lineHeight: 1.6,
              }}
            >
              Coba cari nama rumah sakit, klinik, kota, kabupaten,
              provinsi, atau alamat.
            </p>
          </section>
        )}

        {/* ===================================================
            SEARCH RESULTS
        =================================================== */}

        {hasSearched && (
          <section>

            {/* RESULT HEADER */}

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
              <div>
                <h2
                  style={{
                    margin: 0,
                    fontSize: '1.2rem',
                    fontWeight: '800',
                  }}
                >
                  Hasil pencarian
                </h2>

                <div
                  style={{
                    marginTop: '0.25rem',
                    color: '#64748b',
                    fontSize: '0.82rem',
                  }}
                >
                  Pencarian: "{query}"
                </div>
              </div>

              <div
                style={{
                  color: '#64748b',
                  fontSize: '0.85rem',
                }}
              >
                <strong style={{ color: '#0284c7' }}>
                  {results.length.toLocaleString('id-ID')}
                </strong>{' '}
                ditemukan
              </div>
            </div>

            {/* NO RESULT */}

            {results.length === 0 && (
              <div
                style={{
                  backgroundColor: '#ffffff',
                  border: '1px solid #e2e8f0',
                  borderRadius: '12px',
                  padding: '2rem 1.25rem',
                  textAlign: 'center',
                }}
              >
                <div style={{ fontSize: '2rem' }}>🔍</div>

                <h3
                  style={{
                    margin: '0.5rem 0 0.35rem',
                    fontSize: '1rem',
                  }}
                >
                  Faskes tidak ditemukan
                </h3>

                <p
                  style={{
                    margin: 0,
                    color: '#64748b',
                    fontSize: '0.85rem',
                  }}
                >
                  Belum ada data yang cocok dengan pencarian "{query}".
                </p>
              </div>
            )}

            {/* RESULT LIST */}

            {visibleResults.length > 0 && (
              <div
                style={{
                  display: 'grid',
                  gap: '1rem',
                }}
              >

                {visibleResults.map((item, index) => {
                  const itemId =
                    item.id ||
                    `${item.osm_type || 'osm'}-${item.osm_id || index}`;

                  const isExpanded = expandedId === itemId;

                  const mapUrl = getGoogleMapsUrl(item);

                  const websiteUrl = getWebsiteUrl(item.website);

                  const phoneUrl = getPhoneUrl(item.telepon);

                  return (
                    <article
                      key={itemId}
                      style={{
                        backgroundColor: '#ffffff',
                        border: '1px solid #e2e8f0',
                        borderRadius: '12px',
                        padding: '1.2rem',
                        boxSizing: 'border-box',
                      }}
                    >

                      {/* NAME */}

                      <h3
                        style={{
                          margin: '0 0 0.5rem',
                          color: '#0284c7',
                          fontSize: '1.15rem',
                          lineHeight: 1.35,
                        }}
                      >
                        {item.nama || 'Nama faskes tidak tersedia'}
                      </h3>

                      {/* TYPE */}

                      {item.tipe && (
                        <span
                          style={{
                            display: 'inline-block',
                            backgroundColor: '#e0f2fe',
                            color: '#0369a1',
                            padding: '0.28rem 0.65rem',
                            borderRadius: '999px',
                            fontSize: '0.75rem',
                            fontWeight: '700',
                            marginBottom: '0.85rem',
                          }}
                        >
                          {item.tipe}
                        </span>
                      )}

                      {/* LOCATION */}

                      {getLocation(item) && (
                        <div
                          style={{
                            display: 'flex',
                            gap: '0.5rem',
                            alignItems: 'flex-start',
                            marginBottom: '0.55rem',
                          }}
                        >
                          <span>📍</span>

                          <div
                            style={{
                              fontSize: '0.88rem',
                              color: '#334155',
                              lineHeight: 1.5,
                            }}
                          >
                            {getLocation(item)}
                          </div>
                        </div>
                      )}

                      {/* ADDRESS */}

                      {item.alamat && (
                        <div
                          style={{
                            display: 'flex',
                            gap: '0.5rem',
                            alignItems: 'flex-start',
                            marginBottom: '0.55rem',
                          }}
                        >
                          <span>🏠</span>

                          <div
                            style={{
                              fontSize: '0.85rem',
                              color: '#64748b',
                              lineHeight: 1.55,
                            }}
                          >
                            {item.alamat}
                          </div>
                        </div>
                      )}

                      {/* PHONE */}

                      {item.telepon && (
                        <div
                          style={{
                            display: 'flex',
                            gap: '0.5rem',
                            alignItems: 'flex-start',
                            marginBottom: '0.55rem',
                          }}
                        >
                          <span>☎️</span>

                          <a
                            href={phoneUrl}
                            style={{
                              color: '#0284c7',
                              textDecoration: 'none',
                              fontSize: '0.85rem',
                            }}
                          >
                            {item.telepon}
                          </a>
                        </div>
                      )}

                      {/* WEBSITE */}

                      {item.website && (
                        <div
                          style={{
                            display: 'flex',
                            gap: '0.5rem',
                            alignItems: 'flex-start',
                            marginBottom: '0.65rem',
                          }}
                        >
                          <span>🌐</span>

                          <a
                            href={websiteUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              color: '#0284c7',
                              textDecoration: 'none',
                              fontSize: '0.85rem',
                              wordBreak: 'break-all',
                            }}
                          >
                            {item.website}
                          </a>
                        </div>
                      )}

                      {/* COORDINATE */}

                      {(item.latitude !== undefined &&
                        item.latitude !== null &&
                        item.longitude !== undefined &&
                        item.longitude !== null) && (
                        <div
                          style={{
                            fontSize: '0.78rem',
                            color: '#94a3b8',
                            marginBottom: '0.9rem',
                          }}
                        >
                          📌 {item.latitude}, {item.longitude}
                        </div>
                      )}

                      {/* ACTIONS */}

                      <div
                        style={{
                          display: 'flex',
                          gap: '0.55rem',
                          flexWrap: 'wrap',
                        }}
                      >

                        {mapUrl && (
                          <a
                            href={mapUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.35rem',
                              backgroundColor: '#e0f2fe',
                              border: '1px solid #bae6fd',
                              color: '#0369a1',
                              padding: '0.55rem 0.8rem',
                              borderRadius: '8px',
                              textDecoration: 'none',
                              fontSize: '0.82rem',
                              fontWeight: '700',
                            }}
                          >
                            🗺️ Buka di Google Maps
                          </a>
                        )}

                        <button
                          type="button"
                          onClick={() => {
                            setExpandedId(
                              isExpanded ? null : itemId
                            );
                          }}
                          style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.35rem',
                            backgroundColor: '#ffffff',
                            border: '1px solid #cbd5e1',
                            color: '#334155',
                            padding: '0.55rem 0.8rem',
                            borderRadius: '8px',
                            fontSize: '0.82rem',
                            fontWeight: '700',
                            cursor: 'pointer',
                          }}
                        >
                          {isExpanded
                            ? '▲ Sembunyikan'
                            : 'ℹ️ Lihat detail'}
                        </button>
                      </div>

                      {/* =================================================
                          EXPANDED DETAILS
                      ================================================= */}

                      {isExpanded && (
                        <div
                          style={{
                            marginTop: '1rem',
                            paddingTop: '1rem',
                            borderTop: '1px solid #e2e8f0',
                          }}
                        >

                          <h4
                            style={{
                              margin: '0 0 0.8rem',
                              fontSize: '0.95rem',
                            }}
                          >
                            Informasi Fasilitas Kesehatan
                          </h4>

                          <div
                            style={{
                              display: 'grid',
                              gap: '0.55rem',
                              fontSize: '0.82rem',
                            }}
                          >

                            <InfoRow
                              label="Nama"
                              value={item.nama}
                            />

                            <InfoRow
                              label="Jenis"
                              value={item.tipe}
                            />

                            <InfoRow
                              label="Kota/Kabupaten"
                              value={item.kota}
                            />

                            <InfoRow
                              label="Provinsi"
                              value={item.provinsi}
                            />

                            <InfoRow
                              label="Alamat"
                              value={item.alamat}
                            />

                            <InfoRow
                              label="Telepon"
                              value={item.telepon}
                            />

                            <InfoRow
                              label="Website"
                              value={item.website}
                            />

                            <InfoRow
                              label="Latitude"
                              value={item.latitude}
                            />

                            <InfoRow
                              label="Longitude"
                              value={item.longitude}
                            />

                            <InfoRow
                              label="OSM Type"
                              value={item.osm_type}
                            />

                            <InfoRow
                              label="OSM ID"
                              value={item.osm_id}
                            />

                          </div>

                        </div>
                      )}

                    </article>
                  );
                })}

              </div>
            )}

            {/* MORE RESULT NOTICE */}

            {results.length > 50 && (
              <div
                style={{
                  marginTop: '1rem',
                  padding: '1rem',
                  backgroundColor: '#ffffff',
                  border: '1px solid #e2e8f0',
                  borderRadius: '10px',
                  textAlign: 'center',
                  color: '#64748b',
                  fontSize: '0.82rem',
                }}
              >
                Menampilkan 50 dari{' '}
                {results.length.toLocaleString('id-ID')} hasil.
                <br />
                Pada versi final, hasil akan menggunakan pagination.
              </div>
            )}

          </section>
        )}

      </main>

      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer
        style={{
          backgroundColor: '#ffffff',
          borderTop: '1px solid #e2e8f0',
          padding: '1.5rem 1rem',
          textAlign: 'center',
        }}
      >
        <p
          style={{
            margin: 0,
            color: '#94a3b8',
            fontSize: '0.78rem',
          }}
        >
          © {new Date().getFullYear()} CariFaskes.id
        </p>

        <p
          style={{
            margin: '0.35rem 0 0',
            color: '#cbd5e1',
            fontSize: '0.7rem',
          }}
        >
          Data fasilitas kesehatan bersumber dari OpenStreetMap.
        </p>
      </footer>

    </div>
  );
}


// =========================================================
// INFO ROW
// =========================================================

function InfoRow({ label, value }) {
  if (
    value === undefined ||
    value === null ||
    value === ''
  ) {
    return null;
  }

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: '120px 1fr',
        gap: '0.5rem',
        lineHeight: 1.5,
      }}
    >
      <span
        style={{
          color: '#94a3b8',
        }}
      >
        {label}
      </span>

      <span
        style={{
          color: '#334155',
          wordBreak: 'break-word',
        }}
      >
        {String(value)}
      </span>
    </div>
  );
}
