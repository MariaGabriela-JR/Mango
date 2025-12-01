// lib/sessions/showSession.js
import axios from 'axios'

export async function showSession(fileID) {
  try {
    const res = await axios.get(`/bff/sessions/show/${fileID}`, {
      withCredentials: true,
    })

    return res.data
  } catch (err) {
    console.error('Erro na lib showSession:', err.response?.data || err)
    throw new Error(err.response?.data?.message || 'Erro ao buscar sessão')
  }
}
