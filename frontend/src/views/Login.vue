<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600">
    <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Вход в систему</h1>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <input v-model="form.password" type="password" required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
        </div>

        <button type="submit" :disabled="loading"
          class="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-medium">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <p class="mt-6 text-center text-gray-600">
        Нет аккаунта? 
        <router-link to="/register" class="text-indigo-600 hover:underline font-medium">Регистрация</router-link>
      </p>

      <div class="mt-6 p-4 bg-gray-50 rounded-lg text-sm text-gray-600">
        <p class="font-medium mb-2">Тестовые аккаунты:</p>
        <p>admin@test.com / admin123</p>
        <p>moderator@test.com / moder123</p>
        <p>user@test.com / user1234</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const form = ref({ email: '', password: '' })

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await authAPI.login(form.value)
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data.user))
    router.push('/home')
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}
</script>
