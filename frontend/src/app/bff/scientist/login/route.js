import { NextResponse } from 'next/server'
import axios from 'axios'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function POST(req) {
  try {
    const { email, password } = await req.json()

    const response = await axios.post(
      `${getGatewayUrl()}/scientists/login`,
      { email, password },
      {
        headers: { 'Content-Type': 'application/json' },
      },
    )

    const { access_token, refresh_token, scientist } = response.data
    const scientistId = scientist?.id

    const res = NextResponse.json({ success: true })

    // Cookies httpOnly
    res.cookies.set('accessToken', access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 60 * 10, // 15 (2 para testes) min
    })

    res.cookies.set('refreshToken', refresh_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 60 * 60 * 24 * 7, // 7 dias
    })

    res.cookies.set('scientistId', scientistId, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 60 * 60 * 24 * 7,
    })

    return res
  } catch (err) {
    const message = err.response?.data?.detail || 'Falha no login'
    return NextResponse.json({ success: false, message }, { status: 401 })
  }
}
