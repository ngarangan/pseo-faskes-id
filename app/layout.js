export const metadata = {
  title: 'CariFaskes - Direktori Fasilitas Kesehatan Indonesia',
  description: 'Temukan informasi puskesmas, rumah sakit, dan klinik terdekat.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="id">
      <body style={{ fontFamily: 'system-ui, sans-serif', margin: 0, padding: 0 }}>
        {children}
      </body>
    </html>
  )
}
