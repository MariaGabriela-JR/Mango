// lib/fetchProfile.js
export const fetchProfile = async () => {
  try {
    const response = await fetch('/bff/scientist/me', {
      method: 'GET',
      credentials: 'include',
    })

    const result = await response.json()

    if (!response.ok || !result.success) {
      throw new Error(result.detail || 'Erro ao buscar perfil')
    }

    return result.data
  } catch (err) {
    console.error('Erro fetchProfile:', err.detail)
    throw err
  }
}
