<script setup lang="ts">
type DeviceType = 'SENSOR' | 'ACTUATOR'

interface DeviceNode {
  id: string
  ip: string
  status: boolean
  type: DeviceType
}

interface SpaceNode {
  id: string
  name: string
  devices: DeviceNode[]
}

interface ZoneNode {
  id: string
  name: string
  rooms: SpaceNode[]
}

const lastUpdate = ref(new Date())
const zones = ref<ZoneNode[]>([])

const createZoneOpen = ref(false)
const createSpaceOpen = ref(false)
const createDeviceOpen = ref(false)
const creatingZone = ref(false)
const creatingSpace = ref(false)
const creatingDevice = ref(false)
const loadingZones = ref(false)

const zoneNameInput = ref('')
const spaceNameInput = ref('')
const selectedZoneId = ref('')
const selectedRoomId = ref('')
const deviceIpInput = ref('')
const deviceTypeInput = ref<DeviceType>('SENSOR')
const deviceStatusInput = ref(true)

const loadZones = async () => {
  loadingZones.value = true
  try {
    const response = await $fetch<{ zones: ZoneNode[] }>('/api/zones')
    zones.value = response.zones
    lastUpdate.value = new Date()
  } finally {
    loadingZones.value = false
  }
}

onMounted(loadZones)

const openCreateSpace = (zoneId: string) => {
  selectedZoneId.value = zoneId
  spaceNameInput.value = ''
  createSpaceOpen.value = true
}

const openCreateDevice = (roomId: string) => {
  selectedRoomId.value = roomId
  deviceIpInput.value = ''
  deviceTypeInput.value = 'SENSOR'
  deviceStatusInput.value = true
  createDeviceOpen.value = true
}

const createZone = async () => {
  const name = zoneNameInput.value.trim()
  if (!name) return

  creatingZone.value = true
  try {
    await $fetch('/api/zones', {
      method: 'POST',
      body: { name }
    })
    zoneNameInput.value = ''
    createZoneOpen.value = false
    await loadZones()
  } finally {
    creatingZone.value = false
  }
}

const createSpace = async () => {
  const name = spaceNameInput.value.trim()
  const zoneId = selectedZoneId.value
  if (!name || !zoneId) return

  creatingSpace.value = true
  try {
    await $fetch('/api/spaces', {
      method: 'POST',
      body: { name, zoneId }
    })
    spaceNameInput.value = ''
    createSpaceOpen.value = false
    await loadZones()
  } finally {
    creatingSpace.value = false
  }
}

const createDevice = async () => {
  const ip = deviceIpInput.value.trim()
  const roomId = selectedRoomId.value
  if (!ip || !roomId) return

  creatingDevice.value = true
  try {
    await $fetch('/api/devices', {
      method: 'POST',
      body: {
        ip,
        status: deviceStatusInput.value,
        type: deviceTypeInput.value,
        roomId
      }
    })
    deviceIpInput.value = ''
    createDeviceOpen.value = false
    await loadZones()
  } finally {
    creatingDevice.value = false
  }
}

const totalSpaces = computed(() => zones.value.reduce((acc, zone) => acc + zone.rooms.length, 0))
const totalDevices = computed(() =>
  zones.value.reduce((acc, zone) => acc + zone.rooms.reduce((spacesAcc, room) => spacesAcc + room.devices.length, 0), 0)
)
const onlineDevices = computed(() =>
  zones.value.reduce(
    (acc, zone) =>
      acc
      + zone.rooms.reduce((spacesAcc, room) => spacesAcc + room.devices.filter(device => device.status).length, 0),
    0
  )
)
const offlineDevices = computed(() => totalDevices.value - onlineDevices.value)
const health = computed(() => (totalDevices.value === 0 ? 0 : Math.round((onlineDevices.value / totalDevices.value) * 100)))

const statusColor = (isOnline: boolean) => (isOnline ? 'success' : 'error')
const deviceLabel = (device: DeviceNode) => `${device.type} · ${device.id.slice(0, 8)}`
</script>

