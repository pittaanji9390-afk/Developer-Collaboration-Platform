import api from '../client';

/**
 * labelsApi
 * Repository labels endpoints
 */
export const labelsApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/labels', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/labels/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/labels', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/labels/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/labels/${id}`);
    return res.data;
  }
};

export default labelsApi;
