/**
 * permissionsEvaluator
 * Evaluates client-side RBAC permissions for UI action buttons
 */

export const permissionsEvaluator = {
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
    name: 'permissionsEvaluator',
    description: 'Evaluates client-side RBAC permissions for UI action buttons'
  })
};

export default permissionsEvaluator;