<template>
  <div class="container mx-auto px-4 py-6 space-y-6">
    <section class="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">
          Dashboard Operativo en Tiempo Real
        </h1>
        <p class="text-sm text-muted">
          Vista consolidada de zonas, espacios y dispositivos en tiempo real.
        </p>
      </div>
      <UBadge color="primary" variant="subtle" size="lg" class="w-fit">
        <UIcon name="i-lucide-clock-3" class="size-4 mr-2" />
        Actualizado {{ lastUpdate.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' }) }}
      </UBadge>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <p class="text-sm text-muted">
              Zonas
            </p>
            <UIcon name="i-lucide-map-pinned" class="size-4 text-primary" />
          </div>
        </template>
        <p class="text-3xl font-semibold">
          {{ zones.length }}
        </p>
        <p class="text-xs text-muted mt-1">
          Cobertura activa en el sistema
        </p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <p class="text-sm text-muted">
              Salud del sistema
            </p>
            <UIcon name="i-lucide-activity" class="size-4 text-primary" />
          </div>
        </template>
        <p class="text-3xl font-semibold">
          {{ health }}%
        </p>
        <p class="text-xs text-muted mt-1">
          {{ onlineDevices }} online / {{ offlineDevices }} offline
        </p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <p class="text-sm text-muted">
              Cobertura
            </p>
            <UIcon name="i-lucide-map" class="size-4 text-primary" />
          </div>
        </template>
        <p class="text-3xl font-semibold">
          {{ totalSpaces }} espacios
        </p>
        <p class="text-xs text-muted mt-1">
          Total de espacios creados por zona
        </p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <p class="text-sm text-muted">
              Dispositivos
            </p>
            <UIcon name="i-lucide-cpu" class="size-4 text-primary" />
          </div>
        </template>
        <p class="text-3xl font-semibold">
          {{ totalDevices }}
        </p>
        <p class="text-xs text-muted mt-1">
          Sensores y actuadores registrados
        </p>
      </UCard>
    </section>

    <section class="grid grid-cols-1 gap-4">
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h2 class="text-base font-semibold">
              Estado por zona
            </h2>
            <div class="flex items-center gap-2">
              <UBadge color="neutral" variant="outline">
                {{ zones.length }} zonas
              </UBadge>
              <UButton size="sm" color="primary" @click="createZoneOpen = true">
                <UIcon name="i-lucide-plus" class="size-4 mr-1" />
                Crear zona
              </UButton>
            </div>
          </div>
        </template>

        <div v-if="loadingZones" class="py-8 flex justify-center">
          <UIcon name="i-lucide-loader-2" class="size-6 animate-spin text-primary" />
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="zone in zones"
            :key="zone.id"
            class="rounded-lg border border-accented p-3"
          >
            <div class="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p class="font-medium">
                  {{ zone.name }}
                </p>
              </div>
              <div class="flex flex-wrap gap-2">
                <UBadge color="neutral" variant="outline">
                  Espacios {{ zone.rooms.length }}
                </UBadge>
                <UBadge color="primary" variant="subtle">
                  Devices {{ zone.rooms.reduce((acc, room) => acc + room.devices.length, 0) }}
                </UBadge>
              </div>
            </div>
          </div>
        </div>
      </UCard>
    </section>

    <section>
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h2 class="text-base font-semibold">
              Diagrama de zonas y espacios
            </h2>
            <UBadge color="primary" variant="outline">
              Estructura: Zona > Espacio > Device
            </UBadge>
          </div>
        </template>

        <div v-if="loadingZones" class="py-8 flex justify-center">
          <UIcon name="i-lucide-loader-2" class="size-6 animate-spin text-primary" />
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="zone in zones"
            :key="zone.id"
            class="rounded-xl border border-accented p-4"
          >
            <div class="flex items-center justify-between gap-2 mb-3">
              <div class="flex items-center gap-2">
                <UIcon name="i-lucide-map-pinned" class="size-4 text-cyan-500" />
                <p class="font-semibold">
                  {{ zone.name }}
                </p>
              </div>
              <UButton size="xs" variant="soft" color="primary" @click="openCreateSpace(zone.id)">
                <UIcon name="i-lucide-plus" class="size-3.5 mr-1" />
                Crear espacio
              </UButton>
            </div>

            <div class="space-y-3 pl-2 border-l-2 border-cyan-500/30">
              <div
                v-for="room in zone.rooms"
                :key="room.id"
                class="pl-4"
              >
                <div class="flex items-center gap-2">
                  <UIcon name="i-lucide-door-open" class="size-4 text-indigo-500" />
                  <p class="text-sm font-medium">
                    {{ room.name }}
                  </p>
                  <UButton size="xs" variant="outline" color="neutral" @click="openCreateDevice(room.id)">
                    <UIcon name="i-lucide-plus" class="size-3 mr-1" />
                    Device
                  </UButton>
                </div>
                <div class="flex flex-wrap gap-2 mt-2 pl-6">
                  <UBadge
                    v-for="device in room.devices"
                    :key="device.id"
                    :color="statusColor(device.status)"
                    variant="subtle"
                    class="gap-1"
                  >
                    <UIcon :name="device.type === 'SENSOR' ? 'i-lucide-scan-search' : 'i-lucide-radio' " class="size-3.5" />
                    {{ deviceLabel(device) }} ({{ device.ip }})
                  </UBadge>
                </div>
              </div>
            </div>
          </div>
        </div>
      </UCard>
    </section>

    <UModal v-model:open="createZoneOpen" title="Crear zona">
      <template #body>
        <div class="space-y-3">
          <UFormField label="Nombre de la zona">
            <UInput v-model="zoneNameInput" placeholder="Ej: Hall Central" />
          </UFormField>
        </div>
      </template>
      <template #footer>
        <div class="flex justify-end gap-2 w-full">
          <UButton variant="ghost" color="neutral" @click="createZoneOpen = false">
            Cancelar
          </UButton>
          <UButton :loading="creatingZone" color="primary" @click="createZone">
            Guardar zona
          </UButton>
        </div>
      </template>
    </UModal>

    <UModal v-model:open="createSpaceOpen" title="Crear espacio">
      <template #body>
        <div class="space-y-3">
          <UFormField label="Nombre del espacio">
            <UInput v-model="spaceNameInput" placeholder="Ej: Camino Principal" />
          </UFormField>
        </div>
      </template>
      <template #footer>
        <div class="flex justify-end gap-2 w-full">
          <UButton variant="ghost" color="neutral" @click="createSpaceOpen = false">
            Cancelar
          </UButton>
          <UButton :loading="creatingSpace" color="primary" @click="createSpace">
            Guardar espacio
          </UButton>
        </div>
      </template>
    </UModal>

    <UModal v-model:open="createDeviceOpen" title="Crear dispositivo">
      <template #body>
        <div class="space-y-3">
          <UFormField label="IP del dispositivo">
            <UInput v-model="deviceIpInput" placeholder="Ej: 10.20.1.34" />
          </UFormField>

          <UFormField label="Tipo">
            <USelect
              v-model="deviceTypeInput"
              :items="[
                { label: 'SENSOR', value: 'SENSOR' },
                { label: 'ACTUATOR', value: 'ACTUATOR' }
              ]"
            />
          </UFormField>

          <UFormField label="Estado">
            <USwitch v-model="deviceStatusInput" />
            <p class="text-xs text-muted mt-1">
              {{ deviceStatusInput ? 'Online' : 'Offline' }}
            </p>
          </UFormField>
        </div>
      </template>
      <template #footer>
        <div class="flex justify-end gap-2 w-full">
          <UButton variant="ghost" color="neutral" @click="createDeviceOpen = false">
            Cancelar
          </UButton>
          <UButton :loading="creatingDevice" color="primary" @click="createDevice">
            Guardar dispositivo
          </UButton>
        </div>
      </template>
    </UModal>
  </div>
</template>
