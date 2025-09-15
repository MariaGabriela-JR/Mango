import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { authLogin, authLogout } from '@/lib/authLogin'

export const useAuth = () => {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  // validação simples do JWT
  const checkToken = useCallback(() => {
    if (typeof window === 'undefined') return false
    const token = localStorage.getItem('accessToken')
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
      const token = localStorage.getItem('accessToken')
      const payload = JSON.parse(atob(token.split('.')[1]))
      setUser(payload)
    } else {
      setUser(null)
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    }
    setIsLoading(false)
  }, [checkToken])

  const login = async (email, password) => {
    const { access } = await authLogin(email, password)
    const payload = JSON.parse(atob(access.split('.')[1]))
    setUser(payload)
    return payload
  }

  const logout = async () => {
    await authLogout()
    setUser(null)
    router.replace('/scientist/login')
  }

  const requireAuth = (redirectTo = '/scientist/login') => {
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
