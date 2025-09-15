// lib/addPatient.js
import axios from 'axios'
import { getApiUrl } from '@/lib/getApiUrl'

const addPatient = async (email, password, firstName, lastName) => {
  try {
    const id = localStorage.getItem('id')
    if (!id) throw new Error('Scientist ID não encontrado')

    const data = {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
      scientist: id,
    }

    const response = await axios.post(`${getApiUrl()}/patients/register/`, data, {
      headers: { 'Content-Type': 'application/json' },
    })

    return { success: true, message: response.data.message || 'Paciente criado com sucesso!' }
  } catch (err) {
    let message = 'Erro ao registrar'

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

    throw new Error(message)
  }
}

export default addPatient
