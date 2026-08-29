import api from '../client';

/**
 * milestonesApi
 * Milestone sprint endpoints
 */
export const milestonesApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/milestones', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/milestones/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/milestones', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/milestones/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/milestones/${id}`);
    return res.data;
  }
};

export default milestonesApi;
