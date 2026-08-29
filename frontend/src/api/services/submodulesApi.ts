import api from '../client';

/**
 * submodulesApi
 * Submodules endpoints
 */
export const submodulesApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/git/submodules', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/git/submodules/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/git/submodules', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/git/submodules/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/git/submodules/${id}`);
    return res.data;
  }
};

export default submodulesApi;
