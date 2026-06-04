import { authCookie } from '../../utils/auth'

export default defineEventHandler(async (event) => {
  deleteCookie(event, authCookie.name, { path: '/' })
  return { ok: true }
})
