'use client';

import { useState } from 'react';
import faskesData from '../data/database_faskes.json';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  // Pastikan data selalu berupa array
  const data = Array.isArray(faskesData) ? faskesData : [];

  /*
   * Membersihkan text untuk pencarian
   */
  const normalize = (value) => {
    return String(value || '')
      .toLowerCase()
      .trim();
  };

  /*
   * Format koordinat
   */
  const formatCoordinate = (value) => {
    if (value === null || value === undefined || value === '') {
      return '';
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return String(value);
    }

    return number.toFixed(6);
  };

  /*
   * Membuat URL Google Maps.
   *
   * Kita tidak hanya mengirim koordinat.
   * Nama + wilayah + koordinat memberikan konteks
   * tambahan kepada Google Maps.
   */
  const getGoogleMapsUrl = (item) => {
    const nama = item.nama || item.name || '';
    const kota = item.kota || item.city || '';
    const provinsi = item.provinsi || item.province || '';
    const alamat = item.alamat || item.address || '';

    const latitude = item.latitude;
    const longitude = item.longitude;

    const locationParts = [
      nama,
      alamat,
      kota,
      provinsi,
      'Indonesia',
    ].filter(Boolean);

    let searchQuery = locationParts.join(', ');

    /*
     * Kalau koordinat tersedia, tambahkan ke query.
     */
    if (
      latitude !== undefined &&
      latitude !== null &&
      longitude !== undefined &&
      longitude !== null
    ) {
      searchQuery += ` ${latitude},${longitude}`;
    }

    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
      searchQuery
    )}`;
  };

  /*
   * URL Google Maps untuk navigasi / directions.
   */
  const getDirectionsUrl = (item) => {
    const nama = item.nama || item.name || '';
    const kota = item.kota || item.city || '';
    const provinsi = item.provinsi || item.province || '';

    const latitude = item.latitude;
    const longitude = item.longitude;

    let destination = `${nama}, ${kota}, ${provinsi}, Indonesia`;

    if (
      latitude !== undefined &&
      latitude !== null &&
      longitude !== undefined &&
      longitude !== null
    ) {
      destination = `${latitude},${longitude}`;
    }

    return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(
      destination
    )}`;
  };

  /*
   * Pencarian
   */
  const handleSearch = (e) => {
    e.preventDefault();

    const q = normalize(query);

    if (!q) {
      setResults([]);
      setHasSearched(false);
      return;
    }

    const filtered = data.filter((item) => {
      const nama = normalize(item.nama || item.name);
      const tipe = normalize(item.tipe || item.type);
      const kota = normalize(item.kota || item.city);
      const provinsi = normalize(item.provinsi || item.province);
      const alamat = normalize(item.alamat || item.address);
      const telepon = normalize(item.telepon || item.phone);
      const website = normalize(item.website || item.url);

      return (
        nama.includes(q) ||
        tipe.includes(q) ||
        kota.includes(q) ||
        provinsi.includes(q) ||
        alamat.includes(q) ||
        telepon.includes(q) ||
        website.includes(q)
      );
    });

    setResults(filtered);
    setHasSearched(true);
  };

  /*
   * Warna badge berdasarkan tipe
   */
  const getTypeStyle = (tipe) => {
    const value = normalize(tipe);

    if (value.includes('rumah sakit')) {
      return {
        backgroundColor: '#fee2e2',
        color: '#b91c1c',
      };
    }

    if (value.includes('klinik')) {
      return {
        backgroundColor: '#dbeafe',
        color: '#0369a1',
      };
    }

    if (value.includes('dokter')) {
      return {
        backgroundColor: '#dcfce7',
        color: '#15803d',
      };
    }

    if (value.includes('puskesmas')) {
      return {
        backgroundColor: '#ccfbf1',
        color: '#0f766e',
      };
    }

    return {
      backgroundColor: '#e0f2fe',
      color: '#0369a1',
    };
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
          backgroundColor: '#ffffff',
          borderBottom: '1px solid #e2e8f0',
          padding: '16px 20px',
        }}
      >
        <div
          style={{
            maxWidth: '900px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
          }}
        >
          <div
            style={{
              width: '38px',
              height: '38px',
              borderRadius: '10px',
              backgroundColor: '#0284c7',
              color: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px',
            }}
          >
            🏥
          </div>

          <div>
            <div
              style={{
                fontSize: '19px',
                fontWeight: 800,
                color: '#0284c7',
                lineHeight: 1.1,
              }}
            >
              CariFaskes
              <span style={{ color: '#0f172a' }}>.id</span>
            </div>

            <div
              style={{
                fontSize: '12px',
                color: '#64748b',
                marginTop: '3px',
              }}
            >
              Direktori Fasilitas Kesehatan Indonesia
            </div>
          </div>
        </div>
      </header>

      {/* MAIN */}
      <main
        style={{
          maxWidth: '900px',
          margin: '0 auto',
          padding: '38px 16px 60px',
        }}
      >
        {/* HERO */}
        <section
          style={{
            textAlign: 'center',
            marginBottom: '30px',
          }}
        >
          <h1
            style={{
              fontSize: 'clamp(30px, 7vw, 48px)',
              lineHeight: 1.12,
              fontWeight: 800,
              margin: '0 auto 14px',
              maxWidth: '760px',
              letterSpacing: '-1px',
            }}
          >
            Cari Fasilitas Kesehatan di Indonesia
          </h1>

          <p
            style={{
              margin: '0 auto',
              maxWidth: '720px',
              color: '#64748b',
              fontSize: '17px',
              lineHeight: 1.7,
            }}
          >
            Temukan rumah sakit, klinik, praktik dokter, dan fasilitas
            kesehatan berdasarkan nama, kota, provinsi, atau alamat.
          </p>

          <div
            style={{
              marginTop: '14px',
              color: '#64748b',
              fontSize: '16px',
            }}
          >
            Terdata{' '}
            <strong
              style={{
                color: '#0284c7',
                fontSize: '20px',
              }}
            >
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
            gap: '10px',
            marginBottom: '32px',
          }}
        >
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Cari nama faskes, kota, provinsi..."
            aria-label="Cari fasilitas kesehatan"
            style={{
              flex: 1,
              minWidth: 0,
              padding: '15px 17px',
              borderRadius: '12px',
              border: '1px solid #cbd5e1',
              backgroundColor: '#ffffff',
              color: '#0f172a',
              fontSize: '16px',
              outline: 'none',
              boxSizing: 'border-box',
            }}
          />

          <button
            type="submit"
            style={{
              border: 'none',
              borderRadius: '12px',
              padding: '0 23px',
              backgroundColor: '#0284c7',
              color: '#ffffff',
              fontSize: '16px',
              fontWeight: 700,
              cursor: 'pointer',
              whiteSpace: 'nowrap',
            }}
          >
            Cari
          </button>
        </form>

        {/* HASIL */}
        {hasSearched && (
          <section>
            {/* HEADER HASIL */}
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: '15px',
                marginBottom: '16px',
              }}
            >
              <h2
                style={{
                  fontSize: '22px',
                  margin: 0,
                  fontWeight: 800,
                }}
              >
                Hasil pencarian
              </h2>

              <span
                style={{
                  color: '#64748b',
                  fontSize: '15px',
                  whiteSpace: 'nowrap',
                }}
              >
                {results.length.toLocaleString('id-ID')} ditemukan
              </span>
            </div>

            {/* TIDAK ADA HASIL */}
            {results.length === 0 ? (
              <div
                style={{
                  backgroundColor: '#ffffff',
                  border: '1px solid #e2e8f0',
                  borderRadius: '14px',
                  padding: '30px 20px',
                  textAlign: 'center',
                }}
              >
                <div
                  style={{
                    fontSize: '38px',
                    marginBottom: '10px',
                  }}
                >
                  🔎
                </div>

                <h3
                  style={{
                    margin: '0 0 8px',
                    fontSize: '18px',
                  }}
                >
                  Faskes tidak ditemukan
                </h3>

                <p
                  style={{
                    margin: 0,
                    color: '#64748b',
                    lineHeight: 1.6,
                  }}
                >
                  Tidak ditemukan fasilitas kesehatan untuk kata kunci{' '}
                  <strong>"{query}"</strong>.
                </p>
              </div>
            ) : (
              <>
                {/* LIST */}
                <div
                  style={{
                    display: 'grid',
                    gap: '14px',
                  }}
                >
                  {results.slice(0, 100).map((item, idx) => {
                    const nama = item.nama || item.name || 'Tanpa nama';
                    const tipe =
                      item.tipe || item.type || 'Fasilitas Kesehatan';
                    const kota = item.kota || item.city || '';
                    const provinsi = item.provinsi || item.province || '';
                    const alamat = item.alamat || item.address || '';
                    const telepon = item.telepon || item.phone || '';
                    const website = item.website || item.url || '';

                    const latitude = item.latitude;
                    const longitude = item.longitude;

                    const hasCoordinates =
                      latitude !== undefined &&
                      latitude !== null &&
                      longitude !== undefined &&
                      longitude !== null &&
                      latitude !== '' &&
                      longitude !== '';

                    const mapsUrl = getGoogleMapsUrl(item);
                    const directionsUrl = getDirectionsUrl(item);

                    return (
                      <article
                        key={
                          item.id ||
                          `${item.osm_type || 'item'}-${
                            item.osm_id || idx
                          }`
                        }
                        style={{
                          backgroundColor: '#ffffff',
                          border: '1px solid #e2e8f0',
                          borderRadius: '16px',
                          padding: '20px',
                          boxShadow: '0 1px 2px rgba(15, 23, 42, 0.03)',
                        }}
                      >
                        {/* NAMA */}
                        <h3
                          style={{
                            margin: '0 0 9px',
                            fontSize: '21px',
                            lineHeight: 1.35,
                            color: '#0284c7',
                            fontWeight: 800,
                          }}
                        >
                          {nama}
                        </h3>

                        {/* TIPE */}
                        <div
                          style={{
                            display: 'inline-block',
                            padding: '5px 11px',
                            borderRadius: '999px',
                            fontSize: '13px',
                            fontWeight: 700,
                            marginBottom: '15px',
                            ...getTypeStyle(tipe),
                          }}
                        >
                          {tipe}
                        </div>

                        {/* LOKASI */}
                        {(kota || provinsi) && (
                          <div
                            style={{
                              display: 'flex',
                              gap: '9px',
                              marginBottom: '9px',
                              color: '#334155',
                              fontSize: '15px',
                              lineHeight: 1.5,
                            }}
                          >
                            <span>📍</span>

                            <span>
                              {[kota, provinsi]
                                .filter(Boolean)
                                .join(', ')}
                            </span>
                          </div>
                        )}

                        {/* ALAMAT */}
                        {alamat && (
                          <div
                            style={{
                              display: 'flex',
                              gap: '9px',
                              marginBottom: '9px',
                              color: '#475569',
                              fontSize: '14px',
                              lineHeight: 1.6,
                            }}
                          >
                            <span>🏠</span>

                            <span>{alamat}</span>
                          </div>
                        )}

                        {/* TELEPON */}
                        {telepon && (
                          <div
                            style={{
                              display: 'flex',
                              gap: '9px',
                              marginBottom: '9px',
                              fontSize: '14px',
                              lineHeight: 1.5,
                            }}
                          >
                            <span>📞</span>

                            <a
                              href={`tel:${telepon}`}
                              style={{
                                color: '#0369a1',
                                textDecoration: 'none',
                              }}
                            >
                              {telepon}
                            </a>
                          </div>
                        )}

                        {/* WEBSITE */}
                        {website && (
                          <div
                            style={{
                              display: 'flex',
                              gap: '9px',
                              marginBottom: '12px',
                              fontSize: '14px',
                              lineHeight: 1.5,
                              overflowWrap: 'anywhere',
                            }}
                          >
                            <span>🌐</span>

                            <a
                              href={website}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                color: '#0369a1',
                                textDecoration: 'none',
                              }}
                            >
                              {website}
                            </a>
                          </div>
                        )}

                        {/* KOORDINAT */}
                        {hasCoordinates && (
                          <div
                            style={{
                              color: '#94a3b8',
                              fontSize: '13px',
                              marginTop: '8px',
                              marginBottom: '16px',
                            }}
                          >
                            Koordinat:{' '}
                            {formatCoordinate(latitude)},{' '}
                            {formatCoordinate(longitude)}
                          </div>
                        )}

                        {/* ACTION */}
                        <div
                          style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            gap: '9px',
                            paddingTop: '4px',
                          }}
                        >
                          {hasCoordinates && (
                            <>
                              <a
                                href={mapsUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                  display: 'inline-flex',
                                  alignItems: 'center',
                                  justifyContent: 'center',
                                  gap: '7px',
                                  padding: '10px 15px',
                                  borderRadius: '10px',
                                  backgroundColor: '#e0f2fe',
                                  border: '1px solid #bae6fd',
                                  color: '#0369a1',
                                  textDecoration: 'none',
                                  fontSize: '14px',
                                  fontWeight: 700,
                                }}
                              >
                                📍 Lihat di Google Maps
                              </a>

                              <a
                                href={directionsUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                  display: 'inline-flex',
                                  alignItems: 'center',
                                  justifyContent: 'center',
                                  gap: '7px',
                                  padding: '10px 15px',
                                  borderRadius: '10px',
                                  backgroundColor: '#ffffff',
                                  border: '1px solid #cbd5e1',
                                  color: '#334155',
                                  textDecoration: 'none',
                                  fontSize: '14px',
                                  fontWeight: 700,
                                }}
                              >
                                🧭 Petunjuk Arah
                              </a>
                            </>
                          )}

                          {telepon && (
                            <a
                              href={`tel:${telepon}`}
                              style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '7px',
                                padding: '10px 15px',
                                borderRadius: '10px',
                                backgroundColor: '#f0fdf4',
                                border: '1px solid #bbf7d0',
                                color: '#15803d',
                                textDecoration: 'none',
                                fontSize: '14px',
                                fontWeight: 700,
                              }}
                            >
                              📞 Telepon
                            </a>
                          )}
                        </div>
                      </article>
                    );
                  })}
                </div>

                {/* LIMIT */}
                {results.length > 100 && (
                  <div
                    style={{
                      marginTop: '20px',
                      padding: '15px',
                      textAlign: 'center',
                      color: '#64748b',
                      fontSize: '14px',
                      backgroundColor: '#ffffff',
                      border: '1px solid #e2e8f0',
                      borderRadius: '12px',
                    }}
                  >
                    Menampilkan 100 dari{' '}
                    {results.length.toLocaleString('id-ID')} hasil.
                    Gunakan kata kunci yang lebih spesifik untuk menemukan
                    fasilitas tertentu.
                  </div>
                )}
              </>
            )}
          </section>
        )}

        {/* INFO AWAL */}
        {!hasSearched && (
          <section
            style={{
              marginTop: '30px',
              backgroundColor: '#ffffff',
              border: '1px solid #e2e8f0',
              borderRadius: '16px',
              padding: '22px',
            }}
          >
            <h2
              style={{
                margin: '0 0 10px',
                fontSize: '18px',
              }}
            >
              Cari fasilitas kesehatan di Indonesia
            </h2>

            <p
              style={{
                margin: 0,
                color: '#64748b',
                lineHeight: 1.7,
                fontSize: '14px',
              }}
            >
              Gunakan pencarian untuk menemukan rumah sakit, klinik,
              praktik dokter, dan fasilitas kesehatan berdasarkan nama,
              wilayah, atau alamat.
            </p>
          </section>
        )}
      </main>

      {/* FOOTER */}
      <footer
        style={{
          borderTop: '1px solid #e2e8f0',
          backgroundColor: '#ffffff',
          padding: '25px 16px',
          color: '#64748b',
          fontSize: '13px',
          textAlign: 'center',
        }}
      >
        <div>
          © {new Date().getFullYear()} CariFaskes.id
        </div>

        <div style={{ marginTop: '5px' }}>
          Direktori fasilitas kesehatan Indonesia
        </div>
      </footer>
    </div>
  );
}
