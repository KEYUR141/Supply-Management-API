import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',   // ✅ matches Django backend
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add interceptor to include JWT access token in requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api

