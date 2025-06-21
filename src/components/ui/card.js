import React from 'react';

export const Card = ({ children, className = "", ...props }) => {
  return (
    <div className={`bg-white shadow-lg rounded-2xl overflow-hidden ${className}`} {...props}>
      {children}
    </div>
  );
};

export const CardContent = ({ children, className = "", ...props }) => {
  return (
    <div className={`p-4 ${className}`} {...props}>
      {children}
    </div>
  );
}; 