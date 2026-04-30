import { prisma } from "../utils/db";

export default defineEventHandler(async () => {
  const users = await prisma.user.findMany({
    select: {
      id: true,
      username: true,
      role: true,
      created_at: true
    }
  });
  return users;
});
