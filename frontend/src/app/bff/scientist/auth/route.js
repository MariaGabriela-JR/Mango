import { NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'

export async function GET(req) {
  const accessToken = req.cookies.get('accessToken')?.value

  if (!accessToken) {
    return NextResponse.json({ isLoggedIn: false, user: null })
  }

  try {
    const payload = jwt.decode(accessToken)
    return NextResponse.json({ isLoggedIn: true, user: payload })
  } catch {
    return NextResponse.json({ isLoggedIn: false, user: null })
  }
}
