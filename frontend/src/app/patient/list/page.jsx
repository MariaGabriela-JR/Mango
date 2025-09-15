'use client'

import { useEffect, useState } from 'react'
import { listPatients } from '@/lib/listPatients'
import Navbar from '@/components/ui/Navbar'
import Link from 'next/link'

export default function PatientsList() {
  const [patients, setPatients] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('accessToken')
    const id = localStorage.getItem('id')

    if (!token || !id) {
      setError('Usuário não autenticado')
      setLoading(false)
      return
    }

    listPatients(id, token)
      .then((data) => setPatients(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <Navbar />
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Lista de Pacientes</h1>
        {loading && <p className="text-gray-500">Carregando...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {!loading && !error && (
          <>
            {patients.length === 0 ? (
              <p className="text-gray-600">Nenhum paciente encontrado.</p>
            ) : (
              <ul className="space-y-2">
                {patients.map((p) => (
                  <li key={p.id} className="border p-2 rounded">
                    {p.first_name} {p.last_name}
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
        <div className="flex gap-4 mt-6">
          <Link href="/dashboard">
            <button className="md:w-32 md:h-12 w-28 bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-lg text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
              Voltar
            </button>
          </Link>
          <Link href="/patient/add">
            <button className="md:w-32 md:h-12 w-28 bg-[#1a1b1c] dark:bg-white font-sans font-bold rounded-lg text-white dark:text-black hover:bg-black dark:hover:bg-gray-300 transition-colors duration-300">
              Novo Paciente
            </button>
          </Link>
        </div>
      </div>
    </div>
  )
}
