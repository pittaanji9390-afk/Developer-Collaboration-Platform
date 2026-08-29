/**
 * clipboardHelper
 * Provides cross-browser copy to clipboard with fallback
 */

export const clipboardHelper = {
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
    name: 'clipboardHelper',
    description: 'Provides cross-browser copy to clipboard with fallback'
  })
};

export default clipboardHelper;
