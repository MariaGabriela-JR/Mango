import axios from 'axios'
import { getApiUrl } from '@/lib/getApiUrl'

const authRegister = async (email, password, firstName, lastName, institution, specialization) => {
  try {
    const data = {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
      institution,
      specialization,
    }

    const response = await axios.post(`${getApiUrl()}/scientists/register/`, data, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const { registration_token } = response.data

    localStorage.setItem('registrationToken', registration_token)

    // retorna a mensagem do backend em caso de sucesso
    return { success: true, message: response.data.message || 'Conta criada com sucesso!' }
  } catch (err) {
    let message = 'Erro ao registrar'

    // Extrai mensagem de erro do backend, se disponível
    if (err.response?.data) {
      const data = err.response.data
      const messages = []
      for (const key in data) {
        if (Array.isArray(data[key])) {
          messages.push(`${data[key].join(', ')}`)
        } else {
          messages.push(`${data[key]}`)
        }
      }
      message = messages.join(' | ')
    } else if (err.message) {
      message = err.message
    }

    // lança o erro com a mensagem do backend
    throw new Error(message)
  }
}

export default authRegister
