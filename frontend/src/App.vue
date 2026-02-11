<template>
  <div class="min-h-screen">
    <nav v-if="isAuthenticated" class="bg-indigo-600 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-6">
          <span class="text-xl font-bold">AIHunt</span>
          <router-link to="/home" class="hover:text-indigo-200">Главная</router-link>
          <router-link v-if="isAdmin" to="/admin" class="hover:text-indigo-200">Админ</router-link>
        </div>
        <div class="flex items-center space-x-4">
          <span class="text-sm">{{ user?.email }} ({{ user?.role }})</span>
          <button @click="logout" class="bg-indigo-500 hover:bg-indigo-400 px-3 py-1 rounded text-sm">
            Выйти
          </button>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from './api'

const router = useRouter()

const user = computed(() => {
  const userData = localStorage.getItem('user')
  return userData ? JSON.parse(userData) : null
})

const isAuthenticated = computed(() => !!localStorage.getItem('token'))
const isAdmin = computed(() => user.value?.role === 'admin')

const logout = async () => {
  try {
    await authAPI.logout()
  } catch (e) {}
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>
