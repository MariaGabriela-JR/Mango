'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import addPatient from '@/lib/addPatient'
import Navbar from '@/components/ui/Navbar'

export default function PatientRegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    cpf: '',
    birthDate: '',
    password: '',
    gender: '',
  })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  // Formatação automática do CPF
  const handleCpfChange = (e) => {
    let value = e.target.value.replace(/\D/g, '')
    if (value.length <= 11) {
      value = value.replace(/(\d{3})(\d)/, '$1.$2')
      value = value.replace(/(\d{3})(\d)/, '$1.$2')
      value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2')
    }
    setFormData((prev) => ({
      ...prev,
      cpf: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      const { firstName, lastName, cpf, birthDate, password, gender } = formData
      const result = await addPatient(firstName, lastName, cpf, birthDate, password, gender)
      router.push(`/patients/add/success?message=${encodeURIComponent(result.message)}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const isFormValid = Object.values(formData).every((value) => value.trim() !== '')

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#101111]">
      <Navbar />

      <div className="flex items-center justify-center min-h-[calc(100vh-80px)] px-4 py-8">
        <div className="w-full max-w-4xl">
          {/* Header Administrativo */}
          <div className="bg-white dark:bg-[#1e1e1e] rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
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
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                    Cadastro Administrativo de Paciente
                  </h1>
                  <p className="text-gray-600 dark:text-gray-400">
                    Sistema de gerenciamento de pacientes
                  </p>
                </div>
              </div>
              <Link
                href="/dashboard"
                className="inline-flex items-center text-sm text-orange-600 dark:text-orange-400 hover:text-orange-800 dark:hover:text-orange-300 transition-colors duration-200"
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

          {/* Formulário Retangular */}
          <div className="bg-white dark:bg-[#1e1e1e] rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Dados do Paciente
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Preencha todas as informações obrigatórias
              </p>
            </div>

            <form onSubmit={handleSubmit} className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label
                    htmlFor="firstName"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Nome *
                  </label>
                  <input
                    id="firstName"
                    name="firstName"
                    type="text"
                    placeholder="João"
                    value={formData.firstName}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-gray-50 dark:bg-[#2a2a2a] border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200 text-gray-900 dark:text-white"
                  />
                </div>

                <div>
                  <label
                    htmlFor="lastName"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Sobrenome *
                  </label>
                  <input
                    id="lastName"
                    name="lastName"
                    type="text"
                    placeholder="Lourenço"
                    value={formData.lastName}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-gray-50 dark:bg-[#2a2a2a] border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200 text-gray-900 dark:text-white"
                  />
                </div>

                <div>
                  <label
                    htmlFor="cpf"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    CPF *
                  </label>
                  <input
                    id="cpf"
                    name="cpf"
                    type="text"
                    placeholder="000.000.000-00"
                    value={formData.cpf}
                    onChange={handleCpfChange}
                    maxLength={14}
                    className="w-full px-3 py-2 bg-gray-50 dark:bg-[#2a2a2a] border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200 text-gray-900 dark:text-white"
                  />
                </div>

                <div>
                  <label
                    htmlFor="password"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Senha *
                  </label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Senha de acesso"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-gray-50 dark:bg-[#2a2a2a] border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200 text-gray-900 dark:text-white"
                  />
                </div>

                <div>
                  <label
                    htmlFor="birthDate"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Data de Nascimento *
                  </label>
                  <input
                    id="birthDate"
                    name="birthDate"
                    type="date"
                    value={formData.birthDate}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-gray-50 dark:bg-[#2a2a2a] border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200 text-gray-900 dark:text-white"
                  />
                </div>

                <div>
                  <label
                    htmlFor="gender"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Gênero *
                  </label>
                  <select
                    id="gender"
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    className="w-full px-3 py-2 bg-gray-50 dark:bg-[#2a2a2a] border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-colors duration-200 text-gray-900 dark:text-white"
                  >
                    <option value="">Selecione o gênero</option>
                    <option value="male">Masculino</option>
                    <option value="female">Feminino</option>
                    <option value="other">Outro</option>
                    <option value="unknown">Prefiro não informar</option>
                  </select>
                </div>
              </div>

              {error && (
                <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md mb-4">
                  <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                </div>
              )}

              <div className="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                <Link
                  href="/dashboard"
                  className="flex-1 py-2 px-4 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors duration-200 text-center"
                >
                  Cancelar
                </Link>
                <button
                  type="submit"
                  disabled={!isFormValid || isLoading}
                  className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors duration-200 ${
                    isFormValid && !isLoading
                      ? 'bg-orange-600 hover:bg-orange-700 text-white shadow-sm hover:shadow-md'
                      : 'bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                  }`}
                >
                  {isLoading ? (
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
                      Cadastrando...
                    </span>
                  ) : (
                    'Cadastrar Paciente'
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Informações Adicionais */}
          <div className="mt-4 text-center">
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Todos os campos marcados com * são obrigatórios
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
