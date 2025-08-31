import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';

const MessageContainer = styled(motion.div)`
  margin-bottom: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
`;

const MessageIcon = styled.div`
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 0.5rem;
  
  &.user {
    background: var(--primary-gradient);
    color: white;
  }
  
  &.assistant {
    background: var(--secondary-gradient);
    color: white;
  }
`;

const MessageContent = styled.div`
  flex: 1;
  max-width: 70%;
`;

const MessageBubble = styled.div`
  padding: 1rem 1.5rem;
  border-radius: 18px;
  line-height: 1.6;
  word-wrap: break-word;
  position: relative;
  
  &.user {
    background: var(--primary-gradient);
    color: white;
    border-bottom-right-radius: 6px;
    margin-left: auto;
    text-align: right;
  }
  
  &.assistant {
    background: var(--bg-message);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-bottom-left-radius: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
`;

const MessageTime = styled.div`
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  opacity: 0.8;
  text-align: ${props => props.align || 'left'};
`;

const MessageText = styled.div`
  white-space: pre-wrap;
  font-size: 0.95rem;
  
  &.user {
    text-align: right;
  }
`;

const ChatMessage = ({ message, animations }) => {
  const isUser = message.type === 'user';
  const timeString = new Date(message.timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  const messageVariants = {
    hidden: { 
      opacity: 0, 
      y: 20,
      scale: 0.95
    },
    visible: { 
      opacity: 1, 
      y: 0,
      scale: 1
    },
    exit: { 
      opacity: 0, 
      y: -20,
      scale: 0.95
    }
  };

  const iconVariants = {
    hidden: { scale: 0, rotate: -180 },
    visible: { 
      scale: 1, 
      rotate: 0,
      transition: { type: "spring", stiffness: 200, damping: 15 }
    }
  };

  return (
    <MessageContainer
      variants={animations ? messageVariants : {}}
      initial="hidden"
      animate="visible"
      exit="exit"
      transition={{ duration: 0.3, ease: "easeOut" }}
      layout
    >
      {!isUser && (
        <MessageIcon className="assistant">
          <motion.div
            variants={animations ? iconVariants : {}}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.1 }}
          >
            <Bot size={20} />
          </motion.div>
        </MessageIcon>
      )}
      
      <MessageContent>
        <MessageBubble className={isUser ? 'user' : 'assistant'}>
          <MessageText className={isUser ? 'user' : ''}>
            {message.content}
          </MessageText>
        </MessageBubble>
        <MessageTime align={isUser ? 'right' : 'left'}>
          {timeString}
        </MessageTime>
      </MessageContent>
      
      {isUser && (
        <MessageIcon className="user">
          <motion.div
            variants={animations ? iconVariants : {}}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.1 }}
          >
            <User size={20} />
          </motion.div>
        </MessageIcon>
      )}
    </MessageContainer>
  );
};

export default ChatMessage;