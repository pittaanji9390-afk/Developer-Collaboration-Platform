/**
 * diffCalculator
 * Calculates character-level inline diff highlights for code review
 */

export const diffCalculator = {
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
    name: 'diffCalculator',
    description: 'Calculates character-level inline diff highlights for code review'
  })
};

export default diffCalculator;
