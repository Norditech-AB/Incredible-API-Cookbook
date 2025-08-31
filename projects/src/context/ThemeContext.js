import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  const [animations, setAnimations] = useState(true);
  const [soundEffects, setSoundEffects] = useState(false);

  useEffect(() => {
    // Load theme preferences from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedAnimations = localStorage.getItem('animations') !== 'false';
    const savedSoundEffects = localStorage.getItem('soundEffects') === 'true';
    
    setTheme(savedTheme);
    setAnimations(savedAnimations);
    setSoundEffects(savedSoundEffects);
  }, []);

  useEffect(() => {
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem('animations', animations);
  }, [animations]);

  useEffect(() => {
    localStorage.setItem('soundEffects', soundEffects);
  }, [soundEffects]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const toggleAnimations = () => {
    setAnimations(prev => !prev);
  };

  const toggleSoundEffects = () => {
    setSoundEffects(prev => !prev);
  };

  const value = {
    theme,
    animations,
    soundEffects,
    toggleTheme,
    toggleAnimations,
    toggleSoundEffects,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};