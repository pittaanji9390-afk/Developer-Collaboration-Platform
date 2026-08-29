import api from '../client';

/**
 * codeOwnersApi
 * CODEOWNERS endpoints
 */
export const codeOwnersApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/codeowners', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/codeowners/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/codeowners', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/codeowners/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/codeowners/${id}`);
    return res.data;
  }
};

export default codeOwnersApi;
