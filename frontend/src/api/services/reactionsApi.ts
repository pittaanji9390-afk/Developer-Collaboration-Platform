import api from '../client';

/**
 * reactionsApi
 * Reactions endpoints
 */
export const reactionsApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/reactions', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/reactions/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/reactions', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/reactions/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/reactions/${id}`);
    return res.data;
  }
};

export default reactionsApi;
