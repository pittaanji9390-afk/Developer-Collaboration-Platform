import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Skeleton
 * Animated loading skeleton placeholder
 */
export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  children,
  className,
  variant = 'default',
  size = 'md',
  isLoading = false,
  ...props
}) => {
  const baseClasses = 'transition-all duration-150 ease-in-out';
  
  return (
    <div
      className={twMerge(clsx(baseClasses, className))}
      data-testid="skeleton"
      {...props}
    >
      {isLoading ? (
        <div className="flex items-center justify-center p-2">
          <span className="w-4 h-4 border-2 border-forge-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        children
      )}
    </div>
  );
};

export default Skeleton;
