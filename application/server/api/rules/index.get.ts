import { prisma } from '../../utils/db'
import { requireUser } from '../../utils/auth'

export default defineEventHandler(async (event) => {
  const user = requireUser(event)

  const rules = await prisma.rule.findMany({
    where: {
      OR: [
        { sensor_device: { room: { zone: { users: { some: { user_id: user.id } } } } } },
        { actuator_device: { room: { zone: { users: { some: { user_id: user.id } } } } } }
      ]
    },
    orderBy: { created_at: 'desc' },
    include: {
      sensor_device: true,
      actuator_device: true,
      stat_type: { include: { data_type: true } },
      stat_data_type: true
    }
  })

  return { rules }
})
