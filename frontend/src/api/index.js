import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (data) => api.post('/auth/login/', data),
  register: (data) => api.post('/auth/register/', data),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.patch('/auth/profile/', data),
  deleteAccount: () => api.delete('/auth/profile/')
}

export const articlesAPI = {
  getAll: () => api.get('/articles/'),
  create: (data) => api.post('/articles/', data),
  update: (id, data) => api.put(`/articles/${id}/`, data),
  delete: (id) => api.delete(`/articles/${id}/`)
}

export const accessAPI = {
  getRoles: () => api.get('/access/roles/'),
  getUsers: () => api.get('/access/users/'),
  assignRole: (data) => api.post('/access/user-roles/', data)
}

export default api
