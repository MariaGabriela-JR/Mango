// lib/sessions/discoverEdfFiles.js
export async function discoverEdfFiles() {
  try {
    const res = await fetch('/bff/sessions/new/selectFile', {
      method: 'GET',
      credentials: 'include', // garante que cookies (accessToken) sejam enviados
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.message || 'Erro ao buscar arquivos EDF')
    }

    // garante que o retorno seja sempre um array
    return Array.isArray(data.files) ? data.files : [data.files]
  } catch (error) {
    throw new Error(error.message)
  }
}
