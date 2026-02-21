import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center space-y-3 p-6">
      <Loader2 className="w-8 h-8 text-green-600 dark:text-green-500 animate-spin" />
      <p className="text-gray-600 dark:text-gray-400 font-medium">{message}</p>
    </div>
  );
};

export default LoadingSpinner;
