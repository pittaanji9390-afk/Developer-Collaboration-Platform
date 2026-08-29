import api from '../client';

/**
 * rebaseApi
 * Git rebase endpoints
 */
export const rebaseApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/git/rebase', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/git/rebase/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/git/rebase', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/git/rebase/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/git/rebase/${id}`);
    return res.data;
  }
};

export default rebaseApi;
