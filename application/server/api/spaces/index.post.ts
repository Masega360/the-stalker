import { prisma } from "../../utils/db";

type CreateSpaceBody = {
  name?: string
  zoneId?: string
};

export default defineEventHandler(async (event) => {
  const body = await readBody<CreateSpaceBody>(event);
  const name = body.name?.trim();
  const zoneId = body.zoneId?.trim();

  if (!name || !zoneId) {
    throw createError({ statusCode: 400, statusMessage: "space name and zoneId are required" });
  }

  const zone = await prisma.zone.findUnique({ where: { id: zoneId } });
  if (!zone) {
    throw createError({ statusCode: 404, statusMessage: "zone not found" });
  }

  const space = await prisma.room.create({
    data: {
      name,
      zone_id: zoneId
    }
  });

  return { space };
});
