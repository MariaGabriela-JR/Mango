// app/layout.jsx
import { Inter } from 'next/font/google'
import './globals.css'

export const inter = Inter({
subsets: ['latin'],
display: 'swap',
variable: '--font-inter',
preload: false
})

export const metadata = {
  title: 'MANGO',
  description: 'Um app minimalista e moderno',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
