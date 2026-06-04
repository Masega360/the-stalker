import { prisma } from '../../../utils/db'
import { requireUser } from '../../../utils/auth'

export default defineEventHandler(async (event) => {
  const user = requireUser(event)
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw createError({ statusCode: 400, statusMessage: 'device id is required' })
  }

  const device = await prisma.device.findFirst({
    where: {
      id,
      room: {
        zone: {
          users: { some: { user_id: user.id } }
        }
      }
    },
    include: {
      room: {
        include: {
          zone: true
        }
      },
      stats: {
        orderBy: { time: 'desc' },
        include: {
          stat_type: {
            include: { data_type: true }
          }
        }
      }
    }
  })

  if (!device) {
    throw createError({ statusCode: 404, statusMessage: 'device not found' })
  }

  return { device }
})
