import { prisma } from "../../utils/db";
import { requireUser } from "../../utils/auth";

type CreateSpaceBody = {
  name?: string
  zoneId?: string
};

export default defineEventHandler(async (event) => {
  const user = requireUser(event);
  const body = await readBody<CreateSpaceBody>(event);
  const name = body.name?.trim();
  const zoneId = body.zoneId?.trim();

  if (!name || !zoneId) {
    throw createError({ statusCode: 400, statusMessage: "space name and zoneId are required" });
  }

  const zone = await prisma.zone.findFirst({
    where: {
      id: zoneId,
      users: { some: { user_id: user.id } }
    },
    select: { id: true }
  });

  if (!zone) {
    throw createError({ statusCode: 404, statusMessage: "zone not found" });
  }

  const space = await prisma.room.create({
    data: {
      name,
      zone_id: zone.id
    }
  });

  return { space };
});
