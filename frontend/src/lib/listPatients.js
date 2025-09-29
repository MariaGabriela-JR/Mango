// lib/listPatients.js
export const listPatients = async () => {
  try {
    const response = await fetch('/bff/patients/list', {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || error.detail || 'Erro ao buscar pacientes')
    }

    const data = await response.json()
    return data.patients || []
  } catch (err) {
    console.error('Erro ao buscar pacientes:', err)
    throw err
  }
}
