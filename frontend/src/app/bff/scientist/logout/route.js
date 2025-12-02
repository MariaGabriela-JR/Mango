import { NextResponse } from 'next/server'
import axios from 'axios'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function POST(req) {
  try {
    const refreshToken = req.cookies.get('refreshToken')?.value

    if (refreshToken) {
      await axios.post(
        `${getGatewayUrl()}/scientists/logout`,
        { refresh: refreshToken },
        {
          headers: {
            Authorization: `Bearer ${req.cookies.get('accessToken')?.value}`,
          },
        },
      )
    }

    // resposta com cookies limpos
    const res = NextResponse.json({
      success: true,
      message: 'Logout realizado com sucesso',
    })

    res.cookies.delete('accessToken')
    res.cookies.delete('refreshToken')

    return res
  } catch (err) {
    console.error('Erro no logout:', err.response?.data || err.message)
    const message = err.response?.data?.detail || 'Falha no logout'
    return NextResponse.json({ success: false, message }, { status: 400 })
  }
}
