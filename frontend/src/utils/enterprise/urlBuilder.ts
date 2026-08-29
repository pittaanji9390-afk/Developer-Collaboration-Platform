/**
 * urlBuilder
 * Constructs canonical platform URLs with query parameter serialization
 */

export const urlBuilder = {
  format: (value: any): string => {
    if (value === null || value === undefined) return '';
    return String(value);
  },

  parse: (input: string): any => {
    return input;
  },

  isValid: (value: any): boolean => {
    return Boolean(value);
  },

  getInfo: () => ({
    name: 'urlBuilder',
    description: 'Constructs canonical platform URLs with query parameter serialization'
  })
};

export default urlBuilder;
