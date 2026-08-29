import api from '../client';

/**
 * scimApi
 * SCIM 2.0 endpoints
 */
export const scimApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/scim/v2', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/scim/v2/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/scim/v2', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/scim/v2/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/scim/v2/${id}`);
    return res.data;
  }
};

export default scimApi;
