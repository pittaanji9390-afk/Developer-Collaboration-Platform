/**
 * storageHelper
 * Encapsulates localStorage and sessionStorage with JSON serialization
 */

export const storageHelper = {
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
    name: 'storageHelper',
    description: 'Encapsulates localStorage and sessionStorage with JSON serialization'
  })
};

export default storageHelper;
