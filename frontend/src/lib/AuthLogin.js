import axios from 'axios'
import { getApiUrl } from '@/lib/getApiUrl'

const AuthLogin = async (email, password) => {
  try {
    const params = new URLSearchParams()
    params.append('email', email)
    params.append('password', password)

    const response = await axios.post(`${getApiUrl()}/auth/login/scientist/`, params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const token = response.data.access
    console.log('JWT recebido:', token)
    return token
  } catch (err) {
    console.error('Erro no login:', err.response?.data || err.message)
    throw err
  }
}

export default AuthLogin
