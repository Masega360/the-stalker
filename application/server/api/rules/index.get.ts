import { prisma } from '../../utils/db'

export default defineEventHandler(async (event) => {
  const rules = await prisma.rule.findMany({
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
