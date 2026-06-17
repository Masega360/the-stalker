import { prisma } from '../../../utils/db'

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw createError({ statusCode: 400, statusMessage: 'rule id is required' })
  }

  const rule = await prisma.rule.findUnique({
    where: { id },
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
