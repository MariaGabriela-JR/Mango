// app/bff/sessions/show/[fileID]/route.js
import { NextResponse } from 'next/server'
import axios from 'axios'
import { cookies } from 'next/headers'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function GET(req, { params }) {
  try {
    const { fileID } = params
    const cookieStore = cookies()
    const token = cookieStore.get('accessToken')?.value

    if (!token) {
      return NextResponse.json({ message: 'Token de autenticação não encontrado' }, { status: 401 })
    }

    const backendRes = await axios.get(`${getGatewayUrl()}/edf_files/edf-files/${fileID}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return NextResponse.json(backendRes.data)
  } catch (err) {
    console.error('Erro no BFF showSession:', err.response?.data || err.message)

    return NextResponse.json(
      { message: err.response?.data?.detail || 'Erro interno no BFF' },
      { status: err.response?.status || 500 },
    )
  }
}
