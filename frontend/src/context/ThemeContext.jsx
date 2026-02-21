import { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

const getInitialTheme = () => {
  if (typeof window !== 'undefined') {
    try {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme) {
        return savedTheme === 'dark';
      }
    } catch (error) {
      console.error('Error reading theme from localStorage:', error);
    }
  }
  return true; // Default to dark mode
};

export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(getInitialTheme);
  const [mounted, setMounted] = useState(false);

  // Apply theme class immediately on mount
  useEffect(() => {
    setMounted(true);
    const initialDark = getInitialTheme();
    
    if (initialDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  // Update document class and localStorage when theme changes
  useEffect(() => {
    if (!mounted) return;
    
    if (isDark) {
      document.documentElement.classList.add('dark');
      try {
        localStorage.setItem('theme', 'dark');
      } catch (error) {
        console.error('Error saving theme to localStorage:', error);
      }
    } else {
      document.documentElement.classList.remove('dark');
      try {
        localStorage.setItem('theme', 'light');
      } catch (error) {
        console.error('Error saving theme to localStorage:', error);
      }
    }
  }, [isDark, mounted]);

  const toggleTheme = () => {
    setIsDark(prev => !prev);
  };

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
