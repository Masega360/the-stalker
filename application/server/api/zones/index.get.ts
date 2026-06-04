import { prisma } from '../../utils/db'
import { requireUser } from '../../utils/auth'

export default defineEventHandler(async (event) => {
  const user = requireUser(event)

  const zones = await prisma.zone.findMany({
    where: {
      users: { some: { user_id: user.id } }
    },
    orderBy: { created_at: 'desc' },
    include: {
      rooms: {
        orderBy: { created_at: 'desc' },
        include: {
          devices: true
        }
      }
    }
  })

  return { zones }
})
