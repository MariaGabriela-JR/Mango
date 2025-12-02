import { NextResponse } from 'next/server'
import axios from 'axios'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function POST(req) {
  try {
    const { firstName, lastName, cpf, birthDate, password, gender } = await req.json()

    // Pega cookies no servidor
    const token = req.cookies.get('accessToken')?.value
    const scientistId = req.cookies.get('scientistId')?.value

    if (!token) {
      return NextResponse.json(
        { success: false, message: 'Usuário não autenticado' },
        { status: 401 },
      )
    }
    if (!scientistId) {
      return NextResponse.json(
        { success: false, message: 'Scientist ID não encontrado' },
        { status: 400 },
      )
    }

    const data = {
      cpf,
      password,
      first_name: firstName,
      last_name: lastName,
      birth_date: birthDate,
      gender,
      scientist: scientistId,
    }

    const response = await axios.post(`${getGatewayUrl()}/patients/register`, data, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    })

    return NextResponse.json({
      success: true,
      message: response.data.message || 'Paciente criado com sucesso!',
    })
  } catch (err) {
    let message =
      err.response?.data?.message ||
      err.response?.data?.detail ||
      err.message ||
      'Erro ao registrar'

    return NextResponse.json({ success: false, message }, { status: 400 })
  }
}
