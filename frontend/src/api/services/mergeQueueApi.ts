import api from '../client';

/**
 * mergeQueueApi
 * Merge train queue endpoints
 */
export const mergeQueueApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/merge-queue', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/merge-queue/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/merge-queue', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/merge-queue/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/merge-queue/${id}`);
    return res.data;
  }
};

export default mergeQueueApi;
