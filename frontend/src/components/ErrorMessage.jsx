import { AlertCircle, XCircle } from 'lucide-react';

const ErrorMessage = ({ message, onClose }) => {
  return (
    <div className="bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-start space-x-3">
      <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-500 flex-shrink-0 mt-0.5" />
      <div className="flex-grow">
        <h3 className="font-semibold text-red-800 dark:text-red-400">Error</h3>
        <p className="text-red-700 dark:text-red-500 text-sm mt-1">{message}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-red-400 dark:text-red-500 hover:text-red-600 dark:hover:text-red-300 transition-colors"
          aria-label="Close error message"
        >
          <XCircle className="w-5 h-5" />
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
