import { prisma } from '../../../utils/db'
import { requireUser } from '../../../utils/auth'

export default defineEventHandler(async (event) => {
  const user = requireUser(event)
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw createError({ statusCode: 400, statusMessage: 'rule id is required' })
  }

  const rule = await prisma.rule.findFirst({
    where: {
      id,
      OR: [
        { sensor_device: { room: { zone: { users: { some: { user_id: user.id } } } } } },
        { actuator_device: { room: { zone: { users: { some: { user_id: user.id } } } } } }
      ]
    },
    include: {
      sensor_device: true,
      actuator_device: true,
      stat_type: { include: { data_type: true } },
      stat_data_type: true
    }
  })

  if (!rule) {
    throw createError({ statusCode: 404, statusMessage: 'rule not found' })
  }

  return { rule }
})
