import axios from 'axios'
import { getApiUrl } from '@/lib/getApiUrl'

export const listPatients = async (id) => {
  try {
    const token = localStorage.getItem('accessToken')
    if (!token) throw new Error('Token de autenticação não encontrado')

    const response = await axios.get(`${getApiUrl()}/patients/list/`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'X-Scientist-ID': id,
      },
    })

    return response.data
  } catch (err) {
    console.error('Erro ao buscar pacientes:', err.response?.data || err.message)
    throw err
  }
}
