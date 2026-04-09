import { prisma } from "../../../utils/db";

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id");

  if (!id) {
    throw createError({ statusCode: 400, statusMessage: "device id is required" });
  }

  const device = await prisma.device.findUnique({
    where: { id },
    include: {
      room: {
        include: {
          zone: true
        }
      },
      stats: {
        orderBy: { time: "desc" }
      }
    }
  });

  if (!device) {
    throw createError({ statusCode: 404, statusMessage: "device not found" });
  }

  return { device };
});
