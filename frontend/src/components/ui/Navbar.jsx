'use client'

import { useState, useRef, useEffect } from 'react'
import { useAuth } from '@/hooks/useAuth'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { fetchProfile } from '@/lib/fetchProfile'

export default function Navbar() {
  const { user, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const [profileMenuOpen, setProfileMenuOpen] = useState(false)
  const [scientistProfile, setScientistProfile] = useState(null)
  const [profileLoading, setProfileLoading] = useState(false)
  const menuRef = useRef(null)
  const profileMenuRef = useRef(null)
  const pathname = usePathname()

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
        // Se houver erro, mantemos os dados básicos do user
      } finally {
        setProfileLoading(false)
      }
    }

    loadScientistProfile()
  }, [user])

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false)
      }
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setProfileMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const isActiveLink = (path) => {
    return pathname === path
      ? 'text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/20'
      : 'text-gray-700 dark:text-gray-300 hover:text-orange-600 dark:hover:text-orange-400'
  }

  const handleLogout = () => {
    logout()
    setProfileMenuOpen(false)
  }

  // Função para obter as iniciais do nome
  const getInitials = () => {
    if (scientistProfile?.first_name && scientistProfile?.last_name) {
      return `${scientistProfile.first_name[0]}${scientistProfile.last_name[0]}`
    }
    if (user?.firstName && user?.lastName) {
      return `${user.firstName[0]}${user.lastName[0]}`
    }
    if (user?.name) {
      return user.name[0]
    }
    return 'U'
  }

  // Função para obter o nome completo
  const getFullName = () => {
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

  // Função para obter o email
  const getEmail = () => {
    return scientistProfile?.email || user?.email || ''
  }

  // Função para obter a foto de perfil
  const getProfilePicture = () => {
  if (!scientistProfile?.profilePicture) return null

  return scientistProfile.profilePicture.replace(
    'http://restapi:8000',
    'https://localhost/'
  )
}

  // Componente para renderizar o avatar
  const Avatar = ({ size = 8, className = '' }) => {
    const profilePicture = getProfilePicture()

    if (profileLoading) {
      return (
        <div
          className={`w-${size} h-${size} border-2 border-orange-600 border-t-transparent rounded-full animate-spin ${className}`}
        ></div>
      )
    }

    if (profilePicture) {
      return (
        <img
          src={profilePicture}
          alt="Foto de perfil"
          className={`w-${size} h-${size} rounded-full object-cover border border-orange-200 dark:border-orange-800/30 ${className}`}
        />
      )
    }

    return (
      <div
        className={`w-${size} h-${size} bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-full flex items-center justify-center border border-orange-200 dark:border-orange-800/30 ${className}`}
      >
        <span className="text-orange-600 dark:text-orange-400 font-medium text-sm">
          {getInitials()}
        </span>
      </div>
    )
  }

  return (
    <nav className="w-full bg-white dark:bg-[#101111] border-b border-orange-100 dark:border-orange-900/30 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/dashboard" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-orange-500 to-amber-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">M</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">
              MANGO
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              href="/dashboard"
              className={`px-3 py-2 rounded-lg font-medium transition-all duration-200 ${isActiveLink('/dashboard')}`}
            >
              Dashboard
            </Link>
            <Link
              href="/patients/list"
              className={`px-3 py-2 rounded-lg font-medium transition-all duration-200 ${isActiveLink('/patients/list')}`}
            >
              Pacientes
            </Link>
            <Link
              href="/sessions/list"
              className={`px-3 py-2 rounded-lg font-medium transition-all duration-200 ${isActiveLink('/sessions/list')}`}
            >
              Sessões
            </Link>
          </div>

          {/* Right Section - Desktop */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Profile Menu */}
            <div className="relative" ref={profileMenuRef}>
              <button
                onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors duration-200"
              >
                <Avatar size={8} />
                <span className="text-gray-700 dark:text-gray-300 font-medium">
                  {profileLoading ? 'Carregando...' : getFullName()}
                </span>
                <svg
                  className={`w-4 h-4 text-gray-500 transition-transform duration-200 ${profileMenuOpen ? 'rotate-180' : ''}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>

              {profileMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-[#1e1e1e] border border-orange-100 dark:border-orange-900/30 rounded-lg shadow-lg z-20">
                  <div className="p-3 border-b border-orange-50 dark:border-orange-900/20">
                    <div className="flex items-center space-x-2 mb-2">
                      <Avatar size={8} />
                      <div>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {getFullName()}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                          {getEmail()}
                        </p>
                      </div>
                    </div>
                    {scientistProfile?.institution && (
                      <p className="text-xs text-gray-400 dark:text-gray-500 truncate">
                        {scientistProfile.institution}
                      </p>
                    )}
                  </div>
                  <ul className="py-1">
                    <li>
                      <Link
                        href="/scientist/me"
                        className="flex items-center px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors duration-200"
                        onClick={() => setProfileMenuOpen(false)}
                      >
                        <svg
                          className="w-4 h-4 mr-2"
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
                        Meu Perfil
                      </Link>
                    </li>
                    <li>
                      <button
                        onClick={handleLogout}
                        className="flex items-center w-full px-3 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200"
                      >
                        <svg
                          className="w-4 h-4 mr-2"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                          />
                        </svg>
                        Sair
                      </button>
                    </li>
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden" ref={menuRef}>
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="p-2 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors duration-200"
            >
              <div className="flex flex-col justify-between w-6 h-5">
                <span
                  className={`block h-0.5 w-full bg-gray-700 dark:bg-gray-300 rounded transition-all duration-200 ${menuOpen ? 'rotate-45 translate-y-2' : ''}`}
                ></span>
                <span
                  className={`block h-0.5 w-full bg-gray-700 dark:bg-gray-300 rounded transition-all duration-200 ${menuOpen ? 'opacity-0' : ''}`}
                ></span>
                <span
                  className={`block h-0.5 w-full bg-gray-700 dark:bg-gray-300 rounded transition-all duration-200 ${menuOpen ? '-rotate-45 -translate-y-2' : ''}`}
                ></span>
              </div>
            </button>

            {menuOpen && (
              <div className="absolute right-4 mt-2 w-64 bg-white dark:bg-[#1e1e1e] border border-orange-100 dark:border-orange-900/30 rounded-lg shadow-lg z-20">
                {/* User Info */}
                <div className="p-4 border-b border-orange-50 dark:border-orange-900/20">
                  <div className="flex items-center space-x-3">
                    <Avatar size={10} />
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {profileLoading ? 'Carregando...' : getFullName()}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{getEmail()}</p>
                      {scientistProfile?.institution && (
                        <p className="text-xs text-gray-400 dark:text-gray-500 truncate mt-1">
                          {scientistProfile.institution}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Navigation Links */}
                <ul className="py-2">
                  <li>
                    <Link
                      href="/dashboard"
                      className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 transition-colors duration-200 ${isActiveLink('/dashboard')}`}
                      onClick={() => setMenuOpen(false)}
                    >
                      <svg
                        className="w-5 h-5 mr-3"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                        />
                      </svg>
                      Dashboard
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/patients/list"
                      className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 transition-colors duration-200 ${isActiveLink('/patients/list')}`}
                      onClick={() => setMenuOpen(false)}
                    >
                      <svg
                        className="w-5 h-5 mr-3"
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
                      Pacientes
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/sessions/list"
                      className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 transition-colors duration-200 ${isActiveLink('/sessions/list')}`}
                      onClick={() => setMenuOpen(false)}
                    >
                      <svg
                        className="w-5 h-5 mr-3"
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
                      Sessões
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/scientist/me"
                      className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 transition-colors duration-200 ${isActiveLink('/scientist/me')}`}
                      onClick={() => setMenuOpen(false)}
                    >
                      <svg
                        className="w-5 h-5 mr-3"
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
                      Meu Perfil
                    </Link>
                  </li>
                </ul>

                {/* Logout Button */}
                <div className="p-4 border-t border-orange-50 dark:border-orange-900/20">
                  <button
                    onClick={handleLogout}
                    className="flex items-center justify-center w-full px-4 py-2 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-800 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200"
                  >
                    <svg
                      className="w-5 h-5 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                      />
                    </svg>
                    Sair
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
