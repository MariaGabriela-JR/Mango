// lib/getGatewayUrl.js
export const getGatewayUrl = () => {
  const envUrl = process.env.NEXT_PUBLIC_URL
  const port = process.env.NEXT_PUBLIC_GATEWAY_PORT || 8080

  // se definido manualmente no .env (e não for "auto"), usa direto
  if (envUrl && envUrl !== 'auto') {
    return envUrl
  }

  // server-side (SSR rodando dentro do container)
  if (typeof window === 'undefined') {
    return `http://gateway:${port}/api`
  }

  // client-side (navegador, passando pelo nginx)
  return `https://localhost/api`
}
