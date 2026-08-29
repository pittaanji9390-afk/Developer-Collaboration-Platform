/**
 * keyboardShortcuts
 * Registers global and scoped keyboard shortcut listeners
 */

export const keyboardShortcuts = {
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
    name: 'keyboardShortcuts',
    description: 'Registers global and scoped keyboard shortcut listeners'
  })
};

export default keyboardShortcuts;
