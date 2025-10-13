import * as React from 'react';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  actions?: React.ReactNode;
  className?: string;
}

const Card: React.FC<CardProps> = ({
  children,
  title,
  actions,
  className = ''
}) => {
  return (
    <div className={`card ${className}`}>
      {(title || actions) && (
        <div className="flex items-center justify-between mb-4">
          {title && (
            <h3 className="text-lg font-semibold text-secondary-900">{title}</h3>
          )}
          {actions && (
            <div className="flex space-x-2">{actions}</div>
          )}
        </div>
      )}
      {children}
    </div>
  );
};

export default Card;

