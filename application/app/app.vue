<script setup>
const auth = useAuth()

// Fetch user on initial load
onMounted(() => {
  auth.fetchUser()
})

useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'en'
  }
})

const title = 'The Stalker'
const description = 'Sistema de monitorizacion'

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description
})
</script>

<template>
  <UApp>
    <UHeader>
      <template #left>
        <NuxtLink to="/" class="inline-flex items-center">
          <AppLogo />
        </NuxtLink>
      </template>

      <template #right>
        <div class="flex items-center gap-4 mr-2">
          <div v-if="auth.loading.value" class="text-sm text-gray-500">
            Cargando...
          </div>
          <template v-else-if="auth.user.value">
            <span class="text-sm font-medium">
              {{ auth.user.value.username }}
            </span>
            <UButton
              color="error"
              variant="soft"
              size="xs"
              @click="auth.logout"
            >
              Salir
            </UButton>
          </template>
          <template v-else>
            <UButton
              to="/auth/login"
              variant="ghost"
              color="neutral"
              size="sm"
            >
              Login
            </UButton>
            <UButton
              to="/auth/register"
              color="primary"
              size="sm"
            >
              Register
            </UButton>
          </template>
        </div>

        <UColorModeButton />
      </template>
    </UHeader>

    <UMain>
      <NuxtPage />
    </UMain>

    <USeparator icon="i-lucide-activity" />

    <UFooter>
      <template #left>
        <p class="text-sm text-muted">
          The Stalker • © {{ new Date().getFullYear() }}
        </p>
      </template>
    </UFooter>
  </UApp>
</template>
