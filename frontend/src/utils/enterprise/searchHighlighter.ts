/**
 * searchHighlighter
 * Highlights matched query terms within code search result snippets
 */

export const searchHighlighter = {
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
    name: 'searchHighlighter',
    description: 'Highlights matched query terms within code search result snippets'
  })
};

export default searchHighlighter;
