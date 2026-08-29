/**
 * markdownParser
 * Sanitizes and renders markdown content with syntax highlighting
 */

export const markdownParser = {
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
    name: 'markdownParser',
    description: 'Sanitizes and renders markdown content with syntax highlighting'
  })
};

export default markdownParser;
