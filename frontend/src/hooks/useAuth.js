import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export const useAuth = () => {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkSession = async () => {
      try {
        const res = await fetch('/bff/scientist/auth')
        const data = await res.json()
        if (data.isLoggedIn) {
          setUser(data.user)
        } else {
          setUser(null)
        }
      } catch {
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }
    checkSession()
  }, [])

  const login = async (email, password) => {
    const res = await fetch('/bff/scientist/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    if (!res.ok) throw new Error('Falha no login')

    const data = await res.json()
    setUser({ id: data.id }) // payload simplificado
    return data
  }

  const logout = async () => {
    await fetch('/bff/scientist/logout', { method: 'POST' })
    setUser(null)
    router.replace('/scientist/login')
  }

  const requireAuth = (redirectTo = '/scientist/login') => {
    if (!user && !isLoading) {
      router.replace(redirectTo)
    }
  }

  const redirectIfLogged = (redirectTo = '/dashboard') => {
    if (user && !isLoading) {
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
