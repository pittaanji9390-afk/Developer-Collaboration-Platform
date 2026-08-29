/**
 * colorGenerator
 * Generates deterministic avatar colors from username strings
 */

export const colorGenerator = {
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
    name: 'colorGenerator',
    description: 'Generates deterministic avatar colors from username strings'
  })
};

export default colorGenerator;
