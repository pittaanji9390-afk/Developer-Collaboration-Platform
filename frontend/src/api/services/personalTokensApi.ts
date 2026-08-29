import api from '../client';

/**
 * personalTokensApi
 * Personal access tokens endpoints
 */
export const personalTokensApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/auth/tokens', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/auth/tokens/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/auth/tokens', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/auth/tokens/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/auth/tokens/${id}`);
    return res.data;
  }
};

export default personalTokensApi;
