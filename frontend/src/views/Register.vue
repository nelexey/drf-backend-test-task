<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600">
    <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Регистрация</h1>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
        {{ success }}
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Фамилия</label>
            <input v-model="form.last_name" type="text" required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
            <input v-model="form.first_name" type="text" required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Отчество</label>
          <input v-model="form.patronymic" type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <input v-model="form.password" type="password" required minlength="8"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Повтор пароля</label>
          <input v-model="form.password_confirm" type="password" required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
        </div>

        <button type="submit" :disabled="loading"
          class="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-medium">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="mt-6 text-center text-gray-600">
        Уже есть аккаунт? 
        <router-link to="/login" class="text-indigo-600 hover:underline font-medium">Войти</router-link>
      </p>
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
const success = ref('')
const form = ref({
  email: '',
  first_name: '',
  last_name: '',
  patronymic: '',
  password: '',
  password_confirm: ''
})

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
  if (form.value.password !== form.value.password_confirm) {
    error.value = 'Пароли не совпадают'
    loading.value = false
    return
  }

  try {
    await authAPI.register(form.value)
    success.value = 'Регистрация успешна! Перенаправление...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    const errors = e.response?.data
    if (errors) {
      error.value = Object.values(errors).flat().join(', ')
    } else {
      error.value = 'Ошибка регистрации'
    }
  } finally {
    loading.value = false
  }
}
</script>
