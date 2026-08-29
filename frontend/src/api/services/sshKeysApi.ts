import api from '../client';

/**
 * sshKeysApi
 * SSH keys endpoints
 */
export const sshKeysApi = {
  list: async (params?: Record<string, any>) => {
    const res = await api.get('/users/keys/ssh', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await api.get(`/users/keys/ssh/${id}`);
    return res.data;
  },

  create: async (data: Record<string, any>) => {
    const res = await api.post('/users/keys/ssh', data);
    return res.data;
  },

  update: async (id: string, data: Record<string, any>) => {
    const res = await api.post(`/users/keys/ssh/${id}`, data);
    return res.data;
  },

  delete: async (id: string) => {
    const res = await api.delete(`/users/keys/ssh/${id}`);
    return res.data;
  }
};

export default sshKeysApi;
