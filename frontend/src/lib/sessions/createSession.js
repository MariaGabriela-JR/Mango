// lib/sessions/createSession.js - VERSÃO CORRIGIDA
import axios from 'axios'

export async function createSession(sessionData) {
  try {
    // Mapear os campos do frontend para os nomes que o BFF espera
    const payload = {
      sessionName: sessionData.sessionName,
      edfFile: sessionData.edfFile,
      patientId: sessionData.patientId,
    }

    console.log('Enviando para BFF:', payload) // Debug

    const response = await axios.post('/bff/sessions/new', payload)

    return response.data
  } catch (error) {
    console.error('Erro no createSession:', error.response?.data)
    throw new Error(error.response?.data?.message || 'Erro ao criar sessão')
  }
}
