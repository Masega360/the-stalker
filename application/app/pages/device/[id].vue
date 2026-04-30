<script setup lang="ts">
type DeviceType = 'SENSOR' | 'ACTUATOR'

interface StatDataType {
  id: string
  name: string
  unit: string | null
}

interface StatType {
  id: string
  name: string
  data_type: StatDataType
}

interface DeviceStat {
  id: string
  quantity: number
  time: string
  snapshot_id: string | null
  stat_type: StatType
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

const STAT_COLORS = ['primary', 'warning', 'info', 'success', 'error', 'secondary'] as const
type StatColor = typeof STAT_COLORS[number]

const hashString = (value: string) => {
  let hash = 0
  for (let i = 0; i < value.length; i++) {
    hash = (hash << 5) - hash + value.charCodeAt(i)
    hash |= 0
  }
  return Math.abs(hash)
}

const statColor = (name: string): StatColor =>
  STAT_COLORS[hashString(name) % STAT_COLORS.length]!

const formatValue = (stat: DeviceStat) => {
  const unit = stat.stat_type.data_type.unit
  return unit ? `${stat.quantity} ${unit}` : String(stat.quantity)
}

const formatDate = (value: string) =>
  new Date(value).toLocaleString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })

interface StatGroup {
  name: string
  dataType: string
  unit: string | null
  items: DeviceStat[]
  latest: DeviceStat
}

const groupedStats = computed<StatGroup[]>(() => {
  if (!device.value) return []
  const map = new Map<string, StatGroup>()
  for (const stat of device.value.stats) {
    const key = stat.stat_type.id
    const existing = map.get(key)
    if (existing) {
      existing.items.push(stat)
      if (new Date(stat.time) > new Date(existing.latest.time)) {
        existing.latest = stat
      }
    } else {
      map.set(key, {
        name: stat.stat_type.name,
        dataType: stat.stat_type.data_type.name,
        unit: stat.stat_type.data_type.unit,
        items: [stat],
        latest: stat
      })
    }
  }
  return [...map.values()].sort((a, b) => a.name.localeCompare(b.name))
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
          {{ device?.ip || 'Dispositivo' }}
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
            <p class="text-sm text-muted">ID del dispositivo</p>
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

      <section v-if="groupedStats.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <UCard v-for="group in groupedStats" :key="group.name">
          <template #header>
            <div class="flex items-center justify-between gap-2">
              <UBadge :color="statColor(group.name)" variant="subtle">
                {{ group.name }}
              </UBadge>
              <UBadge color="neutral" variant="outline" size="sm">
                {{ group.dataType }}
              </UBadge>
            </div>
          </template>
          <p class="text-3xl font-semibold">
            {{ group.latest.quantity }}
            <span v-if="group.unit" class="text-base text-muted font-normal">{{ group.unit }}</span>
          </p>
          <p class="text-xs text-muted mt-1">
            Ultima lectura {{ formatDate(group.latest.time) }} · {{ group.items.length }} muestras
          </p>
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
              <div class="flex items-center gap-2 flex-wrap">
                <UBadge :color="statColor(stat.stat_type.name)" variant="subtle">
                  {{ stat.stat_type.name }}
                </UBadge>
                <UBadge color="neutral" variant="outline" size="sm">
                  {{ stat.stat_type.data_type.name }}
                </UBadge>
                <p class="font-medium">
                  {{ formatValue(stat) }}
                </p>
                <span
                  v-if="stat.snapshot_id"
                  class="text-xs text-muted font-mono"
                  :title="stat.snapshot_id"
                >
                  snap {{ stat.snapshot_id.slice(0, 8) }}
                </span>
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
