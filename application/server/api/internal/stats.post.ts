import { prisma } from '../../utils/db'

type IncomingStatBody = {
  snapshot_id?: string
  stat_type?: string
  data_type?: string
  value?: number
  device_id?: string
}

export default defineEventHandler(async (event) => {
  const body = await readBody<IncomingStatBody>(event)

  const snapshotId = body.snapshot_id?.trim()
  const statTypeName = body.stat_type?.trim()
  const dataTypeName = body.data_type?.trim()
  const value = body.value
  const deviceId = body.device_id?.trim()

  if (!snapshotId || !statTypeName || !dataTypeName || typeof value !== 'number') {
    throw createError({
      statusCode: 400,
      statusMessage: 'snapshot_id, stat_type, data_type and value are required'
    })
  }

  if (!Number.isFinite(value)) {
    throw createError({ statusCode: 400, statusMessage: 'value must be a finite number' })
  }

  const result = await prisma.$transaction(async (tx) => {
    const dataType = await tx.statDataType.upsert({
      where: { name: dataTypeName },
      update: {},
      create: { name: dataTypeName }
    })

    const statType = await tx.statType.upsert({
      where: { name: statTypeName },
      update: {},
      create: {
        name: statTypeName,
        data_type_id: dataType.id
      }
    })

    const stat = await tx.stats.create({
      data: {
        quantity: Math.trunc(value),
        snapshot_id: snapshotId,
        stat_type_id: statType.id,
        device_id: deviceId ?? null
      },
      include: {
        stat_type: { include: { data_type: true } }
      }
    })

    return { stat, statType, dataType }
  })

  setResponseStatus(event, 201)
  return {
    stat: result.stat,
    stat_type: result.statType,
    data_type: result.dataType
  }
})
