import { prisma } from "../../utils/db";
import { requireUser } from "../../utils/auth";

export default defineEventHandler(async (event) => {
  const user = requireUser(event);
  const query = getQuery(event);
  const limitRaw = Number(query.limit ?? 50);
  const limit = Number.isFinite(limitRaw) ? Math.min(Math.max(limitRaw, 1), 200) : 50;

  const stats = await prisma.stats.findMany({
    take: limit,
    orderBy: { time: "desc" },
    where: {
      device: {
        is: {
          room: {
            zone: {
              users: { some: { user_id: user.id } }
            }
          }
        }
      }
    },
    include: {
      stat_type: { include: { data_type: true } },
      device: {
        select: {
          id: true,
          ip: true,
          room: { select: { name: true, zone: { select: { name: true } } } }
        }
      }
    }
  });

  return { stats };
});
