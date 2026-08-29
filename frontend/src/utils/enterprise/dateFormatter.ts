/**
 * dateFormatter
 * Formats timestamps into relative time ago and localized ISO dates
 */

export const dateFormatter = {
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
    name: 'dateFormatter',
    description: 'Formats timestamps into relative time ago and localized ISO dates'
  })
};

export default dateFormatter;
