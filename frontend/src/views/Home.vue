<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Статьи</h1>
      <button v-if="canCreate" @click="showCreateModal = true"
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 font-medium">
        + Новая статья
      </button>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-500">Загрузка...</div>

    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="article in articles" :key="article.id" 
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
        <h2 class="text-xl font-semibold text-gray-800 mb-2">{{ article.title }}</h2>
        <p class="text-gray-600 mb-4">{{ article.content }}</p>
        <div class="flex justify-between items-center text-sm">
          <span class="text-gray-400">{{ article.author }}</span>
          <div v-if="canModify" class="space-x-2">
            <button @click="editArticle(article)" class="text-indigo-600 hover:underline">Редактировать</button>
            <button @click="deleteArticle(article.id)" class="text-red-600 hover:underline">Удалить</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && articles.length === 0" class="text-center py-12 text-gray-500">
      Статей пока нет
    </div>

    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg">
        <h2 class="text-xl font-bold mb-4">{{ editingArticle ? 'Редактировать' : 'Новая статья' }}</h2>
        <form @submit.prevent="saveArticle" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Заголовок</label>
            <input v-model="articleForm.title" type="text" required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Содержание</label>
            <textarea v-model="articleForm.content" rows="4" required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"></textarea>
          </div>
          <div class="flex justify-end space-x-3">
            <button type="button" @click="closeModal" class="px-4 py-2 text-gray-600 hover:text-gray-800">
              Отмена
            </button>
            <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
              Сохранить
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { articlesAPI } from '../api'

const articles = ref([])
const loading = ref(true)
const error = ref('')
const showCreateModal = ref(false)
const editingArticle = ref(null)
const articleForm = ref({ title: '', content: '' })

const user = computed(() => {
  const userData = localStorage.getItem('user')
  return userData ? JSON.parse(userData) : null
})

const canCreate = computed(() => ['admin', 'moderator'].includes(user.value?.role))
const canModify = computed(() => ['admin', 'moderator'].includes(user.value?.role))

const loadArticles = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await articlesAPI.getAll()
    articles.value = data
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка загрузки статей'
  } finally {
    loading.value = false
  }
}

const editArticle = (article) => {
  editingArticle.value = article
  articleForm.value = { title: article.title, content: article.content }
  showCreateModal.value = true
}

const closeModal = () => {
  showCreateModal.value = false
  editingArticle.value = null
  articleForm.value = { title: '', content: '' }
}

const saveArticle = async () => {
  try {
    if (editingArticle.value) {
      await articlesAPI.update(editingArticle.value.id, articleForm.value)
    } else {
      await articlesAPI.create(articleForm.value)
    }
    closeModal()
    await loadArticles()
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка сохранения'
  }
}

const deleteArticle = async (id) => {
  if (!confirm('Удалить статью?')) return
  try {
    await articlesAPI.delete(id)
    await loadArticles()
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка удаления'
  }
}

onMounted(loadArticles)
</script>
