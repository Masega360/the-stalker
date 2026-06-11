import { prisma } from '../../utils/db'
import { requireUser } from '../../utils/auth'

type CreateZoneBody = {
  name?: string
}

export default defineEventHandler(async (event) => {
  const user = requireUser(event)
  const body = await readBody<CreateZoneBody>(event)
  const name = body.name?.trim()

  if (!name) {
    throw createError({ statusCode: 400, statusMessage: 'zone name is required' })
  }

  const zone = await prisma.zone.create({
    data: {
      name,
      users: {
        create: { user_id: user.id }
      }
    },
    include: {
      rooms: {
        include: {
          devices: true
        }
      }
    }
  })

  return { zone }
})
