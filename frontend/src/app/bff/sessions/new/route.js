// app/bff/sessions/new/route.js
import { NextResponse } from 'next/server'
import axios from 'axios'
import { getGatewayUrl } from '@/lib/getGatewayUrl'

export async function POST(req) {
  try {
    const { patientId, sessionName, edfFile } = await req.json()

    const accessToken = req.cookies.get('accessToken')?.value
    if (!accessToken) {
      return NextResponse.json({ success: false, message: 'Não autenticado' }, { status: 401 })
    }

    // Payload no formato esperado pelo Gateway
    const payload = {
      patient_iid: patientId,
      session_name: sessionName,
      file_path: edfFile,
    }

    console.log('Payload enviado ao Gateway:', payload)

    const response = await axios.post(`${getGatewayUrl()}/edf_files/process-edf-file`, payload, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })

    return NextResponse.json({
      success: true,
      message: response.data.message || 'Sessão criada com sucesso!',
      data: response.data,
    })
  } catch (err) {
    console.error('Erro ao criar sessão', err.response?.data || err.message)

    return NextResponse.json(
      {
        success: false,
        message:
          err.response?.data?.detail ||
          (typeof err.response?.data === 'string' ? err.response.data : 'Erro ao criar sessão'),
      },
      { status: err.response?.status || 500 },
    )
  }
}
