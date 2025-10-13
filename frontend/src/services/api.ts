import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Для Django session authentication
});

// Request interceptor для добавления CSRF токена
apiClient.interceptors.request.use((config) => {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.getAttribute('value');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

// Response interceptor для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;

