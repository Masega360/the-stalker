import { prisma } from '../../utils/db'
import { requireUser } from '../../utils/auth'

type DeviceKind = 'SENSOR' | 'ACTUATOR'

type CreateDeviceBody = {
  ip?: string
  status?: boolean
  type?: DeviceKind
  roomId?: string
}

export default defineEventHandler(async (event) => {
  const user = requireUser(event)
  const body = await readBody<CreateDeviceBody>(event)
  const ip = body.ip?.trim()
  const roomId = body.roomId?.trim()
  const status = body.status
  const type = body.type

  if (!ip || !roomId || typeof status !== 'boolean' || !type) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ip, status, type and roomId are required'
    })
  }

  if (type !== 'SENSOR' && type !== 'ACTUATOR') {
    throw createError({
      statusCode: 400,
      statusMessage: 'invalid device type'
    })
  }

  const room = await prisma.room.findFirst({
    where: {
      id: roomId,
      zone: {
        users: { some: { user_id: user.id } }
      }
    },
    select: { id: true }
  })

  if (!room) {
    throw createError({ statusCode: 404, statusMessage: 'space not found' })
  }

  const device = await prisma.device.create({
    data: {
      ip,
      status,
      type,
      room_id: room.id
    }
  })

  return { device }
})
