// lib/sessions/listSessions.js
export const listSessions = async () => {
  try {
    const response = await fetch('/bff/sessions', {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || error.detail || 'Erro ao buscar sessões')
    }

    const data = await response.json()

    return Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Erro ao buscar sessões:', err)
    throw err
  }
}
