import { apiClient } from './config'

export const authService = {
    async login(email, password) {
        const response = await apiClient.post('/token', {
            username: email,
            password: password
        })
        return response.data
    },

    async register(userData) {
        const response = await apiClient.post('/users', userData)
        return response.data
    },

    async getCurrentUser() {
        const response = await apiClient.get('/users/me')
        return response.data
    }
}