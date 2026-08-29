/**
 * gitRefParser
 * Parses refs/heads/*, refs/tags/*, and refs/pull/* reference strings
 */

export const gitRefParser = {
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
    name: 'gitRefParser',
    description: 'Parses refs/heads/*, refs/tags/*, and refs/pull/* reference strings'
  })
};

export default gitRefParser;
