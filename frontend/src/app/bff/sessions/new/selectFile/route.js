import { NextResponse } from 'next/server'
import axios from 'axios'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function GET(req) {
  try {
    const accessToken = req.cookies.get('accessToken')?.value
    if (!accessToken) {
      return NextResponse.json({ success: false, message: 'Não autenticado' }, { status: 401 })
    }

    const response = await axios.get(`${getGatewayUrl()}/filters/discover`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })

    return NextResponse.json({ success: true, files: response.data })
  } catch (err) {
    return NextResponse.json(
      { success: false, message: err.response?.data?.detail || 'Erro ao buscar arquivos' },
      { status: err.response?.status || 500 },
    )
  }
}
