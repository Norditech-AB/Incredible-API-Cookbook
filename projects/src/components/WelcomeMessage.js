import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { MessageCircle, Sparkles, Zap, Heart } from 'lucide-react';

const WelcomeContainer = styled(motion.div)`
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
`;

const WelcomeIcon = styled(motion.div)`
  font-size: 4rem;
  color: var(--primary-color);
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
`;

const WelcomeTitle = styled.h2`
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
  font-weight: 700;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const WelcomeSubtitle = styled.p`
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  color: var(--text-secondary);
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
`;

const FeatureCard = styled(motion.div)`
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border-color: var(--primary-color);
  }
`;

const FeatureIcon = styled.div`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--primary-gradient);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
`;

const FeatureTitle = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
`;

const FeatureDescription = styled.p`
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
`;

const WelcomeMessage = () => {
  const containerVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  const iconVariants = {
    hidden: { scale: 0, rotate: -180 },
    visible: { 
      scale: 1, 
      rotate: 0,
      transition: { 
        type: "spring", 
        stiffness: 200, 
        damping: 15,
        delay: 0.5
      }
    }
  };

  const features = [
    {
      icon: <MessageCircle size={24} />,
      title: "Smart Conversations",
      description: "Engage in natural, intelligent conversations with AI assistance"
    },
    {
      icon: <Sparkles size={24} />,
      title: "Creative Help",
      description: "Get help with writing, brainstorming, and creative projects"
    },
    {
      icon: <Zap size={24} />,
      title: "Quick Responses",
      description: "Fast, accurate answers to your questions and problems"
    },
    {
      icon: <Heart size={24} />,
      title: "Personalized Experience",
      description: "Adapts to your conversation style and preferences"
    }
  ];

  return (
    <WelcomeContainer
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <WelcomeIcon>
        <motion.div
          variants={iconVariants}
          initial="hidden"
          animate="visible"
        >
          <MessageCircle size={64} />
        </motion.div>
      </WelcomeIcon>
      
      <motion.div variants={itemVariants}>
        <WelcomeTitle>Welcome to AI Chat Assistant</WelcomeTitle>
      </motion.div>
      
      <motion.div variants={itemVariants}>
        <WelcomeSubtitle>
          Your intelligent companion for conversations, problem-solving, and creative exploration. 
          Start chatting to experience the power of AI assistance!
        </WelcomeSubtitle>
      </motion.div>

      <FeatureGrid>
        {features.map((feature, index) => (
          <FeatureCard
            key={index}
            variants={itemVariants}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FeatureIcon>
              {feature.icon}
            </FeatureIcon>
            <FeatureTitle>{feature.title}</FeatureTitle>
            <FeatureDescription>{feature.description}</FeatureDescription>
          </FeatureCard>
        ))}
      </FeatureGrid>
    </WelcomeContainer>
  );
};

export default WelcomeMessage;