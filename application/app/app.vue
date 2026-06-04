<script setup>
const auth = useAuth()
const userInitial = computed(() => auth.user.value?.username?.charAt(0).toUpperCase() ?? '?')

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
        <NuxtLink
          to="/"
          class="inline-flex items-center"
        >
          <AppLogo />
        </NuxtLink>
      </template>

      <template #right>
        <div class="flex items-center gap-4 mr-2">
          <div
            v-if="auth.loading.value"
            class="text-sm text-gray-500"
          >
            Cargando...
          </div>
          <template v-else-if="auth.user.value">
            <div class="flex items-center gap-2">
              <span class="size-7 rounded-full bg-primary-100 text-primary-700 dark:bg-primary-900/40 dark:text-primary-200 inline-flex items-center justify-center text-xs font-semibold">
                {{ userInitial }}
              </span>
              <span class="text-sm font-medium">
                {{ auth.user.value.username }}
              </span>
            </div>
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
