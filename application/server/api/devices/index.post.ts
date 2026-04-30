import { DEVICES } from "@prisma/client";
import { prisma } from "../../utils/db";

type CreateDeviceBody = {
  ip?: string
  status?: boolean
  type?: DEVICES
  roomId?: string
};

export default defineEventHandler(async (event) => {
  const body = await readBody<CreateDeviceBody>(event);
  const ip = body.ip?.trim();
  const roomId = body.roomId?.trim();
  const status = body.status;
  const type = body.type;

  if (!ip || !roomId || typeof status !== "boolean" || !type) {
    throw createError({
      statusCode: 400,
      statusMessage: "ip, status, type and roomId are required"
    });
  }

  if (type !== DEVICES.SENSOR && type !== DEVICES.ACTUATOR) {
    throw createError({
      statusCode: 400,
      statusMessage: "invalid device type"
    });
  }

  const room = await prisma.room.findUnique({ where: { id: roomId } });
  if (!room) {
    throw createError({ statusCode: 404, statusMessage: "space not found" });
  }

  const device = await prisma.device.create({
    data: {
      ip,
      status,
      type,
      room_id: roomId
    }
  });

  return { device };
});
