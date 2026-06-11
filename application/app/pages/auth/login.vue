<script setup lang="ts">
import type { User } from '@/composables/useAuth'

const auth = useAuth()

const loginForm = reactive({
  username: '',
  password: ''
})

const showPassword = ref(false)
const loadingLogin = ref(false)
const feedback = ref('')

const login = async () => {
  loadingLogin.value = true
  feedback.value = ''
  try {
    const response = await $fetch<{ user: User }>('/api/auth/login', {
      method: 'POST',
      body: {
        username: loginForm.username,
        password: loginForm.password
      }
    })
    auth.user.value = response.user
    navigateTo('/')
  } catch (error) {
    feedback.value = (error as Error).message || 'Credenciales invalidas'
  } finally {
    loadingLogin.value = false
  }
}
</script>

<template>
  <div class="min-h-[calc(100vh-64px)] flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Decoración de fondo -->
    <div class="absolute -top-40 -right-40 w-96 h-96 bg-primary-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" />
    <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-cyan-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000" />

    <UCard class="w-full max-w-md relative z-10 bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl border border-gray-200/50 dark:border-gray-800/50 shadow-2xl">
      <template #header>
        <div class="text-center">
          <div class="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 text-primary rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner">
            <UIcon
              name="i-lucide-lock-keyhole"
              class="w-8 h-8"
            />
          </div>
          <h2 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            Iniciar Sesión
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Ingresá tus credenciales para acceder a la plataforma
          </p>
        </div>
      </template>

      <form
        class="space-y-5"
        @submit.prevent="login"
      >
        <div class="space-y-2">
          <label
            for="login-username"
            class="block text-sm font-semibold text-gray-700 dark:text-gray-200"
          >
            Usuario
          </label>
          <UInput
            id="login-username"
            v-model="loginForm.username"
            placeholder="admin"
            icon="i-lucide-user"
            size="lg"
            class="w-full"
            autofocus
          />
        </div>

        <div class="space-y-2">
          <label
            for="login-password"
            class="block text-sm font-semibold text-gray-700 dark:text-gray-200"
          >
            Contraseña
          </label>
          <UInput
            id="login-password"
            v-model="loginForm.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••••"
            icon="i-lucide-key"
            size="lg"
            class="w-full"
          >
            <template #trailing>
              <UButton
                color="neutral"
                variant="ghost"
                size="xs"
                :icon="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                :padded="false"
                type="button"
                @click="showPassword = !showPassword"
              />
            </template>
          </UInput>
        </div>

        <div
          v-if="feedback"
          class="p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm rounded-lg flex items-center gap-2"
        >
          <UIcon
            name="i-lucide-alert-circle"
            class="w-4 h-4 shrink-0"
          />
          {{ feedback }}
        </div>

        <UButton
          type="submit"
          :loading="loadingLogin"
          size="lg"
          block
          color="primary"
          class="mt-6 shadow-md transition-transform active:scale-95 font-semibold"
        >
          Ingresar
        </UButton>

        <div class="text-sm text-center mt-6 text-gray-500 dark:text-gray-400">
          ¿No tenés cuenta?
          <NuxtLink
            to="/auth/register"
            class="font-semibold text-primary hover:text-primary-600 transition-colors underline-offset-4 hover:underline"
          >
            Crear cuenta nueva
          </NuxtLink>
        </div>
      </form>
    </UCard>
  </div>
</template>

<style scoped>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
</style>
