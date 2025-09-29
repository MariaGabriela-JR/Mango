// app/patients/list/page.jsx
'use client'

import { useEffect, useState } from 'react'
import { listPatients } from '@/lib/listPatients'
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

// Função para formatar o gênero
const formatGender = (gender) => {
  const genderMap = {
    male: 'Masculino',
    female: 'Feminino',
    other: 'Outro',
    unknown: 'Não informado',
  }
  return genderMap[gender] || 'Não informado'
}

export default function PatientsList() {
  const [patients, setPatients] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listPatients()
      .then((data) => setPatients(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
            <div>
              <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white mb-2">
                Lista de Pacientes
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Gerencie todos os pacientes do seu consultório
              </p>
            </div>

            <Link href="/patients/add" className="mt-4 sm:mt-0">
              <button className="py-2 px-6 bg-gradient-to-r from-orange-600 to-orange-700 text-white font-medium rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center gap-2">
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
          </div>

          {/* Loading State */}
          {loading && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
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
          )}

          {/* Error State */}
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center">
              <svg
                className="w-12 h-12 text-red-400 mx-auto mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <h3 className="text-lg font-medium text-red-800 dark:text-red-300 mb-2">
                Erro ao carregar pacientes
              </h3>
              <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
              <button
                onClick={() => window.location.reload()}
                className="py-2 px-4 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200"
              >
                Tentar Novamente
              </button>
            </div>
          )}

          {/* Empty State */}
          {!loading && !error && patients.length === 0 && (
            <div className="bg-white dark:bg-[#1e1e1e] rounded-lg shadow-sm border border-orange-100 dark:border-orange-900/30 p-8 text-center">
              <svg
                className="w-16 h-16 text-gray-400 dark:text-gray-600 mx-auto mb-4"
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
              <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-2">
                Nenhum paciente encontrado
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Comece adicionando seu primeiro paciente ao sistema
              </p>
              <Link href="/patients/add">
                <button className="py-2 px-6 bg-gradient-to-r from-orange-600 to-orange-700 text-white rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all duration-200 shadow-md hover:shadow-lg">
                  Adicionar Primeiro Paciente
                </button>
              </Link>
            </div>
          )}

          {/* Patients Grid */}
          {!loading && !error && patients.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {patients.map((patient) => (
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
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 dark:text-white truncate">
                        {patient.first_name} {patient.last_name}
                      </h3>
                      <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1 mt-1">
                        <div>{calculateAge(patient.birth_date)} anos</div>
                        <div>{formatGender(patient.gender)}</div>
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-3 border-t border-orange-50 dark:border-orange-900/20">
                    <span className="text-gray-500 dark:text-gray-400 text-xs font-mono">
                      ID: {patient.id}
                    </span>
                    <button
                      className="text-orange-600 dark:text-orange-400 hover:text-orange-800 dark:hover:text-orange-300 transition-colors duration-200 p-1 rounded flex items-center gap-1 text-sm"
                      onClick={() => {
                        // Aqui você pode implementar a lógica de edição
                        console.log('Editar paciente:', patient.id)
                      }}
                    >
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
                      Editar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Back Button */}
          <div className="flex justify-center mt-8">
            <Link href="/dashboard">
              <button className="py-2 px-6 bg-white dark:bg-[#1e1e1e] border border-orange-200 dark:border-orange-800/50 text-gray-900 dark:text-white font-medium rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 shadow-sm hover:shadow-md flex items-center justify-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10 19l-7-7m0 0l7-7m-7 7h18"
                  />
                </svg>
                Voltar ao Dashboard
              </button>
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}
