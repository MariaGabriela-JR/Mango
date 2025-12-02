// app/sessions/new/page.jsx
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { discoverEdfFiles } from '@/lib/sessions/discoverEdfFiles'
import { listPatients } from '@/lib/listPatients'
import { createSession } from '@/lib/sessions/createSession'
import Navbar from '@/components/ui/Navbar'
import Link from 'next/link'

export default function CreateSessionPage() {
  const router = useRouter()
  const { user, requireAuth, isLoading } = useAuth()
  const [loading, setLoading] = useState(true)

  // Estados do formulário
  const [formData, setFormData] = useState({
    sessionName: '',
    edfFile: '',
    patientId: '',
  })

  // Estados dos dados
  const [edfFiles, setEdfFiles] = useState([])
  const [patients, setPatients] = useState([])
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Verificação de autenticação
  useEffect(() => {
    requireAuth('/scientist/login')
    setLoading(false)
  }, [requireAuth])

  // Carregar dados iniciais
  useEffect(() => {
    if (!user) return

    const loadInitialData = async () => {
      try {
        setError('')
        const [filesData, patientsData] = await Promise.all([discoverEdfFiles(), listPatients()])

        // Garantir que filesData seja um array
        setEdfFiles(Array.isArray(filesData) ? filesData : [])
        setPatients(Array.isArray(patientsData) ? patientsData : [])
      } catch (err) {
        setError(`Erro ao carregar dados: ${err.message}`)
        console.error('Erro ao carregar dados iniciais:', err)
      }
    }

    loadInitialData()
  }, [user])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      const { sessionName, edfFile, patientId } = formData

      // Validação
      if (!sessionName.trim()) {
        throw new Error('Nome da sessão é obrigatório')
      }
      if (!edfFile) {
        throw new Error('Selecione um arquivo EDF')
      }
      if (!patientId) {
        throw new Error('Selecione um paciente')
      }

      // Criar sessão
      const result = await createSession({
        sessionName: sessionName.trim(),
        edfFile: edfFile,
        patientId: patientId,
      })

      // Redirecionar para sucesso
      router.push(`/sessions/new/success?message=${encodeURIComponent(result.message)}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const isFormValid =
    formData.sessionName.trim() !== '' && formData.edfFile !== '' && formData.patientId !== ''

  // Estados de loading
  if (isLoading || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f] flex items-center justify-center">
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

      <div className="flex items-center justify-center min-h-[calc(100vh-80px)] px-4 py-8">
        <div className="w-full max-w-4xl">
          {/* Header */}
          <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl shadow-xl p-6 mb-8 border border-orange-100 dark:border-orange-900/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-lg flex items-center justify-center border border-orange-200 dark:border-orange-800/30">
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
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                    Nova Sessão EEG
                  </h1>
                  <p className="text-gray-600 dark:text-gray-400">
                    Crie uma nova sessão de eletroencefalografia
                  </p>
                </div>
              </div>
              <Link
                href="/dashboard"
                className="inline-flex items-center text-sm text-orange-600 dark:text-orange-400 hover:text-orange-800 dark:hover:text-orange-300 transition-colors duration-200 border border-orange-200 dark:border-orange-800/30 rounded-lg px-4 py-2 hover:bg-orange-50 dark:hover:bg-orange-900/20"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
                Voltar ao Dashboard
              </Link>
            </div>
          </div>

          {/* Formulário */}
          <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl shadow-xl border border-orange-100 dark:border-orange-900/30">
            <div className="p-6 border-b border-orange-100 dark:border-orange-900/30">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Configuração da Sessão
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Defina os parâmetros para a nova sessão EEG
              </p>
            </div>

            <form onSubmit={handleSubmit} className="p-6">
              <div className="space-y-6">
                {/* Nome da Sessão */}
                <div>
                  <label
                    htmlFor="sessionName"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Nome da Sessão *
                  </label>
                  <input
                    id="sessionName"
                    name="sessionName"
                    type="text"
                    placeholder="Ex: Sessão EEG - Paciente João - 2024"
                    value={formData.sessionName}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                  />
                </div>

                {/* Seleção de Arquivo EDF */}
                <div>
                  <label
                    htmlFor="edfFile"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Arquivo EDF *
                  </label>
                  <select
                    id="edfFile"
                    name="edfFile"
                    value={formData.edfFile}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                  >
                    <option value="">Selecione um arquivo EDF</option>
                    {edfFiles.map((file, index) => (
                      <option key={index} value={file.path}>
                        {file.path} ({file.name}) - {file.size} KB
                      </option>
                    ))}
                  </select>
                  {edfFiles.length === 0 && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Nenhum arquivo EDF encontrado
                    </p>
                  )}
                </div>

                {/* Seleção de Paciente */}
                <div>
                  <label
                    htmlFor="patientId"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Paciente *
                  </label>
                  <select
                    id="patientId"
                    name="patientId"
                    value={formData.patientId}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                  >
                    <option value="">Selecione um paciente</option>
                    {patients.map((patient) => (
                      <option key={patient.patient_iid} value={patient.patient_iid}>
                        {patient.first_name} {patient.last_name}
                        {patient.birth_date &&
                          ` - ${new Date().getFullYear() - new Date(patient.birth_date).getFullYear()} anos`}
                      </option>
                    ))}
                  </select>
                  {patients.length === 0 && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Nenhum paciente cadastrado
                    </p>
                  )}
                </div>
              </div>

              {/* Mensagem de Erro */}
              {error && (
                <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg mt-6">
                  <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                </div>
              )}

              {/* Ações do Formulário */}
              <div className="flex gap-3 pt-6 border-t border-orange-100 dark:border-orange-900/30 mt-6">
                <Link
                  href="/dashboard"
                  className="flex-1 py-3 px-4 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 text-center font-medium"
                >
                  Cancelar
                </Link>
                <button
                  type="submit"
                  disabled={!isFormValid || isSubmitting}
                  className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
                    isFormValid && !isSubmitting
                      ? 'bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                      : 'bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                  }`}
                >
                  {isSubmitting ? (
                    <span className="flex items-center justify-center">
                      <svg
                        className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                      Criando Sessão...
                    </span>
                  ) : (
                    'Criar Sessão EEG'
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Informações Adicionais */}
          <div className="mt-6 text-center">
            <p className="text-xs text-gray-500 dark:text-gray-400 bg-white dark:bg-[#1e1e1e] rounded-lg p-3 border border-orange-100 dark:border-orange-900/30">
              Todos os campos marcados com * são obrigatórios
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
