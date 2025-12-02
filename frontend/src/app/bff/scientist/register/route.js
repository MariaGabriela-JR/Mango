import { NextResponse } from 'next/server'
import axios from 'axios'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function POST(req) {
  try {
    const body = await req.json()
    const { email, password, firstName, lastName, institution, specialization } = body

    const data = {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
      institution,
      specialization,
    }
    const response = await axios.post(`${getGatewayUrl()}/scientists/register`, data, {
      headers: { 'Content-Type': 'application/json' },
    })

    const { registration_token } = response.data

    return NextResponse.json({
      success: true,
      message: response.data.message || 'Conta criada com sucesso!',
      registration_token,
    })
  } catch (err) {
    return handleError(err)
  }
}

function handleError(err) {
  let message = 'Erro ao registrar'
  if (err.response?.data) {
    const data = err.response.data
    const messages = []
    for (const key in data) {
      if (Array.isArray(data[key])) messages.push(data[key].join(', '))
      else messages.push(String(data[key]))
    }
    message = messages.join(' | ')
  } else if (err.message) {
    message = err.message
  }
  return NextResponse.json({ success: false, message }, { status: 400 })
}
