import api from '../client';

/**
 * gpgKeysApi
 * GPG keys endpoints
 */
export const gpgKeysApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/users/keys/gpg', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/users/keys/gpg/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/users/keys/gpg', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/users/keys/gpg/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/users/keys/gpg/${id}`);
    return res.data;
  }
};

export default gpgKeysApi;
