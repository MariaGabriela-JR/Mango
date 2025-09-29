export const authLogin = async (email, password) => {
  const response = await fetch('/bff/scientist/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
    credentials: 'include',
  })

  const result = await response.json()
  if (!response.ok) {
    const errorMessage = result.message || result.detail || 'Falha no login'
    throw new Error(errorMessage)
  }

  return result
}

export const authLogout = async () => {
  await fetch('/bff/scientist/logout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  })
}
