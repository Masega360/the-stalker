import { prisma } from "../../utils/db";

type CreateZoneBody = {
  name?: string
};

export default defineEventHandler(async (event) => {
  const body = await readBody<CreateZoneBody>(event);
  const name = body.name?.trim();

  if (!name) {
    throw createError({ statusCode: 400, statusMessage: "zone name is required" });
  }

  const zone = await prisma.zone.create({
    data: { name },
    include: {
      rooms: {
        include: {
          devices: true
        }
      }
    }
  });

  return { zone };
});
