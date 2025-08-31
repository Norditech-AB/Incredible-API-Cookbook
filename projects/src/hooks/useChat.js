import { useState, useEffect, useCallback } from 'react';
import { CONFIG } from '../config';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  // Load chat history from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem('chatHistory');
      if (saved) {
        const parsedMessages = JSON.parse(saved);
        // Recreate timestamp objects
        const messagesWithTimestamps = parsedMessages.map(msg => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        }));
        setMessages(messagesWithTimestamps);
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  }, []);

  // Save chat history to localStorage whenever messages change
  useEffect(() => {
    try {
      localStorage.setItem('chatHistory', JSON.stringify(messages));
    } catch (error) {
      console.error('Failed to save chat history:', error);
    }
  }, [messages]);

  const sendMessage = useCallback(async (content) => {
    if (!content.trim()) return;

    const userMessage = {
      id: Date.now(),
      content: content.trim(),
      type: 'user',
      timestamp: new Date()
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Get AI response
      const response = await getAIResponse(content, messages);
      
      const assistantMessage = {
        id: Date.now() + 1,
        content: response,
        type: 'assistant',
        timestamp: new Date()
      };

      // Add assistant message
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error getting AI response:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        content: 'Sorry, I encountered an error. Please try again.',
        type: 'assistant',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  }, [messages]);

  const clearChat = useCallback(() => {
    setMessages([]);
    localStorage.removeItem('chatHistory');
  }, []);

  const getAIResponse = async (message, messageHistory) => {
    // Check if we're in demo mode
    if (CONFIG.API.ENDPOINT === 'DEMO_MODE') {
      // Simulate API delay for demo
      await new Promise(resolve => setTimeout(resolve, 1000));
      return getMockResponse(message);
    }

    // Use configuration from config.js
    const apiUrl = CONFIG.API.ENDPOINT;
    const apiKey = CONFIG.API.API_KEY;

    if (!apiUrl || !apiKey || apiUrl === 'YOUR_API_ENDPOINT_HERE') {
      // Fallback to mock response if API not configured
      return getMockResponse(message);
    }

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          messages: [
            ...messageHistory.map(msg => ({
              role: msg.type === 'user' ? 'user' : 'assistant',
              content: msg.content
            })),
            { role: 'user', content: message }
          ],
          max_tokens: CONFIG.API.MAX_TOKENS,
          temperature: CONFIG.API.TEMPERATURE,
          model: CONFIG.API.MODEL
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const data = await response.json();
      return data.choices[0].message.content;

    } catch (error) {
      console.error('API Error:', error);
      // Fallback to mock response on API failure
      return getMockResponse(message);
    }
  };

  const getMockResponse = (message) => {
    const lowerMessage = message.toLowerCase();
    
    // Enhanced keyword-based responses
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
      return "Hello! 👋 I'm your AI assistant. How can I help you today?";
    } else if (lowerMessage.includes('help')) {
      return "I'm here to help! 🤝 What would you like to know or discuss? I can assist with questions, creative tasks, problem-solving, and more.";
    } else if (lowerMessage.includes('thank')) {
      return "You're welcome! 😊 Is there anything else I can help you with?";
    } else if (lowerMessage.includes('weather')) {
      return "I can't check the weather in real-time, but I'd be happy to help you with other questions! 🌤️";
    } else if (lowerMessage.includes('time')) {
      return `The current time is ${new Date().toLocaleTimeString()}. ⏰ How else can I assist you?`;
    } else if (lowerMessage.includes('joke')) {
      const jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        "I told my wife she was drawing her eyebrows too high. She looked surprised! 😲"
      ];
      return jokes[Math.floor(Math.random() * jokes.length)];
    } else if (lowerMessage.includes('code') || lowerMessage.includes('programming')) {
      return "I'd be happy to help with coding questions! 💻 What programming language or problem are you working with?";
    } else if (lowerMessage.includes('how are you')) {
      return "I'm functioning perfectly! 😊 How are you doing today?";
    } else if (lowerMessage.includes('name')) {
      return "I'm your AI Chat Assistant! 🤖 Nice to meet you!";
    } else if (lowerMessage.includes('bye') || lowerMessage.includes('goodbye')) {
      return "Goodbye! 👋 Feel free to come back anytime if you have more questions!";
    } else if (lowerMessage.includes('react')) {
      return "React is a fantastic JavaScript library for building user interfaces! ⚛️ It's great for creating interactive, component-based applications. What specific React question do you have?";
    } else if (lowerMessage.includes('ai') || lowerMessage.includes('artificial intelligence')) {
      return "Artificial Intelligence is fascinating! 🤖 It's transforming how we interact with technology. I'm an example of AI in action - how can I help you learn more about it?";
    }
    
    // Contextual responses based on message length
    if (message.length < 10) {
      return "That's a short message! Could you tell me more about what you'd like to know? 🤔";
    } else if (message.length > 100) {
      return "That's quite detailed! 📝 I appreciate you taking the time to explain. Let me think about how I can best help you with this.";
    }
    
    // General thoughtful responses
    const responses = [
      "That's an interesting question! 🤔 I'd be happy to help you explore that topic further.",
      "I understand what you're asking. Let me think about this... 💭",
      "Great question! Here's what I can tell you about that topic. 📚",
      "I appreciate you asking that. Let me provide some insights. 💡",
      "That's a thoughtful question. Here's my perspective on it. 🎯",
      "Interesting! I'd love to discuss that with you. What specific aspect would you like to explore? 🔍",
      "That's a great point! Let me share what I know about that. 📖",
      "I'm glad you asked that question. Here's what I can tell you. ✨"
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  return {
    messages,
    sendMessage,
    clearChat,
    isTyping
  };
};