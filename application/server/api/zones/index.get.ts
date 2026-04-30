import { prisma } from "../../utils/db";

export default defineEventHandler(async () => {
  const zones = await prisma.zone.findMany({
    orderBy: { created_at: "desc" },
    include: {
      rooms: {
        orderBy: { created_at: "desc" },
        include: {
          devices: true
        }
      }
    }
  });

  return { zones };
});
