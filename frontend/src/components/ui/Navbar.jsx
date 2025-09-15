'use client'

import { useState, useRef, useEffect } from 'react'
import { useAuth } from '@/hooks/useAuth'
import Link from "next/link"

export default function Navbar() {
  const { user, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false)
      }
    }
    if (menuOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [menuOpen])

  return (
    <nav className="w-full flex items-center justify-between p-4 bg-gray-100 dark:bg-[#101111]">
      <div className="text-3xl font-bold font-sans">MANGO</div>

      <div className="relative" ref={menuRef}>
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="flex flex-col justify-between w-6 h-5 focus:outline-none"
        >
          <span className="block h-0.5 w-full bg-black dark:bg-white rounded"></span>
          <span className="block h-0.5 w-full bg-black dark:bg-white rounded"></span>
          <span className="block h-0.5 w-full bg-black dark:bg-white rounded"></span>
        </button>

        {menuOpen && (
          <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-[#1a1b1c] border border-gray-300 dark:border-gray-700 rounded shadow-lg z-10">
            <ul className="flex flex-col">
              <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                <Link href="/">Home</Link>
              </li>
              <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                <Link href="/patient/list">Pacientes</Link>
              </li>
              <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                Sessões
              </li>
              <li className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer">
                Perfil
              </li>
              <li
                className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer"
                onClick={logout}
              >
                Sair
              </li>
            </ul>
          </div>
        )}
      </div>
    </nav>
  )
}
