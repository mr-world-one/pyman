import { apiClient } from './config'

export const authService = {
    async login(email, password) {
        try {
            const response = await apiClient.post('/auth/login', {
                username: email,
                password: password
            })
            if (response.data.access_token) {
                localStorage.setItem('token', response.data.access_token)
                // Update Authorization header for future requests
                apiClient.defaults.headers.common['Authorization'] = 
                    `Bearer ${response.data.access_token}`
            }
            return response.data
        } catch (error) {
            console.error('Login error:', error.response?.data || error.message)
            throw error
        }
    },

    async register(userData) {
        try {
            const response = await apiClient.post('/auth/register', {
                email: userData.email,
                password: userData.password,
                name: userData.name
            })
            if (response.data.access_token) {
                localStorage.setItem('token', response.data.access_token)
                apiClient.defaults.headers.common['Authorization'] = 
                    `Bearer ${response.data.access_token}`
            }
            return response.data
        } catch (error) {
            console.error('Registration error:', error.response?.data || error.message)
            throw error
        }
    },

    async getCurrentUser() {
        try {
            const token = localStorage.getItem('token')
            if (!token) {
                throw new Error('No authentication token found')
            }
            const response = await apiClient.get('/auth/users/me')
            return response.data
        } catch (error) {
            console.error('Get current user error:', error.response?.data || error.message)
            throw error
        }
    },

    logout() {
        localStorage.removeItem('token')
        delete apiClient.defaults.headers.common['Authorization']
    }
}