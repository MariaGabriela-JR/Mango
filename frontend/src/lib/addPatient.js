const addPatient = async (firstName, lastName, cpf, birthDate, password, gender) => {
  const response = await fetch('/bff/patients/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ firstName, lastName, cpf, birthDate, password, gender }),
    credentials: 'include',
  })

  const result = await response.json()
  if (!response.ok) {
    const errorMessage = result.message || result.detail || 'Erro ao registrar paciente'
    throw new Error(errorMessage)
  }

  return result
}

export default addPatient
