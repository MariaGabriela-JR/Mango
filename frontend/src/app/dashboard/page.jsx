'use client'

import ModelViewer from '@/components/ui/ModelViewer'
import { useEffect, useRef, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import Link from 'next/link'

export default function Dashboard() {
  const { user, requireAuth, isLoading, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    requireAuth('/login')
  }, [requireAuth])

  // Fecha menu ao clicar fora
  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false)
      }
    }
    if (menuOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [menuOpen])

  if (isLoading) return <p className="flex items-center justify-center">Carregando...</p>

  return (
    <div className="min-h-screen bg-white dark:bg-[#1a1b1c] text-black dark:text-white flex flex-col">
      {/* Navbar */}
      <nav className="w-full flex items-center justify-between p-4 bg-gray-100 dark:bg-[#101111]">
        <div className="text-3xl font-bold font-sans">MANGO</div>

        {/* Hamburger */}
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="flex flex-col justify-between w-6 h-5 focus:outline-none"
          >
            <span className="block h-0.5 w-full bg-black dark:bg-white rounded"></span>
            <span className="block h-0.5 w-full bg-black dark:bg-white rounded"></span>
            <span className="block h-0.5 w-full bg-black dark:bg-white rounded"></span>
          </button>

          {/* Dropdown Menu */}
          {menuOpen && (
            <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-[#1a1b1c] border border-gray-300 dark:border-gray-700 rounded shadow-lg z-10">
              <ul className="flex flex-col">
                <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                  Home
                </li>
                <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                  Pacientes
                </li>
                <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                  Sessões
                </li>
                <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                  Perfil
                </li>
                <li
                  className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer"
                  onClick={logout}
                >
                  Sair
                </li>
              </ul>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex flex-1 flex-col md:flex-row items-center justify-between px-8 md:px-20 gap-10">
        {/* Esquerda: Texto e Botões */}
        <div className="flex flex-col items-start text-left ml-30 max-w-lg">
          <h1 className="text-5xl font-bold font-sans leading-tight mb-4">
            Bem-vindo, {user?.name || 'Usuário'}!
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
            Gerencie seus pacientes e sessões de forma rápida e prática.
          </p>
          <div className="flex flex-col md:flex-row gap-4">
            <Link href="/newPatient">
              <button className="py-3 px-8 text-xl bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-md text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
                Novo Paciente
              </button>
            </Link>
            <Link href="/newSession">
              <button className="py-3 px-8 text-xl bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-md text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
                Nova Sessão
              </button>
            </Link>
          </div>
        </div>

        {/* Direita: Modelo 3D */}
        <div className="flex justify-center">
          <ModelViewer
            className="w-64 h-64 md:w-96 md:h-96 lg:w-[500px] lg:h-[500px]"
            modelPath="/models/source.glb"
          />
        </div>
      </main>
    </div>
  )
}
