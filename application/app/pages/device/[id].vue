<script setup lang="ts">
type StatType = 'PEOPLE' | 'GENRE' | 'AGE'
type DeviceType = 'SENSOR' | 'ACTUATOR'

interface DeviceStat {
  id: string
  quantity: number
  type: StatType
  time: string
}

interface DeviceDetails {
  id: string
  ip: string
  status: boolean
  type: DeviceType
  room: {
    name: string
    zone: {
      name: string
    }
  }
  stats: DeviceStat[]
}

const route = useRoute()
const deviceId = computed(() => String(route.params.id || ''))
const loading = ref(true)
const device = ref<DeviceDetails | null>(null)

const loadDevice = async () => {
  if (!deviceId.value) return

  loading.value = true
  try {
    const response = await $fetch<{ device: DeviceDetails }>(`/api/devices/${deviceId.value}/stats`)
    device.value = response.device
  } finally {
    loading.value = false
  }
}

watch(deviceId, loadDevice, { immediate: true })

const statColor = (type: StatType) => {
  if (type === 'PEOPLE') return 'primary'
  if (type === 'AGE') return 'warning'
  return 'neutral'
}

const formatDate = (value: string) =>
  new Date(value).toLocaleString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
</script>

<template>
  <div class="container mx-auto px-4 py-6 space-y-6">
    <div class="flex items-center justify-between gap-3">
      <div>
        <p class="text-sm text-muted">
          <NuxtLink to="/dashboard" class="hover:underline">Dashboard</NuxtLink> / Device
        </p>
        <h1 class="text-2xl font-bold tracking-tight">
          Dispositivo {{ device?.id.slice(0, 8) || '' }}
        </h1>
      </div>
      <UButton to="/dashboard" variant="ghost" color="neutral">
        Volver
      </UButton>
    </div>

    <div v-if="loading" class="py-10 flex justify-center">
      <UIcon name="i-lucide-loader-2" class="size-7 animate-spin text-primary" />
    </div>

    <template v-else-if="device">
      <section class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <UCard>
          <template #header>
            <p class="text-sm text-muted">IP</p>
          </template>
          <p class="text-xl font-semibold">{{ device.ip }}</p>
        </UCard>

        <UCard>
          <template #header>
            <p class="text-sm text-muted">Ubicacion</p>
          </template>
          <p class="text-xl font-semibold">{{ device.room.zone.name }}</p>
          <p class="text-xs text-muted">{{ device.room.name }}</p>
        </UCard>

        <UCard>
          <template #header>
            <p class="text-sm text-muted">Estado</p>
          </template>
          <div class="flex items-center gap-2">
            <UBadge :color="device.status ? 'success' : 'error'" variant="subtle">
              {{ device.status ? 'Online' : 'Offline' }}
            </UBadge>
            <UBadge color="neutral" variant="outline">
              {{ device.type }}
            </UBadge>
          </div>
        </UCard>
      </section>

      <section>
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-base font-semibold">Estadisticas del dispositivo</h2>
              <UBadge color="neutral" variant="outline">
                {{ device.stats.length }} registros
              </UBadge>
            </div>
          </template>

          <div v-if="device.stats.length === 0" class="text-sm text-muted">
            Este dispositivo aun no tiene estadisticas registradas.
          </div>

          <div v-else class="space-y-2">
            <div
              v-for="stat in device.stats"
              :key="stat.id"
              class="rounded-lg border border-accented p-3 flex flex-wrap items-center justify-between gap-2"
            >
              <div class="flex items-center gap-2">
                <UBadge :color="statColor(stat.type)" variant="subtle">
                  {{ stat.type }}
                </UBadge>
                <p class="font-medium">
                  {{ stat.quantity }}
                </p>
              </div>
              <p class="text-xs text-muted">
                {{ formatDate(stat.time) }}
              </p>
            </div>
          </div>
        </UCard>
      </section>
    </template>
  </div>
</template>
