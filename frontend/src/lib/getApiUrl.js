// lib/getApiUrl.js
export const getApiUrl = () => {
  const port = process.env.NEXT_PUBLIC_RESTAPI_PORT || 8002

  // se estiver definido manualmente no .env, usa ele
  if (process.env.NEXT_PUBLIC_RESTAPI_URL && process.env.NEXT_PUBLIC_RESTAPI_URL !== 'auto') {
    return process.env.NEXT_PUBLIC_RESTAPI_URL
  }

  // server-side
  if (typeof window === 'undefined') {
    // dentro do Docker, o container do frontend se comunica com o container da REST API pelo nome do serviço do docker-compose
    return `https://localhost/restapi`
  } else {
    // client-side, rodando no browser
    return `https://localhost/restapi`
  }
}
