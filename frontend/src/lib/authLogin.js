import axios from 'axios'
import { getApiUrl } from '@/lib/getApiUrl'

export const authLogin = async (email, password) => {
  try {
    const params = new URLSearchParams()
    params.append('email', email)
    params.append('password', password)

    const response = await axios.post(`${getApiUrl()}/auth/login/scientists/`, params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const { access, refresh, id } = response.data

    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)

    if (id) {
      localStorage.setItem('id', id)
    }

    return { access, refresh, id }
  } catch (err) {
    console.error('Erro no login:', err.response?.data || err.message)
    throw err
  }
}

export const authLogout = async () => {
  try {
    const refreshToken = localStorage.getItem('refreshToken')

    if (refreshToken) {
      await axios.post(`${getApiUrl()}/auth/logout/`, { refresh: refreshToken })
    }
  } catch (err) {
    console.error('Erro no logout:', err.response?.data || err.message)
  } finally {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('id')
  }
}
