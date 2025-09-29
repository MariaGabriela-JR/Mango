// app/bff/scientist/me/route.js
import { NextResponse } from 'next/server'
import axios from 'axios'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function GET(req) {
  try {
    const accessToken = req.cookies.get('accessToken')?.value
    if (!accessToken) {
      return NextResponse.json({ success: false, message: 'Não autenticado' }, { status: 401 })
    }
    const response = await axios.get(`${getGatewayUrl()}/scientists/profile`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })

    return NextResponse.json({ success: true, data: response.data.scientist })
  } catch (err) {
    console.error('Erro ao acessar', err.response?.data || err.detail || err.message)
    return NextResponse.json(
      { success: false, message: err.response?.data?.detail || 'Erro ao buscar perfil' },
      { status: err.response?.status || 500 },
    )
  }
}
