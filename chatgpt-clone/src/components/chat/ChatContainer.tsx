'use client';

import { useChat } from '@/hooks/useChat';
import { ChatHeader } from './ChatHeader';
import { ChatSidebar } from './ChatSidebar';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { useState } from 'react';

export function ChatContainer() {
  const {
    conversations,
    currentConversation,
    currentConversationId,
    isLoading,
    error,
    createNewConversation,
    selectConversation,
    deleteConversation,
    sendMessage,
  } = useChat();

  const [showSettings, setShowSettings] = useState(false);

  const handleNewChat = () => {
    createNewConversation();
  };

  const handleSettings = () => {
    setShowSettings(!showSettings);
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <ChatSidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={selectConversation}
        onDeleteConversation={deleteConversation}
        onNewChat={handleNewChat}
      />
      
      <div className="flex-1 flex flex-col">
        <ChatHeader
          onNewChat={handleNewChat}
          onSettings={handleSettings}
        />
        
        <div className="flex-1 overflow-y-auto p-4">
          {error && (
            <div className="mb-4 p-3 bg-destructive/10 border border-destructive/20 rounded-md">
              <p className="text-destructive text-sm">{error}</p>
            </div>
          )}
          
          {!currentConversation ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <h2 className="text-2xl font-bold mb-2">Welcome to ChatGPT Clone</h2>
                <p className="text-muted-foreground mb-4">
                  Start a new conversation to begin chatting with AI that can take actions!
                </p>
                <button
                  onClick={handleNewChat}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                  Start New Chat
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {currentConversation.messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  message={message}
                />
              ))}
              
              {isLoading && (
                <MessageBubble
                  message={{
                    id: 'typing',
                    role: 'assistant',
                    content: '',
                    timestamp: new Date(),
                  }}
                  isTyping={true}
                />
              )}
            </div>
          )}
        </div>
        
        <ChatInput
          onSendMessage={sendMessage}
          isLoading={isLoading}
          disabled={!currentConversationId}
        />
      </div>
    </div>
  );
}