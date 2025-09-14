import { Inter, Roboto_Mono, Playfair_Display } from 'next/font/google'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
  display: 'swap',
})

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
})

export const metadata = {
  title: 'MANGO',
  description: 'Um app minimalista e moderno',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${robotoMono.variable} ${playfair.variable}`}>
      <body>{children}</body>
    </html>
  )
}
