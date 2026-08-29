import api from '../client';

/**
 * secretScanningApi
 * Secret scanning alerts endpoints
 */
export const secretScanningApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/security/secrets', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/security/secrets/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/security/secrets', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/security/secrets/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/security/secrets/${id}`);
    return res.data;
  }
};

export default secretScanningApi;
