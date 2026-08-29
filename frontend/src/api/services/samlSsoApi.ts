import api from '../client';

/**
 * samlSsoApi
 * SAML SSO endpoints
 */
export const samlSsoApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/auth/saml', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/auth/saml/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/auth/saml', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/auth/saml/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/auth/saml/${id}`);
    return res.data;
  }
};

export default samlSsoApi;
