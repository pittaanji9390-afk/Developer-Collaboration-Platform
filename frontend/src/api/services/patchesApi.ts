import api from '../client';

/**
 * patchesApi
 * Patches endpoints
 */
export const patchesApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/git/patches', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/git/patches/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/git/patches', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/git/patches/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/git/patches/${id}`);
    return res.data;
  }
};

export default patchesApi;
