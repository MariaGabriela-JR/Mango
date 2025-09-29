'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export default function RegisterSuccess() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('registrationToken')
      if (!token) {
        router.push('/') // redireciona se não houver token
      } else {
        setLoading(false)
      }
    }
  }, [router])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f] flex items-center justify-center">
        <div className="flex flex-col items-center">
          <div className="w-16 h-16 border-4 border-orange-200 border-t-orange-600 rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Carregando...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f] flex items-center justify-center px-4 py-8">
      <div className="max-w-md w-full">
        {/* Card principal */}
        <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl shadow-xl p-8 text-center border border-orange-100 dark:border-orange-900/30">
          {/* Ícone de sucesso animado */}
          <div className="relative mb-6">
            <div className="w-24 h-24 bg-gradient-to-br from-orange-500 to-amber-500 rounded-full flex items-center justify-center mx-auto shadow-lg">
              <svg
                className="w-12 h-12 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            {/* Efeito de pulso */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-24 h-24 rounded-full bg-orange-200 animate-ping opacity-20"></div>
            </div>
          </div>

          {/* Título e mensagem */}
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
            Conta Registrada com Sucesso!
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            Aguarde a liberação de um administrador para acessar sua conta.
          </p>

          {/* Botões de ação */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <Link href="/scientist/login" className="flex-1">
              <button className="w-full py-3 px-6 bg-gradient-to-r from-orange-600 to-amber-600 text-white font-medium rounded-lg hover:from-orange-700 hover:to-amber-700 transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
                Fazer Login
              </button>
            </Link>
            <Link href="/" className="flex-1">
              <button className="w-full py-3 px-6 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-lg hover:bg-gray-50 dark:hover:bg-[#363636] transition-all duration-200 shadow-sm">
                Página Inicial
              </button>
            </Link>
          </div>

          {/* Informação adicional */}
          <div className="text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-[#2a2a2a] rounded-lg p-3">
            <p>Vocá receberá um e-mail quando sua conta for ativada.</p>
          </div>
        </div>

        {/* Rodapé */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Precisa de ajuda?{' '}
            <Link href="/contact" className="text-orange-600 dark:text-orange-400 hover:underline">
              Entre em contato
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
