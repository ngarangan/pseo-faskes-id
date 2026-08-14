export const metadata = {
  metadataBase: new URL('https://carifaskes.id'),

  title: {
    default: 'CariFaskes.id - Direktori Fasilitas Kesehatan Indonesia',
    template: '%s | CariFaskes.id',
  },

  description:
    'Cari rumah sakit, klinik, praktik dokter, dan fasilitas kesehatan di Indonesia berdasarkan nama, kota, kabupaten, dan provinsi.',

  keywords: [
    'faskes',
    'fasilitas kesehatan',
    'rumah sakit',
    'klinik',
    'dokter',
    'puskesmas',
    'rumah sakit Indonesia',
    'klinik Indonesia',
  ],

  openGraph: {
    title: 'CariFaskes.id - Direktori Fasilitas Kesehatan Indonesia',
    description:
      'Temukan rumah sakit, klinik, praktik dokter, dan fasilitas kesehatan di Indonesia.',
    type: 'website',
    locale: 'id_ID',
    siteName: 'CariFaskes.id',
    url: 'https://carifaskes.id',
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="id">
      <body
        style={{
          fontFamily:
            'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          margin: 0,
          padding: 0,
        }}
      >
        {children}
      </body>
    </html>
  );
}
