'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import authRegister from '@/lib/authRegister'

export default function RegisterPage() {
  const router = useRouter()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [institution, setInstitution] = useState('')
  const [specialization, setSpecialization] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const result = await authRegister(
        email,
        password,
        firstName,
        lastName,
        institution,
        specialization,
      )

      // Redireciona para página de sucesso passando a mensagem do backend
      router.push(`/scientist/register/success?message=${encodeURIComponent(result.message)}`)
    } catch (err) {
      // Mostra a mensagem de erro exata retornada pelo backend
      setError(err.message)
    }
  }

  const isFormValid = email && password && firstName && lastName && institution && specialization

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
          <h2 className="text-2xl font-bold mb-6 text-center">
            Olá, cientista! <br />
            Crie agora mesmo sua conta!
          </h2>

          <label className="block mb-2 font-medium">Nome</label>
          <input
            type="text"
            placeholder="Digite seu nome"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />

          <label className="block mb-2 font-medium">Sobrenome</label>
          <input
            type="text"
            placeholder="Digite seu sobrenome"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />

          <label className="block mb-2 font-medium">Email</label>
          <input
            type="email"
            placeholder="Digite seu email"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label className="block mb-2 font-medium">Senha</label>
          <input
            type="password"
            placeholder="Digite sua senha"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <label className="block mb-2 font-medium">Instituição</label>
          <input
            type="text"
            placeholder="Digite sua instituição"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={institution}
            onChange={(e) => setInstitution(e.target.value)}
          />

          <label className="block mb-2 font-medium">Especialização</label>
          <input
            type="text"
            placeholder="Digite sua especialização"
            className="w-full mb-4 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={specialization}
            onChange={(e) => setSpecialization(e.target.value)}
          />

          {error && <p className="text-red-500 mb-2">{error}</p>}

          <button
            type="submit"
            className={`w-full py-3 text-white font-bold rounded-md transition-colors ${
              isFormValid ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'
            }`}
            disabled={!isFormValid}
          >
            Criar Conta
          </button>

          <p className="mt-4 text-center">
            Já tem uma conta?{' '}
            <Link href="/scientist/login" className="text-blue-600 hover:underline">
              Fazer login
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}
