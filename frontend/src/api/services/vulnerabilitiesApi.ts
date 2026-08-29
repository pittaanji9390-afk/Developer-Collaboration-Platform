import api from '../client';

/**
 * vulnerabilitiesApi
 * CVE vulnerability endpoints
 */
export const vulnerabilitiesApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/security/vulnerabilities', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/security/vulnerabilities/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/security/vulnerabilities', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/security/vulnerabilities/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/security/vulnerabilities/${id}`);
    return res.data;
  }
};

export default vulnerabilitiesApi;
