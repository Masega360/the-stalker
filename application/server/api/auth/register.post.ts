import { ROLE } from "@prisma/client";
import { prisma } from "../../utils/db";
import { authCookie, createSessionToken, hashPassword } from "../../utils/auth";

type RegisterBody = {
  username?: string
  password?: string
};

export default defineEventHandler(async (event) => {
  const body = await readBody<RegisterBody>(event);
  const username = body.username?.trim();
  const password = body.password?.trim();

  if (!username || !password) {
    throw createError({ statusCode: 400, statusMessage: "username and password are required" });
  }

  if (username.length < 3 || password.length < 6) {
    throw createError({
      statusCode: 400,
      statusMessage: "username must be >= 3 and password must be >= 6 characters"
    });
  }

  const existingUser = await prisma.user.findUnique({ where: { username } });
  if (existingUser) {
    throw createError({ statusCode: 409, statusMessage: "username already exists" });
  }

  const user = await prisma.user.create({
    data: {
      username,
      p_hash: hashPassword(password),
      role: ROLE.USER
    },
    select: {
      id: true,
      username: true,
      role: true
    }
  });

  const token = createSessionToken({ userId: user.id, username: user.username });
  setCookie(event, authCookie.name, token, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    maxAge: authCookie.maxAge,
    path: "/"
  });

  return { user };
});
