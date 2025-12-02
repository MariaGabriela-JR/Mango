// app/patients/add/success/page.jsx
import Link from 'next/link'

export default function RegisterSuccess({ searchParams }) {
  const message =
    searchParams?.message ||
    'Pedido de criação de conta enviado! Aguarde a autorização de um administrador'

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
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">Sucesso!</h1>
          <p className="text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">{message}</p>

          {/* Botões de ação */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <Link href="/patients/list" className="flex-1">
              <button className="w-full py-3 px-6 bg-gradient-to-r from-orange-600 to-amber-600 text-white font-medium rounded-lg hover:from-orange-700 hover:to-amber-700 transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
                Listar Pacientes
              </button>
            </Link>

            <Link href="/dashboard" className="flex-1">
              <button className="w-full py-3 px-6 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 text-gray-900 dark:text-white font-medium rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 shadow-sm">
                Dashboard
              </button>
            </Link>
          </div>

          {/* Link adicional */}
          <div className="mt-6">
            <Link
              href="/patients/add"
              className="text-orange-600 dark:text-orange-400 hover:text-orange-800 dark:hover:text-orange-300 text-sm font-medium transition-colors duration-200 inline-flex items-center gap-1 border border-orange-200 dark:border-orange-800/30 rounded-lg px-3 py-2 hover:bg-orange-50 dark:hover:bg-orange-900/20"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Adicionar outro paciente
            </Link>
          </div>
        </div>

        {/* Rodapé */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Sistema de Gerenciamento de Pacientes
          </p>
        </div>
      </div>
    </div>
  )
}
