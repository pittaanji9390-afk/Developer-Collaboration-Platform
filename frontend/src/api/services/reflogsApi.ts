import api from '../client';

/**
 * reflogsApi
 * Git reflogs endpoints
 */
export const reflogsApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/git/reflogs', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/git/reflogs/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/git/reflogs', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/git/reflogs/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/git/reflogs/${id}`);
    return res.data;
  }
};

export default reflogsApi;
