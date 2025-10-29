// lib/updateScientist.js
export const updateScientist = async (formDataObj) => {
  try {
    // Debug: Check the value before sending
    console.log('Profile Picture File:', formDataObj.profilePicture)
    console.log('File type:', typeof formDataObj.profilePicture)

    const formData = new FormData()
    Object.entries(formDataObj).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'profilePicture') {
          formData.append('profile_picture', value)
        } else {
          formData.append(key, value)
        }
      }
    })

    // Debug: Check what's in FormData
    for (let [key, value] of formData.entries()) {
      console.log(key, value)
    }

    const response = await fetch('/bff/scientist/update', {
      method: 'PATCH',
      body: formData,
      credentials: 'include',
    })

    const result = await response.json()

    if (!response.ok || !result.success) {
      throw new Error(result.message || 'Erro ao atualizar perfil')
    }

    return result.data
  } catch (err) {
    console.error('Erro updateScientist:', err)
    throw err
  }
}
