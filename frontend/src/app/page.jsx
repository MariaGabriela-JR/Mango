'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f] flex flex-col items-center justify-center px-4 relative">
      {/* Conteúdo Principal */}
      <div className="text-center mb-12">
        {/* Badge UTFPR */}
        <div className="inline-flex items-center px-4 py-2 bg-white dark:bg-[#1e1e1e] rounded-full border border-orange-200 dark:border-orange-800/30 shadow-sm mb-8 animate-fadeIn delay-200 opacity-0">
          <span className="text-sm font-medium text-orange-600 dark:text-orange-400">
            Powered by UTFPR
          </span>
        </div>

        {/* Logo MANGO */}
        <div className="mb-6 animate-fadeIn delay-400 opacity-0">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-2xl">M</span>
            </div>
            <h1 className="text-6xl lg:text-8xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">
              MANGO
            </h1>
          </div>
        </div>

        {/* Descrição */}
        <p className="text-xl lg:text-2xl text-gray-600 dark:text-gray-300 font-light max-w-2xl mx-auto leading-relaxed animate-fadeIn delay-600 opacity-0">
          Mindwave Analysis for Neurofeedback & Graphical Observation
        </p>

        {/* Destaques */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto mt-12 animate-fadeIn delay-800 opacity-0">
          <div className="bg-white dark:bg-[#1e1e1e] p-6 rounded-2xl border border-orange-100 dark:border-orange-900/30 shadow-sm hover:shadow-md transition-all duration-300">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-lg flex items-center justify-center mb-4 mx-auto">
              <svg
                className="w-6 h-6 text-orange-600 dark:text-orange-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Análise Avançada</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Processamento de sessões EEG para análise técnica.
            </p>
          </div>

          <div className="bg-white dark:bg-[#1e1e1e] p-6 rounded-2xl border border-orange-100 dark:border-orange-900/30 shadow-sm hover:shadow-md transition-all duration-300">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-lg flex items-center justify-center mb-4 mx-auto">
              <svg
                className="w-6 h-6 text-orange-600 dark:text-orange-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              Visualização Intuitiva
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Gráficos e interações em 3D para melhor compreensão dos dados.
            </p>
          </div>

          <div className="bg-white dark:bg-[#1e1e1e] p-6 rounded-2xl border border-orange-100 dark:border-orange-900/30 shadow-sm hover:shadow-md transition-all duration-300">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-lg flex items-center justify-center mb-4 mx-auto">
              <svg
                className="text-orange-600 dark:text-orange-400"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="size-6"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"
                />
              </svg>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              Armazenagem de Dados
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Armazenamento e Processamento de Sinais EEG com estruturação em banco de dados para
              consulta eficiente.
            </p>
          </div>
        </div>
      </div>

      {/* Botões de Ação */}
      <div className="flex flex-col sm:flex-row gap-4 mt-8 animate-fadeIn delay-1000 opacity-0">
        <Link href="/scientist/login" className="flex-1 min-w-[200px]">
          <button className="w-full py-4 px-8 bg-gradient-to-r from-orange-600 to-amber-600 text-white font-semibold rounded-2xl hover:from-orange-700 hover:to-amber-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center justify-center gap-3">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
              />
            </svg>
            Fazer Login
          </button>
        </Link>

        <Link href="/scientist/register" className="flex-1 min-w-[200px]">
          <button className="w-full py-4 px-8 bg-white dark:bg-[#1e1e1e] border border-orange-200 dark:border-orange-800/50 text-gray-900 dark:text-white font-semibold rounded-2xl hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center justify-center gap-3">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
              />
            </svg>
            Criar Conta
          </button>
        </Link>
      </div>

      {/* Botão Sobre */}
      <div className="mt-4 animate-fadeIn delay-1200 opacity-0">
        <Link href="/about">
          <button className="py-3 px-6 bg-white/80 dark:bg-[#1e1e1e]/80 backdrop-blur-sm border border-orange-200 dark:border-orange-800/30 text-gray-700 dark:text-gray-300 font-medium rounded-xl hover:bg-white dark:hover:bg-[#1e1e1e] hover:shadow-lg transition-all duration-300 hover:-translate-y-0.5">
            Sobre o Projeto
          </button>
        </Link>
      </div>

      {/* Rodapé */}
      <div className="mt-16 text-center animate-fadeIn delay-1200 opacity-0">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Plataforma desenvolvida para pesquisa e análise de sessões EEG.
        </p>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          0% {
            opacity: 0;
            transform: translateY(30px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.8s ease-out forwards;
        }
        .delay-200 {
          animation-delay: 0.2s;
        }
        .delay-400 {
          animation-delay: 0.4s;
        }
        .delay-600 {
          animation-delay: 0.6s;
        }
        .delay-800 {
          animation-delay: 0.8s;
        }
        .delay-1000 {
          animation-delay: 1s;
        }
        .delay-1200 {
          animation-delay: 1.2s;
        }
      `}</style>
    </div>
  )
}
