import api from '../client';

/**
 * twoFactorApi
 * Two factor authentication endpoints
 */
export const twoFactorApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/auth/2fa', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/auth/2fa/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/auth/2fa', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/auth/2fa/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/auth/2fa/${id}`);
    return res.data;
  }
};

export default twoFactorApi;
