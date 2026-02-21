import { Download, Moon, Sun } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';

const Header = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-emerald-950 border-b border-gray-200 dark:border-emerald-900 sticky top-0 z-50 transition-colors duration-300">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2.5 hover:opacity-70 transition-opacity group">
            <div className="bg-green-600 p-2 rounded-lg">
              <Download className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">Video Downloader</h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">YouTube • Facebook • Instagram • TikTok</p>
            </div>
          </Link>

          {/* Theme Toggle Button */}
          <button
            onClick={toggleTheme}
            className="p-2.5 rounded-lg bg-gray-100 dark:bg-emerald-900 hover:bg-gray-200 dark:hover:bg-emerald-800 text-gray-700 dark:text-gray-300 transition-colors"
            aria-label="Toggle theme"
          >
            {isDark ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
