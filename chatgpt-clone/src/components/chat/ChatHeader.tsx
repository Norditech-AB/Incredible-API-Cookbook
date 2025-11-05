'use client';

import { Button } from '@/components/ui/button';
import { Plus, Settings, Moon, Sun } from 'lucide-react';
import { useState } from 'react';

interface ChatHeaderProps {
  onNewChat: () => void;
  onSettings: () => void;
}

export function ChatHeader({ onNewChat, onSettings }: ChatHeaderProps) {
  const [isDark, setIsDark] = useState(false);

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className="flex items-center justify-between p-4 border-b bg-background">
      <div className="flex items-center gap-2">
        <h1 className="text-xl font-bold">ChatGPT Clone</h1>
        <span className="text-sm text-muted-foreground">with Actions</span>
      </div>
      
      <div className="flex items-center gap-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          title="Toggle theme"
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onSettings}
          title="Settings"
        >
          <Settings className="w-4 h-4" />
        </Button>
        
        <Button onClick={onNewChat} className="gap-2">
          <Plus className="w-4 h-4" />
          New Chat
        </Button>
      </div>
    </div>
  );
}