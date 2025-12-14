/**
 * API Service
 * VULNERABLE: No CSRF token handling, XSS in search results
 */

import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Include cookies
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/api/v1/auth/login', { email, password })
    return response.data
  },
  
  logout: async () => {
    const response = await api.post('/api/v1/auth/logout')
    return response.data
  },
  
  getToken: async (email: string, password: string) => {
    const response = await api.post('/api/v1/auth/token', { email, password })
    return response.data
  },
  
  resetPassword: async (email: string) => {
    const response = await api.post('/api/v1/auth/reset-password', { email })
    return response.data
  },
}

// Courses API
export const coursesAPI = {
  getAll: async (filter?: string) => {
    const params = filter ? { filter } : {}
    const response = await api.get('/api/v1/courses', { params })
    return response.data
  },
  
  getById: async (id: number) => {
    const response = await api.get(`/api/v1/courses/${id}`)
    return response.data
  },
  
  search: async (query: string) => {
    // VULNERABLE: XSS - query will be reflected in results
    const response = await api.get('/api/v1/courses', {
      params: { filter: `title LIKE '%${query}%'` }
    })
    return response.data
  },
}

// Enrollments API
export const enrollmentsAPI = {
  create: async (courseId: number, studentId: number) => {
    // FIX: Instead of sending a JSON object {course_id, student_id},
    // we send URLSearchParams which mimics a standard HTML Form.
    const formData = new URLSearchParams();
    formData.append('course_id', courseId.toString());
    formData.append('student_id', studentId.toString());

    const response = await api.post('/api/v1/enrollments', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  },
  
  delete: async (id: number) => {
    const response = await api.delete(`/api/v1/enrollments/${id}`)
    return response.data
  },
  
  getByUser: async (userId: number) => {
    const response = await api.get('/api/v1/enrollments', {
      params: { user_id: userId }
    })
    return response.data
  },
}

// Admin API
export const adminAPI = {
  createCourse: async (courseData: any) => {
    // VULNERABLE: Trust Boundary Violation
    // We manually add a static secret header that the backend blindly trusts.
    const response = await api.post('/api/v1/admin/courses', courseData, {
      headers: { 'X-Admin-Access': 'SuperSecretAdmin123' }
    })
    return response.data
  },

  
}
export const auditAPI = {
  getLogs: async () => {
    // VULNERABLE: Broken Access Control
    // This should be restricted, but any authenticated user can hit this.
    const response = await api.get('/api/v1/audit');
    return response.data;
  }
}


export default api

