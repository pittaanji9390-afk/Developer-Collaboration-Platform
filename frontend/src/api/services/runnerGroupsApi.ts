import api from '../client';

/**
 * runnerGroupsApi
 * Runner groups endpoints
 */
export const runnerGroupsApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/runner-groups', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/runner-groups/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/runner-groups', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/runner-groups/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/runner-groups/${id}`);
    return res.data;
  }
};

export default runnerGroupsApi;
