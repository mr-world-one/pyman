import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
});

apiClient.interceptors.request.use(
  (config) => {
    console.log('Request:', config);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    console.log('Response:', response);
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(email, password) {
    try {
      console.log('Sending login request with:', { email, password });
      const response = await apiClient.post('/auth/auth/login', {
        email,
        password
      });
      console.log('Login response:', response.data);
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      } else {
        throw new Error('No access token in response');
      }
      return response.data;
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      throw error;
    }
  },

  async register(userData) {
    try {
      console.log('Sending register request with:', userData);
      const response = await apiClient.post('/auth/auth/register', {
        email: userData.email,
        name: userData.name,
        password: userData.password
      });
      console.log('Register response:', response.data);
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      }
      return response.data;
    } catch (error) {
      console.error('Registration error:', error.response?.data || error.message);
      throw error;
    }
  },

  async getCurrentUser() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      console.log('Checking current user with token:', token);
      const response = await apiClient.get('/auth/users/me');
      console.log('Current user response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Get current user error:', error.response?.data || error.message);
      throw error;
    }
  },

  logout() {
    localStorage.removeItem('token');
    delete apiClient.defaults.headers.common['Authorization'];
    window.location.href = '/signin';
  }
};
