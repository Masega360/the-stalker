<script setup lang="ts">
const auth = useAuth()
const registerForm = reactive({
  username: "",
  password: ""
})
const loadingRegister = ref(false)
const feedback = ref("")

const register = async () => {
  loadingRegister.value = true
  feedback.value = ""
  try {
    const response = await $fetch<{ user: any }>("/api/auth/register", {
      method: "POST",
      body: {
        username: registerForm.username,
        password: registerForm.password
      }
    })
    auth.user.value = response.user
    navigateTo("/")
  } catch (error) {
    feedback.value = (error as Error).message || "No se pudo registrar. Verificá los datos."
  } finally {
    loadingRegister.value = false
  }
}
</script>

<template>
  <div class="min-h-[calc(100vh-64px)] flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Decoración de fondo -->
    <div class="absolute -top-40 -left-40 w-96 h-96 bg-cyan-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" />
    <div class="absolute -bottom-40 -right-40 w-96 h-96 bg-primary-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000" />

    <UCard class="w-full max-w-md relative z-10 bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl border border-gray-200/50 dark:border-gray-800/50 shadow-2xl">
      <template #header>
        <div class="text-center">
          <div class="w-16 h-16 bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-inner">
            <UIcon name="i-lucide-user-plus" class="w-8 h-8" />
          </div>
          <h2 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            Crear Cuenta
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Sumate a The Stalker para gestionar tus zonas
          </p>
        </div>
      </template>

      <form
        class="space-y-5"
        @submit.prevent="register"
      >
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label
              for="register-username"
              class="block text-sm font-semibold text-gray-700 dark:text-gray-200"
            >
              Nuevo usuario
            </label>
            <span class="text-xs text-gray-500 dark:text-gray-400">Min. 3 caracteres</span>
          </div>
          <UInput
            id="register-username"
            v-model="registerForm.username"
            placeholder="ej. juan_perez"
            icon="i-lucide-user"
            size="lg"
            class="w-full"
            autofocus
          />
        </div>

        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label
              for="register-password"
              class="block text-sm font-semibold text-gray-700 dark:text-gray-200"
            >
              Contraseña
            </label>
            <span class="text-xs text-gray-500 dark:text-gray-400">Min. 6 caracteres</span>
          </div>
          <UInput
            id="register-password"
            v-model="registerForm.password"
            type="password"
            placeholder="••••••••"
            icon="i-lucide-key"
            size="lg"
            class="w-full"
          />
        </div>
        
        <div v-if="feedback" class="p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm rounded-lg flex items-center gap-2">
          <UIcon name="i-lucide-alert-circle" class="w-4 h-4 shrink-0" />
          {{ feedback }}
        </div>

        <UButton
          type="submit"
          :loading="loadingRegister"
          size="lg"
          block
          color="neutral"
          class="mt-6 shadow-md transition-transform active:scale-95 font-semibold"
        >
          Registrarse
        </UButton>

        <div class="text-sm text-center mt-6 text-gray-500 dark:text-gray-400">
          ¿Ya tenés una cuenta? 
          <NuxtLink to="/auth/login" class="font-semibold text-cyan-600 hover:text-cyan-500 transition-colors underline-offset-4 hover:underline">
            Iniciá sesión acá
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
