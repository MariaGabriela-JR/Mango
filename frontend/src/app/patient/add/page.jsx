<<<<<<< HEAD
<<<<<<< HEAD
=======
// app/register/patient/page.jsx
>>>>>>> 4b1e246 (feat: implementação das funções básicas de patients)
=======
>>>>>>> 5a4d937 (fix: função para voltar para telas anteriores)
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
<<<<<<< HEAD
<<<<<<< HEAD
import Link from 'next/link'
=======
>>>>>>> 4b1e246 (feat: implementação das funções básicas de patients)
=======
import Link from 'next/link'
>>>>>>> 5a4d937 (fix: função para voltar para telas anteriores)
import addPatient from '@/lib/addPatient'
import Navbar from '@/components/ui/Navbar'

export default function PatientRegisterPage() {
  const router = useRouter()
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const result = await addPatient(email, password, firstName, lastName)
      router.push(`/patient/add/success?message=${encodeURIComponent(result.message)}`)
    } catch (err) {
      setError(err.message)
    }
  }

  const isFormValid = firstName && lastName && email && password

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#121212] flex flex-col">
      <Navbar />
      <div className="flex items-center justify-center flex-1">
        <form
          className="w-full max-w-lg bg-white dark:bg-[#1a1b1c] p-10 rounded-lg shadow-lg"
          onSubmit={handleSubmit}
        >
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5a4d937 (fix: função para voltar para telas anteriores)
          <Link
            href="/dashboard"
            className="flex w-auto h-auto items-center mb-4 text-blue-600 hover:text-blue-800 cursor-pointer"
          >
            <span className="mr-2 text-2xl"></span> Voltar
          </Link>

<<<<<<< HEAD
=======
>>>>>>> 4b1e246 (feat: implementação das funções básicas de patients)
=======
>>>>>>> 5a4d937 (fix: função para voltar para telas anteriores)
          <h1 className="text-4xl font-bold mb-6 text-center text-gray-800 dark:text-gray-200">
            Registro de Paciente
          </h1>

          <input
            type="text"
            placeholder="Nome"
            className="w-full mb-4 px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />

          <input
            type="text"
            placeholder="Sobrenome"
            className="w-full mb-4 px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />

          <input
            type="email"
            placeholder="Email"
            className="w-full mb-4 px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Senha"
            className="w-full mb-6 px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && <p className="text-red-500 mb-4">{error}</p>}

          <button
            type="submit"
            disabled={!isFormValid}
            className={`w-full py-3 text-white font-bold rounded-md transition-colors ${
              isFormValid ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'
            }`}
          >
            Registrar Paciente
          </button>
        </form>
      </div>
    </div>
  )
}
