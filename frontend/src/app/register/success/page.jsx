'use client'

import Link from 'next/link'
import { useSearchParams } from 'next/navigation'

export default function RegisterSuccess() {
  let message = 'Pedido de criação de conta enviado! Aguarde a autorização de um administrador';
  if (typeof window !== 'undefined') {
    const searchParams = useSearchParams();
    message = searchParams.get('message') || message;
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 dark:bg-[#121212]">
      <h1 className="text-3xl font-bold mb-4 text-center">{message}</h1>

      <div className="flex gap-4 mt-6">
        <Link href="/login">
          <button className="md:w-32 md:h-12 w-28 bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-lg text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
            Login
          </button>
        </Link>
        <Link href="/">
          <button className="md:w-32 md:h-12 w-28 bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-lg text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
            Home
          </button>
        </Link>
      </div>
    </div>
  )
}
