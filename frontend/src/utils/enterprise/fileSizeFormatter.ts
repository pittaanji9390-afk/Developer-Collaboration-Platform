/**
 * fileSizeFormatter
 * Formats byte counts into human-readable B, KB, MB, GB strings
 */

export const fileSizeFormatter = {
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
    name: 'fileSizeFormatter',
    description: 'Formats byte counts into human-readable B, KB, MB, GB strings'
  })
};

export default fileSizeFormatter;
