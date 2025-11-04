import React from 'react';
import './App.css';
import ChatApp from './components/ChatApp';
import { ThemeProvider } from './context/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <div className="App">
        <ChatApp />
      </div>
    </ThemeProvider>
  );
}

export default App;
