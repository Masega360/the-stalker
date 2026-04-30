<script setup lang="ts">
const auth = useAuth()
</script>

<template>
  <div class="relative overflow-hidden min-h-[calc(100vh-64px)] flex flex-col">
    <!-- Glowing background elements -->
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" />
    <div class="absolute top-1/3 right-1/4 w-96 h-96 bg-cyan-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000" />
    <div class="absolute -bottom-32 left-1/2 w-96 h-96 bg-blue-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-4000" />

    <div class="relative z-10 container mx-auto px-4 py-16 flex-1 flex flex-col justify-center items-center text-center">
      <div class="mb-6 flex justify-center">
        <UBadge
          color="primary"
          variant="subtle"
          size="lg"
          class="rounded-full px-4 py-1 animate-pulse-slow"
        >
          <UIcon name="i-lucide-radar" class="w-4 h-4 mr-2" />
          Sistema Activo v1.0
        </UBadge>
      </div>

      <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900 dark:text-white mb-8">
        Bienvenido a <br />
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-cyan-500">
          The Stalker
        </span>
      </h1>
      
      <p class="mt-4 text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-10 leading-relaxed">
        Una plataforma inteligente de monitorización en tiempo real.
        Controlá tus dispositivos, analizá estadísticas y gestioná tus zonas desde un único lugar.
      </p>

      <div v-if="auth.loading.value" class="flex justify-center py-4">
        <UIcon name="i-lucide-loader-2" class="w-8 h-8 animate-spin text-primary" />
      </div>
      
      <div v-else-if="auth.user.value" class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up">
        <UButton
          to="/dashboard"
          size="xl"
          color="primary"
          class="px-8 font-semibold shadow-lg shadow-primary-500/30 transition-transform hover:scale-105"
        >
          <UIcon name="i-lucide-layout-dashboard" class="w-5 h-5 mr-2" />
          Ir al Panel
        </UButton>
      </div>
      
      <div v-else class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up">
        <UButton
          to="/auth/login"
          size="xl"
          color="primary"
          class="px-8 font-semibold shadow-lg shadow-primary-500/30 transition-transform hover:scale-105"
        >
          Ingresar al Sistema
        </UButton>
        <UButton
          to="/auth/register"
          size="xl"
          variant="outline"
          color="neutral"
          class="px-8 font-semibold transition-transform hover:scale-105 dark:hover:bg-gray-800"
        >
          Crear cuenta
        </UButton>
      </div>
    </div>

    <!-- Features Section -->
    <div class="relative z-10 bg-gray-50/50 dark:bg-gray-900/50 py-16 border-t border-gray-200 dark:border-gray-800">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <UCard class="bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl border border-gray-200/50 dark:border-gray-700/50 hover:shadow-xl transition-all duration-300">
            <div class="p-4 flex flex-col items-center text-center">
              <div class="w-14 h-14 rounded-2xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center mb-4 text-primary">
                <UIcon name="i-lucide-activity" class="w-7 h-7" />
              </div>
              <h3 class="text-lg font-bold mb-2">Monitorización 24/7</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">Obtené telemetría en tiempo real de todos tus sensores sin latencia.</p>
            </div>
          </UCard>
          
          <UCard class="bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl border border-gray-200/50 dark:border-gray-700/50 hover:shadow-xl transition-all duration-300">
            <div class="p-4 flex flex-col items-center text-center">
              <div class="w-14 h-14 rounded-2xl bg-cyan-100 dark:bg-cyan-900/30 flex items-center justify-center mb-4 text-cyan-500">
                <UIcon name="i-lucide-cpu" class="w-7 h-7" />
              </div>
              <h3 class="text-lg font-bold mb-2">Control de Actuadores</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">Interactuá remotamente con tus dispositivos y controlá su estado al instante.</p>
            </div>
          </UCard>
          
          <UCard class="bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl border border-gray-200/50 dark:border-gray-700/50 hover:shadow-xl transition-all duration-300">
            <div class="p-4 flex flex-col items-center text-center">
              <div class="w-14 h-14 rounded-2xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4 text-blue-500">
                <UIcon name="i-lucide-bar-chart-3" class="w-7 h-7" />
              </div>
              <h3 class="text-lg font-bold mb-2">Análisis de Datos</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">Estadísticas detalladas por zonas y dispositivos para tomar mejores decisiones.</p>
            </div>
          </UCard>
        </div>
      </div>
    </div>
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
.animation-delay-4000 {
  animation-delay: 4s;
}
.animate-pulse-slow {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
