import { prisma } from "../../utils/db";
import { authCookie, readSessionToken } from "../../utils/auth";

export default defineEventHandler(async (event) => {
  const token = getCookie(event, authCookie.name);
  const session = readSessionToken(token);

  if (!session) {
    return { user: null };
  }

  const user = await prisma.user.findUnique({
    where: { id: session.sub },
    select: {
      id: true,
      username: true,
      role: true
    }
  });

  if (!user) {
    deleteCookie(event, authCookie.name, { path: "/" });
    return { user: null };
  }

  return { user };
});
