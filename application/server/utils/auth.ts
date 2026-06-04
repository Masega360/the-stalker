import type { H3Event } from 'h3'
import { createHmac, randomBytes, scryptSync, timingSafeEqual } from 'node:crypto'

const SESSION_COOKIE_NAME = 'stalker_session'
const SESSION_MAX_AGE_SECONDS = 60 * 60 * 24 * 7 // 7 days

type SessionPayload = {
  sub: string
  username: string
  exp: number
}

export type SessionUser = {
  id: string
  username: string
}

const toBase64Url = (value: string) => Buffer.from(value, 'utf8').toString('base64url')
const fromBase64Url = (value: string) => Buffer.from(value, 'base64url').toString('utf8')

const getAuthSecret = () => {
  const secret = useRuntimeConfig().authSecret

  if (!secret || secret.length < 16) {
    throw createError({
      statusCode: 500,
      statusMessage: 'AUTH_SECRET is missing or too short'
    })
  }

  return secret
}

export const hashPassword = (password: string) => {
  const salt = randomBytes(16).toString('hex')
  const hash = scryptSync(password, salt, 64).toString('hex')
  return `${salt}:${hash}`
}

export const verifyPassword = (password: string, storedHash: string) => {
  const [salt, originalHash] = storedHash.split(':')
  if (!salt || !originalHash) return false

  const computedHash = scryptSync(password, salt, 64).toString('hex')

  const original = Buffer.from(originalHash, 'hex')
  const computed = Buffer.from(computedHash, 'hex')

  if (original.length !== computed.length) return false
  return timingSafeEqual(original, computed)
}

const signPayload = (payloadBase64: string, secret: string) =>
  createHmac('sha256', secret).update(payloadBase64).digest('base64url')

export const createSessionToken = (input: { userId: string, username: string }) => {
  const secret = getAuthSecret()
  const payload: SessionPayload = {
    sub: input.userId,
    username: input.username,
    exp: Math.floor(Date.now() / 1000) + SESSION_MAX_AGE_SECONDS
  }

  const payloadBase64 = toBase64Url(JSON.stringify(payload))
  const signature = signPayload(payloadBase64, secret)
  return `${payloadBase64}.${signature}`
}

export const readSessionToken = (token: string | undefined): SessionPayload | null => {
  if (!token) return null

  const [payloadBase64, signature] = token.split('.')
  if (!payloadBase64 || !signature) return null

  const secret = getAuthSecret()
  const expectedSignature = signPayload(payloadBase64, secret)
  if (expectedSignature !== signature) return null

  const payload = JSON.parse(fromBase64Url(payloadBase64)) as SessionPayload
  if (payload.exp <= Math.floor(Date.now() / 1000)) return null
  return payload
}

export const authCookie = {
  name: SESSION_COOKIE_NAME,
  maxAge: SESSION_MAX_AGE_SECONDS
}

export const getSessionUser = (event: H3Event): SessionUser | null => {
  const token = getCookie(event, authCookie.name)
  const session = readSessionToken(token)
  if (!session) return null
  return { id: session.sub, username: session.username }
}

export const requireUser = (event: H3Event): SessionUser => {
  const user = getSessionUser(event)
  if (!user) {
    throw createError({ statusCode: 401, statusMessage: 'unauthenticated' })
  }
  return user
}
