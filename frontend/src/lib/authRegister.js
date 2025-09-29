const authRegister = async (email, password, firstName, lastName, institution, specialization) => {
  const response = await fetch('/bff/scientist/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, firstName, lastName, institution, specialization }),
  })

  const result = await response.json()

  if (!response.ok) {
    const errorMessage = result.message || result.detail
    throw new Error(errorMessage)
  }
  if (result.registration_token) {
    localStorage.setItem('registrationToken', result.registration_token)
  }

  return result
}

export default authRegister
