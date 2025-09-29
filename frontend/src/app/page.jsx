'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-white dark:bg-[#1a1b1c] text-black dark:text-white px-4">
      <div className="flex flex-col items-center mb-8">
        <p className="text-lg font-light text-center font-sans mb-2 animate-fadeIn delay-200 opacity-0">
          Powered by UTFPR
        </p>

        <h1 className="text-9xl font-bold font-sans text-center animate-fadeIn delay-400 opacity-0">
          MANGO
        </h1>

        <p className="text-lg text-center font-light font-sans max-w-md mt-4 animate-fadeIn delay-600 opacity-0">
          Mindwave Analysis for Neurofeedback & Graphical Observation
        </p>
      </div>
      <div className="flex items-center justify-center gap-4 mt-2 animate-fadeIn delay-1000 opacity-0">
        <Link href="/scientist/login">
          <button className="md:w-32 md:h-12 w-28 bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-lg text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
            Login
          </button>
        </Link>
        <Link href="/scientist/register">
          <button className="md:w-32 md:h-12 w-28 bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-lg text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
            Cadastre-se
          </button>
        </Link>
      </div>
      <style jsx>{`
        @keyframes fadeIn {
          0% {
            opacity: 0;
            transform: translateY(20px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.8s forwards;
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
        .delay-1000 {
          animation-delay: 1s;
        }
      `}</style>
    </div>
  )
}
