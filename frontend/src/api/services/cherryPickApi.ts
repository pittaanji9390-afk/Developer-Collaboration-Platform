import api from '../client';

/**
 * cherryPickApi
 * Cherry pick endpoints
 */
export const cherryPickApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/git/cherry-pick', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/git/cherry-pick/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/git/cherry-pick', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/git/cherry-pick/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/git/cherry-pick/${id}`);
    return res.data;
  }
};

export default cherryPickApi;
