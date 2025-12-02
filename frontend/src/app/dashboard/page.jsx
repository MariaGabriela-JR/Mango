// app/dashboard/page.jsx
'use client'

import ModelViewer from '@/components/ui/ModelViewer'
import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { listPatients } from '@/lib/listPatients'
import { fetchProfile } from '@/lib/fetchProfile'
import Navbar from '@/components/ui/Navbar'
import Link from 'next/link'

// Função para calcular a idade a partir da data de nascimento
const calculateAge = (birthDate) => {
  if (!birthDate) return 'N/A'
  const today = new Date()
  const birth = new Date(birthDate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  return age
}

const formatGender = (gender) => {
  const genderMap = {
    male: 'Masculino',
    female: 'Feminino',
    other: 'Outro',
    unknown: 'Não informado',
  }
  return genderMap[gender] || 'Não informado'
}

export default function Dashboard() {
  const { user, requireAuth, isLoading } = useAuth()
  const [loading, setLoading] = useState(true)
  const [patients, setPatients] = useState([])
  const [patientsError, setPatientsError] = useState(null)
  const [patientsLoading, setPatientsLoading] = useState(true)
  const [scientistProfile, setScientistProfile] = useState(null)
  const [profileLoading, setProfileLoading] = useState(true)

  useEffect(() => {
    requireAuth('/scientist/login')
    setLoading(false)
  }, [requireAuth])

  // Carregar perfil do cientista
  useEffect(() => {
    if (!user) return

    const loadScientistProfile = async () => {
      try {
        setProfileLoading(true)
        const profileData = await fetchProfile()
        setScientistProfile(profileData)
      } catch (err) {
        console.error('Erro ao carregar perfil do cientista:', err)
        // Se houver erro, usamos os dados básicos do user
      } finally {
        setProfileLoading(false)
      }
    }

    loadScientistProfile()
  }, [user])

  useEffect(() => {
    if (!user) return

    const fetchPatients = async () => {
      try {
        setPatientsLoading(true)
        const patientsData = await listPatients()
        setPatients(patientsData)
      } catch (err) {
        setPatientsError(err.message)
        console.error('Erro ao carregar pacientes:', err)
      } finally {
        setPatientsLoading(false)
      }
    }

    fetchPatients()
  }, [user])

  // Função para obter o nome completo do cientista
  const getScientistName = () => {
    if (scientistProfile?.first_name && scientistProfile?.last_name) {
      return `${scientistProfile.first_name} ${scientistProfile.last_name}`
    }
    if (user?.firstName && user?.lastName) {
      return `${user.firstName} ${user.lastName}`
    }
    if (user?.name) {
      return user.name
    }
    return 'Usuário'
  }

  if (isLoading || loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-[#101111] flex items-center justify-center">
        <div className="flex flex-col items-center">
          <div className="w-12 h-12 border-4 border-orange-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Carregando...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-12 max-w-7xl mx-auto">
          {/* Text Content */}
          <div className="flex flex-col items-start text-left max-w-2xl">
            <div className="mb-8">
              <h1 className="text-4xl lg:text-5xl font-bold leading-tight mb-4 text-gray-900 dark:text-white">
                Bem-vindo, {profileLoading ? '...' : getScientistName()}!
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-300">
                Gerencie seus pacientes e sessões de forma eficiente com nossa plataforma intuitiva.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 w-full">
              <Link href="/patients/add" className="flex-1">
                <button className="w-full py-3 px-6 bg-gradient-to-r from-orange-600 to-orange-700 text-white font-medium rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                  Novo Paciente
                </button>
              </Link>

              <Link href="/sessions/new" className="flex-1">
                <button className="w-full py-3 px-6 bg-white dark:bg-[#1e1e1e] border border-orange-200 dark:border-orange-800/50 text-gray-900 dark:text-white font-medium rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 shadow-sm hover:shadow-md flex items-center justify-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                    />
                  </svg>
                  Nova Sessão
                </button>
              </Link>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-2 gap-6 mt-12 w-full">
              <div className="bg-white dark:bg-[#1e1e1e] p-4 rounded-lg shadow-sm border border-orange-100 dark:border-orange-900/30">
                <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                  {patientsLoading ? '...' : patients.length}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Pacientes Ativos</div>
              </div>

              <div className="bg-white dark:bg-[#1e1e1e] p-4 rounded-lg shadow-sm border border-orange-100 dark:border-orange-900/30">
                <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {patientsLoading ? '...' : patients.filter((p) => p.last_session_date).length}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Com Sessões</div>
              </div>
            </div>
          </div>

          {/* Model Viewer */}
          <div className="flex justify-center lg:justify-end">
            <div className="relative">
              <ModelViewer
                className="w-80 h-80 lg:w-96 lg:h-96 xl:w-[420px] xl:h-[420px] rounded-2xl border border-orange-100 dark:border-orange-900/30 shadow-xl"
                modelPath="/models/source.glb"
              />
            </div>
          </div>
        </div>

        {/* Lista de Pacientes Section */}
        <div className="max-w-7xl mx-auto mt-16">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Meus Pacientes</h2>
            <Link href="/patients/list">
              <div className="text-orange-600 dark:text-orange-400 text-sm font-medium cursor-pointer hover:underline">
                Lista completa
              </div>
            </Link>
          </div>

          {patientsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="bg-white dark:bg-[#1e1e1e] p-6 rounded-lg shadow-sm border border-orange-100 dark:border-orange-900/30 animate-pulse"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 bg-gray-300 dark:bg-gray-700 rounded-full"></div>
                    <div className="space-y-2 flex-1">
                      <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-3/4"></div>
                      <div className="h-3 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : patientsError ? (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <p className="text-red-600 dark:text-red-400">{patientsError}</p>
            </div>
          ) : patients.length === 0 ? (
            <div className="bg-white dark:bg-[#1e1e1e] rounded-lg shadow-sm border border-orange-100 dark:border-orange-900/30 p-8 text-center">
              <svg
                className="w-12 h-12 text-gray-400 dark:text-gray-600 mx-auto mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"
                />
              </svg>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Nenhum paciente encontrado
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Comece adicionando seu primeiro paciente
              </p>
              <Link href="/patients/add">
                <button className="py-2 px-4 bg-gradient-to-r from-orange-600 to-orange-700 text-white rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all duration-200">
                  Adicionar Paciente
                </button>
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {patients.slice(0, 6).map((patient) => (
                <div
                  key={patient.id}
                  className="bg-white dark:bg-[#1e1e1e] p-6 rounded-lg shadow-sm border border-orange-100 dark:border-orange-900/30 hover:shadow-md transition-all duration-200"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-full flex items-center justify-center border border-orange-200 dark:border-orange-800/30">
                      <span className="text-orange-600 dark:text-orange-400 font-medium text-lg">
                        {patient.first_name?.[0]}
                        {patient.last_name?.[0]}
                      </span>
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-900 dark:text-white">
                        {patient.first_name} {patient.last_name}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1 mt-1">
                        <div>{calculateAge(patient.birth_date)} anos</div>
                        <div>{formatGender(patient.gender)}</div>
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-3 border-t border-orange-50 dark:border-orange-900/20">
                    <span className="text-gray-500 dark:text-gray-400 text-xs">
                      ID: {patient.id}
                    </span>
                    <button className="text-orange-600 dark:text-orange-400 hover:text-orange-800 dark:hover:text-orange-300 transition-colors duration-200 p-1 rounded">
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
