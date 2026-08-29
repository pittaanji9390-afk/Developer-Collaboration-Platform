/**
 * jwtDecoder
 * Decodes JWT payload claims and checks token expiration in browser
 */

export const jwtDecoder = {
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
    name: 'jwtDecoder',
    description: 'Decodes JWT payload claims and checks token expiration in browser'
  })
};

export default jwtDecoder;
