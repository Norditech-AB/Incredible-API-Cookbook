'use client';

import { useState, useCallback } from 'react';
import { Message, Conversation, Action } from '@/types/chat';

export function useChat() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createNewConversation = useCallback(() => {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    setConversations(prev => [newConversation, ...prev]);
    setCurrentConversationId(newConversation.id);
    setError(null);
    
    return newConversation.id;
  }, []);

  const selectConversation = useCallback((id: string) => {
    setCurrentConversationId(id);
    setError(null);
  }, []);

  const deleteConversation = useCallback((id: string) => {
    setConversations(prev => prev.filter(conv => conv.id !== id));
    if (currentConversationId === id) {
      setCurrentConversationId(null);
    }
  }, [currentConversationId]);

  const addMessage = useCallback((conversationId: string, message: Message) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id === conversationId) {
        const updatedConv = {
          ...conv,
          messages: [...conv.messages, message],
          updatedAt: new Date(),
        };
        
        // Update title if it's the first user message
        if (conv.messages.length === 0 && message.role === 'user') {
          updatedConv.title = message.content.slice(0, 50) + (message.content.length > 50 ? '...' : '');
        }
        
        return updatedConv;
      }
      return conv;
    }));
  }, []);

  const updateMessage = useCallback((conversationId: string, messageId: string, updates: Partial<Message>) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id === conversationId) {
        return {
          ...conv,
          messages: conv.messages.map(msg => 
            msg.id === messageId ? { ...msg, ...updates } : msg
          ),
          updatedAt: new Date(),
        };
      }
      return conv;
    }));
  }, []);

  const addActionToMessage = useCallback((conversationId: string, messageId: string, action: Action) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id === conversationId) {
        return {
          ...conv,
          messages: conv.messages.map(msg => {
            if (msg.id === messageId) {
              return {
                ...msg,
                actions: [...(msg.actions || []), action],
              };
            }
            return msg;
          }),
          updatedAt: new Date(),
        };
      }
      return conv;
    }));
  }, []);

  const updateAction = useCallback((conversationId: string, messageId: string, actionId: string, updates: Partial<Action>) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id === conversationId) {
        return {
          ...conv,
          messages: conv.messages.map(msg => {
            if (msg.id === messageId) {
              return {
                ...msg,
                actions: msg.actions?.map(action => 
                  action.id === actionId ? { ...action, ...updates } : action
                ) || [],
              };
            }
            return msg;
          }),
          updatedAt: new Date(),
        };
      }
      return conv;
    }));
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!currentConversationId) {
      createNewConversation();
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    addMessage(currentConversationId, userMessage);
    setIsLoading(true);
    setError(null);

    try {
      const currentConv = conversations.find(c => c.id === currentConversationId);
      const messages = [
        ...(currentConv?.messages || []),
        userMessage,
      ].map(msg => ({
        role: msg.role,
        content: msg.content,
      }));

      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.message.content,
        timestamp: new Date(),
      };

      addMessage(currentConversationId, assistantMessage);

      // Add action if present
      if (data.action) {
        const action: Action = {
          id: Date.now().toString(),
          name: data.action.name,
          description: `Executed ${data.action.name}`,
          parameters: data.action.parameters,
          result: typeof data.action.result === 'string' 
            ? data.action.result 
            : JSON.stringify(data.action.result, null, 2),
          status: data.action.success ? 'completed' : 'failed',
        };

        addActionToMessage(currentConversationId, assistantMessage.id, action);
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  }, [currentConversationId, conversations, createNewConversation, addMessage, addActionToMessage]);

  const currentConversation = conversations.find(c => c.id === currentConversationId);

  return {
    conversations,
    currentConversation,
    currentConversationId,
    isLoading,
    error,
    createNewConversation,
    selectConversation,
    deleteConversation,
    sendMessage,
    addMessage,
    updateMessage,
    addActionToMessage,
    updateAction,
  };
}