import React, { useState, useRef, useEffect } from 'react';
import styled from '@emotion/styled';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Trash2, Send, Settings, Sun, Moon, Zap, Volume2, VolumeX } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import ChatMessage from './ChatMessage';
import WelcomeMessage from './WelcomeMessage';
import { useChat } from '../hooks/useChat';

const ChatAppContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  overflow: hidden;
`;

const Header = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const LogoIcon = styled(motion.div)`
  color: var(--primary-color);
  display: flex;
  align-items: center;
`;

const LogoText = styled.h1`
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
`;

const HeaderActions = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const ActionButton = styled.button`
  background: var(--button-bg);
  color: var(--button-text);
  border: none;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;

  &:hover {
    background: var(--button-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  &.danger {
    background: var(--danger-color);
    
    &:hover {
      background: var(--danger-hover);
    }
  }
`;

const ChatContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background: var(--bg-chat);
  position: relative;
`;

const InputContainer = styled.div`
  padding: 1.5rem 2rem;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  background: var(--bg-input);
  border-radius: 25px;
  padding: 0.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
`;

const TextArea = styled.textarea`
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-family: inherit;
  background: transparent;
  color: var(--text-primary);
  max-height: 120px;
  min-height: 44px;
  line-height: 1.5;

  &::placeholder {
    color: var(--text-secondary);
  }
`;

const SendButton = styled(motion.button)`
  background: var(--primary-gradient);
  color: white;
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;

  &:hover:not(:disabled) {
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const InputFooter = styled.div`
  margin-top: 0.5rem;
  min-height: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  gap: 0.25rem;
  align-items: center;
  color: var(--primary-color);
`;

const Dot = styled(motion.div)`
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
`;

const SettingsPanel = styled(motion.div)`
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 200px;
`;

const SettingsItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color);

  &:last-child {
    border-bottom: none;
  }
`;

const SettingsLabel = styled.span`
  color: var(--text-primary);
  font-size: 0.9rem;
`;

const Toggle = styled.button`
  background: ${props => props.active ? 'var(--primary-color)' : 'var(--text-secondary)'};
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;

  &:hover {
    opacity: 0.8;
  }
`;

const ChatApp = () => {
  const { theme, animations, soundEffects, toggleTheme, toggleAnimations, toggleSoundEffects } = useTheme();
  const { messages, sendMessage, clearChat, isTyping } = useChat();
  const [inputValue, setInputValue] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const textareaRef = useRef(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  }, [inputValue]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = () => {
    if (!inputValue.trim() || isTyping) return;
    
    sendMessage(inputValue.trim());
    setInputValue('');
    
    if (textareaRef.current) {
      textareaRef.current.style.height = '44px';
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      clearChat();
    }
  };

  return (
    <ChatAppContainer>
      <Header>
        <Logo>
          <LogoIcon
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          >
            <Bot size={32} />
          </LogoIcon>
          <LogoText>AI Chat Assistant</LogoText>
        </Logo>
        
        <HeaderActions>
          <ActionButton onClick={() => setShowSettings(!showSettings)}>
            <Settings size={20} />
          </ActionButton>
          <ActionButton className="danger" onClick={handleClearChat}>
            <Trash2 size={20} />
          </ActionButton>
          
          <AnimatePresence>
            {showSettings && (
              <SettingsPanel
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                <SettingsItem>
                  <SettingsLabel>Theme</SettingsLabel>
                  <ActionButton onClick={toggleTheme}>
                    {theme === 'light' ? <Moon size={16} /> : <Sun size={16} />}
                  </ActionButton>
                </SettingsItem>
                <SettingsItem>
                  <SettingsLabel>Animations</SettingsLabel>
                  <Toggle active={animations} onClick={toggleAnimations}>
                    {animations ? 'ON' : 'OFF'}
                  </Toggle>
                </SettingsItem>
                <SettingsItem>
                  <SettingsLabel>Sound Effects</SettingsLabel>
                  <Toggle active={soundEffects} onClick={toggleSoundEffects}>
                    {soundEffects ? 'ON' : 'OFF'}
                  </Toggle>
                </SettingsItem>
              </SettingsPanel>
            )}
          </AnimatePresence>
        </HeaderActions>
      </Header>

      <ChatContainer ref={chatContainerRef}>
        <AnimatePresence>
          {messages.length === 0 ? (
            <WelcomeMessage key="welcome" />
          ) : (
            messages.map((message, index) => (
              <ChatMessage 
                key={index} 
                message={message} 
                animations={animations}
              />
            ))
          )}
        </AnimatePresence>
        
        {isTyping && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            style={{ marginTop: '1rem' }}
          >
            <TypingIndicator>
              <span>AI is typing</span>
              <Dot animate={{ y: [0, -10, 0] }} transition={{ duration: 1, repeat: Infinity, delay: 0 }} />
              <Dot animate={{ y: [0, -10, 0] }} transition={{ duration: 1, repeat: Infinity, delay: 0.2 }} />
              <Dot animate={{ y: [0, -10, 0] }} transition={{ duration: 1, repeat: Infinity, delay: 0.4 }} />
            </TypingIndicator>
          </motion.div>
        )}
      </ChatContainer>

      <InputContainer>
        <InputWrapper>
          <TextArea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Type your message here..."
            rows={1}
          />
          <SendButton
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isTyping}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Send size={20} />
          </SendButton>
        </InputWrapper>
        
        <InputFooter>
          <div></div>
          <small style={{ color: 'var(--text-secondary)' }}>
            Press Enter to send, Shift+Enter for new line
          </small>
        </InputFooter>
      </InputContainer>
    </ChatAppContainer>
  );
};

export default ChatApp;