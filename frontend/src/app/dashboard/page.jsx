// app/dashboard/page.jsx
'use client'

import ModelViewer from '@/components/ui/ModelViewer'
import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import Navbar from '@/components/ui/Navbar'
import Link from 'next/link'

export default function Dashboard() {
  const { user, requireAuth, isLoading } = useAuth()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    requireAuth('/scientist/login')
    setLoading(false)
  }, [requireAuth])

  if (isLoading || loading) return <p className="flex items-center justify-center">Carregando...</p>

  return (
    <div className="min-h-screen bg-white dark:bg-[#1a1b1c] text-black dark:text-white flex flex-col">
      <Navbar />
      <main className="flex flex-1 flex-col md:flex-row items-center justify-between px-8 md:px-20 gap-10">
        <div className="flex flex-col items-start text-left ml-30 max-w-lg">
          <h1 className="text-5xl font-bold font-sans leading-tight mb-4">
            Bem-vindo, {user?.name || 'Usuário'}!
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
            Gerencie seus pacientes e sessões de forma rápida e prática.
          </p>
          <div className="flex flex-col md:flex-row gap-4">
            <Link href="/patient/add">
              <button className="py-3 px-8 text-xl bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-md text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
                Novo Paciente
              </button>
            </Link>
            <Link href="/">
              <button className="py-3 px-8 text-xl bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-md text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
                Nova Sessão
              </button>
            </Link>
          </div>
        </div>
        <div className="flex justify-center">
          <ModelViewer
            className="w-64 h-64 md:w-96 md:h-96 lg:w-[500px] lg:h-[500px]"
            modelPath="/frontend/models/source.glb"
          />
        </div>
      </main>
    </div>
  )
}
