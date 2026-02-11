<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-8">Панель администратора</h1>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
      {{ success }}
    </div>

    <div class="grid gap-8 lg:grid-cols-2">
      <div class="bg-white rounded-xl shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">Пользователи</h2>
        <div v-if="loading" class="text-gray-500">Загрузка...</div>
        <div v-else class="space-y-3">
          <div v-for="u in users" :key="u.id" 
            class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <div>
              <p class="font-medium">{{ u.email }}</p>
              <p class="text-sm text-gray-500">{{ u.last_name }} {{ u.first_name }}</p>
            </div>
            <div class="flex items-center space-x-2">
              <span class="px-2 py-1 text-xs rounded-full"
                :class="{
                  'bg-red-100 text-red-800': u.role === 'admin',
                  'bg-yellow-100 text-yellow-800': u.role === 'moderator',
                  'bg-gray-100 text-gray-800': u.role === 'user'
                }">
                {{ u.role }}
              </span>
              <select v-model="selectedRoles[u.id]" @change="assignRole(u.id)"
                class="text-sm border border-gray-300 rounded px-2 py-1">
                <option value="">Изменить роль</option>
                <option v-for="role in roles" :key="role.id" :value="role.name">
                  {{ role.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">Роли и права</h2>
        <div v-for="role in roles" :key="role.id" class="mb-4 p-3 bg-gray-50 rounded-lg">
          <h3 class="font-medium text-lg">{{ role.name }}</h3>
          <p class="text-sm text-gray-500 mb-2">{{ role.description }}</p>
          <div class="flex flex-wrap gap-1">
            <span v-for="perm in role.permissions" :key="perm.id"
              class="px-2 py-0.5 bg-indigo-100 text-indigo-800 text-xs rounded">
              {{ perm.resource_name }}:{{ perm.action }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { accessAPI } from '../api'

const users = ref([])
const roles = ref([])
const loading = ref(true)
const error = ref('')
const success = ref('')
const selectedRoles = reactive({})

const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [usersRes, rolesRes] = await Promise.all([
      accessAPI.getUsers(),
      accessAPI.getRoles()
    ])
    users.value = usersRes.data
    roles.value = rolesRes.data
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка загрузки данных'
  } finally {
    loading.value = false
  }
}

const assignRole = async (userId) => {
  const roleName = selectedRoles[userId]
  if (!roleName) return
  
  error.value = ''
  success.value = ''
  
  try {
    await accessAPI.assignRole({ user_id: userId, role_name: roleName })
    success.value = 'Роль успешно назначена'
    selectedRoles[userId] = ''
    await loadData()
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка назначения роли'
  }
}

onMounted(loadData)
</script>
