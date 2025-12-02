// app/bff/scientist/update/route.js
import { NextResponse } from 'next/server'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function PATCH(req) {
  try {
    const accessToken = req.cookies.get('accessToken')?.value
    if (!accessToken) {
      return NextResponse.json({ success: false, message: 'Não autenticado' }, { status: 401 })
    }

    const formData = await req.formData()

    // DEBUG: Verifique o que está chegando na rota
    console.log('=== DEBUG FORM DATA ===')
    for (const [key, value] of formData.entries()) {
      if (value instanceof File) {
        console.log(
          `File field: ${key}, size: ${value.size}, type: ${value.type}, name: ${value.name}`,
        )
      } else {
        console.log(`Field: ${key}, value: ${value}`)
      }
    }
    console.log('=== FIM DEBUG ===')

    const gatewayResponse = await fetch(`${getGatewayUrl()}/scientists/update`, {
      method: 'PATCH',
      body: formData,
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })

    const result = await gatewayResponse.json()

    // DEBUG: Verifique a resposta do gateway
    console.log('=== DEBUG GATEWAY RESPONSE ===')
    console.log('Status:', gatewayResponse.status)
    console.log('Response data:', JSON.stringify(result, null, 2))
    console.log('=== FIM DEBUG ===')

    if (!gatewayResponse.ok) {
      throw new Error(result.detail || `Erro do gateway: ${gatewayResponse.status}`)
    }

    return NextResponse.json({
      success: true,
      data: result.scientist,
    })
  } catch (err) {
    console.error('Erro ao atualizar cientista:', err.message)
    return NextResponse.json(
      {
        success: false,
        message: err.message || 'Erro ao atualizar perfil',
      },
      { status: 500 },
    )
  }
}
