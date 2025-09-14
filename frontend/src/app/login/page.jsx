'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'

export default function LoginPage() {
  const { login, redirectIfLogged, isLoading } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  // Redireciona para dashboard caso já esteja logado
  useEffect(() => {
    redirectIfLogged('/dashboard')
  }, [redirectIfLogged])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('') // limpa mensagens anteriores

    try {
      await login(email, password)
      // login com sucesso redireciona automaticamente via hook
    } catch (err) {
      console.error(err)
      setError(err.response?.data?.detail || 'Login falhou. Verifique nome de usuário e senha.')
    }
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p>Carregando...</p>
      </div>
    )
  }

  return (
    <div className="flex h-screen">
      {/* Coluna esquerda */}
      <div className="w-1/2 flex items-center justify-center bg-white dark:bg-[#1a1b1c]">
        <h1 className="text-7xl font-bold font-sans">MANGO</h1>
      </div>

      {/* Coluna direita */}
      <div className="w-1/2 flex items-center justify-center bg-gray-100 dark:bg-[#121212]">
        <form
          className="w-4/5 max-w-md bg-white dark:bg-[#1a1b1c] p-8 rounded-lg shadow-md"
          onSubmit={handleSubmit}
        >
          <h2 className="text-3xl font-bold mb-4">Login</h2>

          {error && <p className="text-red-500 mb-2">{error}</p>}

          <label className="block mb-2 font-medium">Email</label>
          <input
            type="email"
            name="email"
            placeholder="Digite seu email"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label className="block mb-2 font-medium">Senha</label>
          <input
            type="password"
            name="password"
            placeholder="Digite sua senha"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Link href="/login" className="block mb-5 text-end font-medium">
            Esqueci minha senha
          </Link>

          <button
            type="submit"
            className="w-full py-3 bg-blue-600 text-white font-bold rounded-md hover:bg-blue-700 transition-colors"
          >
            Entrar
          </button>
          <p className="mt-4 text-center">
            Não possui uma conta?{' '}
              <Link href="/login" className="text-blue-600 hover:underline">
                Criar conta
              </Link>
          </p>
        </form>
      </div>
    </div>
  )
}
