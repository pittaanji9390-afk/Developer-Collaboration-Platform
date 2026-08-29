/**
 * themeManager
 * Manages system, dark, and light color theme preferences
 */

export const themeManager = {
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
    name: 'themeManager',
    description: 'Manages system, dark, and light color theme preferences'
  })
};

export default themeManager;
