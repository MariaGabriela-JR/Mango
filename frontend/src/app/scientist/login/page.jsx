'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { authLogin } from '@/lib/authLogin' // Importando a função de login

export default function LoginPage() {
  const { redirectIfLogged, isLoading } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    redirectIfLogged('/dashboard')
  }, [redirectIfLogged])

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
      // Usando a função authLogin para fazer o login
      const result = await authLogin(formData.email, formData.password)

      // Se o login for bem-sucedido, redirecionar para o dashboard
      if (result.success) {
        window.location.href = '/dashboard'
      } else {
        setError(result.message || 'Login falhou. Verifique suas credenciais.')
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Login falhou. Verifique suas credenciais.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const isFormValid = formData.email.trim() !== '' && formData.password.trim() !== ''

  if (isLoading) {
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
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f] flex items-center justify-center p-4">
      <div className="w-full max-w-6xl flex bg-white dark:bg-[#1e1e1e] rounded-2xl shadow-2xl overflow-hidden border border-orange-100 dark:border-orange-900/30">
        {/* Coluna esquerda - Branding */}
        <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-orange-400 to-orange-700 items-center justify-center p-12">
          <div className="text-center text-white">
            <h1 className="text-6xl font-bold mb-4">MANGO</h1>
            <p className="text-orange-100 text-lg">
              Mindwave Analysis for Neurofeedback & Graphical Observation
            </p>
          </div>
        </div>

        {/* Coluna direita - Formulário */}
        <div className="w-full lg:w-1/2 p-8 lg:p-12">
          <div className="text-center mb-8">
            <div className="lg:hidden mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-full flex items-center justify-center mx-auto border border-orange-200 dark:border-orange-800/30">
                <span className="text-2xl font-bold text-orange-600 dark:text-orange-400">M</span>
              </div>
              <h1 className="text-3xl font-bold mt-2 text-gray-900 dark:text-white">MANGO</h1>
            </div>

            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Acessar Plataforma
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Entre com suas credenciais para acessar o sistema
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email
              </label>
              <input
                type="email"
                name="email"
                placeholder="seu.email@instituicao.com"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Senha
              </label>
              <input
                type="password"
                name="password"
                placeholder="Sua senha"
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                required
              />
            </div>

            <div className="flex justify-between items-center">
              <Link
                href="/scientist/forgot-password"
                className="text-sm text-orange-600 dark:text-orange-400 hover:text-orange-800 dark:hover:text-orange-300 transition-colors duration-200"
              >
                Esqueci minha senha
              </Link>
            </div>

            {error && <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>}

            <button
              type="submit"
              disabled={!isFormValid || isSubmitting}
              className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 flex items-center justify-center ${
                isFormValid && !isSubmitting
                  ? 'bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                  : 'bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
              }`}
            >
              {isSubmitting ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
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
                  Entrando...
                </>
              ) : (
                'Entrar'
              )}
            </button>

            <div className="text-center pt-4 border-t border-orange-100 dark:border-orange-900/30">
              <p className="text-gray-600 dark:text-gray-400">
                Não possui uma conta?{' '}
                <Link
                  href="/scientist/register"
                  className="text-orange-600 dark:text-orange-400 hover:text-orange-800 dark:hover:text-orange-300 font-medium transition-colors duration-200"
                >
                  Criar conta
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
