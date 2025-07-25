import React from 'react';
import { AlertCircle, Wifi, WifiOff } from 'lucide-react';

interface ConnectionStatusProps {
  isConnected: boolean;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ isConnected }) => {
  if (isConnected) {
    return (
      <div className="flex items-center space-x-2 text-green-600 bg-green-50 px-3 py-2 rounded-lg">
        <Wifi className="w-4 h-4" />
        <span className="text-sm font-medium">Conectado</span>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-2 text-red-600 bg-red-50 px-3 py-2 rounded-lg">
      <WifiOff className="w-4 h-4" />
      <span className="text-sm font-medium">Desconectado</span>
    </div>
  );
};

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  size = 'md', 
  className = '' 
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  return (
    <div className={`animate-spin ${sizeClasses[size]} ${className}`}>
      <div className="border-2 border-current border-t-transparent rounded-full w-full h-full" />
    </div>
  );
};

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ 
  message, 
  onRetry, 
  className = '' 
}) => {
  return (
    <div className={`flex items-center space-x-3 text-red-600 bg-red-50 border border-red-200 rounded-lg p-4 ${className}`}>
      <AlertCircle className="w-5 h-5 flex-shrink-0" />
      <div className="flex-1">
        <p className="text-sm font-medium">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-sm font-medium hover:underline"
        >
          Reintentar
        </button>
      )}
    </div>
  );
};

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  action,
  className = ''
}) => {
  return (
    <div className={`text-center py-12 ${className}`}>
      {icon && (
        <div className="mx-auto w-16 h-16 text-gray-300 mb-4">
          {icon}
        </div>
      )}
      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
      {description && (
        <p className="text-gray-500 mb-6">{description}</p>
      )}
      {action && action}
    </div>
  );
};
