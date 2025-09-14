import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import AuthLogin from '@/lib/AuthLogin'

export const useAuth = () => {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  const checkToken = useCallback(() => {
    if (typeof window === 'undefined') return false
    const token = localStorage.getItem('token')
    if (!token) return false

    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp * 1000 > Date.now()
    } catch {
      return false
    }
  }, [])

  useEffect(() => {
    const valid = checkToken()
    if (valid) {
      const token = localStorage.getItem('token')
      const payload = JSON.parse(atob(token.split('.')[1]))
      setUser(payload)
    } else {
      setUser(null)
      localStorage.removeItem('token')
    }
    setIsLoading(false)
  }, [checkToken])

  const login = async (email, password) => {
    const token = await AuthLogin(email, password)
    localStorage.setItem('token', token)

    const payload = JSON.parse(atob(token.split('.')[1]))
    setUser(payload)
    return payload
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
    router.replace('/login')
  }

  const requireAuth = (redirectTo = '/login') => {
    if (!checkToken()) {
      router.replace(redirectTo)
    }
  }

  const redirectIfLogged = (redirectTo = '/dashboard') => {
    if (checkToken()) {
      router.replace(redirectTo)
    }
  }

  return {
    user,
    isLoading,
    login,
    logout,
    requireAuth,
    redirectIfLogged,
    isLoggedIn: !!user,
  }
}
