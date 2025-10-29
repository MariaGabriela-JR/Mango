// lib/fetchProfile.js
export const fetchProfile = async () => {
  try {
    const response = await fetch('/bff/scientist/me', {
      method: 'GET',
      credentials: 'include',
    })

    const result = await response.json()

    if (!response.ok || !result.success) {
      throw new Error(result.message || 'Erro ao buscar perfil')
    }

    const data = result.data

    return {
      ...data,
      profilePicture: data.profilePicture || data.profile_picture || null,
    }
  } catch (err) {
    console.error('Erro fetchProfile:', err)
    throw err
  }
}
