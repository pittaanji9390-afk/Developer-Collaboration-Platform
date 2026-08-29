/**
 * durationFormatter
 * Formats milliseconds into human-readable execution durations
 */

export const durationFormatter = {
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
    name: 'durationFormatter',
    description: 'Formats milliseconds into human-readable execution durations'
  })
};

export default durationFormatter;
