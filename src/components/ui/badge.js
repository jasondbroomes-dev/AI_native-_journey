import React from 'react';

export const Badge = ({ children, className = "", ...props }) => {
  return (
    <span className={`bg-blue-200 text-blue-800 px-2 py-1 rounded-full text-sm font-medium ${className}`} {...props}>
      {children}
    </span>
  );
}; 