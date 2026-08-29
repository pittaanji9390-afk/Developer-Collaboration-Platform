import api from '../client';

/**
 * licenseComplianceApi
 * License compliance endpoints
 */
export const licenseComplianceApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/security/licenses', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/security/licenses/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/security/licenses', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/security/licenses/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/security/licenses/${id}`);
    return res.data;
  }
};

export default licenseComplianceApi;
