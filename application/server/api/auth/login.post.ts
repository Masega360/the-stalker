import { prisma } from '../../utils/db'
import { authCookie, createSessionToken, verifyPassword } from '../../utils/auth'

type LoginBody = {
  username?: string
  password?: string
}

export default defineEventHandler(async (event) => {
  const body = await readBody<LoginBody>(event)
  const username = body.username?.trim()
  const password = body.password?.trim()

  if (!username || !password) {
    throw createError({ statusCode: 400, statusMessage: 'username and password are required' })
  }

  const user = await prisma.user.findUnique({
    where: { username },
    select: {
      id: true,
      username: true,
      role: true,
      p_hash: true
    }
  })

  if (!user || !verifyPassword(password, user.p_hash)) {
    throw createError({ statusCode: 401, statusMessage: 'invalid credentials' })
  }

  const token = createSessionToken({ userId: user.id, username: user.username })
  setCookie(event, authCookie.name, token, {
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
    maxAge: authCookie.maxAge,
    path: '/'
  })

  return {
    user: {
      id: user.id,
      username: user.username,
      role: user.role
    }
  }
})
