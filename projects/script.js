// Chat functionality for AI Chat Assistant
class ChatApp {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.userInput = document.getElementById('userInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.messages = [];
        this.isTyping = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadChatHistory();
        this.autoResizeTextarea();
    }

    setupEventListeners() {
        this.userInput.addEventListener('input', () => this.autoResizeTextarea());
        this.userInput.addEventListener('focus', () => this.autoResizeTextarea());
    }

    autoResizeTextarea() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isTyping) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.autoResizeTextarea();
        this.scrollToBottom();

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Get AI response
            const response = await this.getAIResponse(message);
            this.hideTypingIndicator();
            this.addMessage(response, 'assistant');
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            console.error('Error:', error);
        }

        this.scrollToBottom();
    }

    async getAIResponse(message) {
        // Check if we're in demo mode
        if (window.CONFIG?.API?.ENDPOINT === 'DEMO_MODE') {
            // Simulate API delay for demo
            await new Promise(resolve => setTimeout(resolve, 1000));
            return this.getMockResponse(message);
        }
        
        // Use configuration from config.js
        const apiUrl = window.CONFIG?.API?.ENDPOINT || 'YOUR_API_ENDPOINT_HERE';
        const apiKey = window.CONFIG?.API?.API_KEY || 'YOUR_API_KEY_HERE';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    messages: [
                        ...this.messages.map(msg => ({
                            role: msg.type === 'user' ? 'user' : 'assistant',
                            content: msg.content
                        })),
                        { role: 'user', content: message }
                    ],
                    max_tokens: window.CONFIG?.API?.MAX_TOKENS || 1000,
                    temperature: window.CONFIG?.API?.TEMPERATURE || 0.7,
                    model: window.CONFIG?.API?.MODEL || 'gpt-3.5-turbo'
                })
            });

            if (!response.ok) {
                throw new Error(`API request failed: ${response.status}`);
            }

            const data = await response.json();
            return data.choices[0].message.content;

        } catch (error) {
            // For demo purposes, return a mock response
            // Remove this when you have your actual API
            return this.getMockResponse(message);
        }
    }

    getMockResponse(message) {
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
    }

    addMessage(content, type) {
        const message = {
            content,
            type,
            timestamp: new Date()
        };

        this.messages.push(message);
        this.saveChatHistory();
        this.displayMessage(message);
    }

    displayMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${message.type}`;
        
        const timeString = message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        messageElement.innerHTML = `
            <div class="message-content">${this.escapeHtml(message.content)}</div>
            <div class="message-time">${timeString}</div>
        `;

        // Remove welcome message if it exists
        const welcomeMessage = this.chatContainer.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        this.chatContainer.appendChild(messageElement);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showTypingIndicator() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'flex';
        this.sendBtn.disabled = true;
    }

    hideTypingIndicator() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
        this.sendBtn.disabled = false;
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        }, 100);
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.messages = [];
            this.chatContainer.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-icon">
                        <i class="fas fa-comments"></i>
                    </div>
                    <h2>Welcome to AI Chat Assistant</h2>
                    <p>Ask me anything! I'm here to help you with questions, creative tasks, and more.</p>
                </div>
            `;
            this.saveChatHistory();
        }
    }

    saveChatHistory() {
        try {
            localStorage.setItem('chatHistory', JSON.stringify(this.messages));
        } catch (error) {
            console.error('Failed to save chat history:', error);
        }
    }

    loadChatHistory() {
        try {
            const saved = localStorage.getItem('chatHistory');
            if (saved) {
                this.messages = JSON.parse(saved);
                this.messages.forEach(message => {
                    // Recreate timestamp objects
                    message.timestamp = new Date(message.timestamp);
                    this.displayMessage(message);
                });
                this.scrollToBottom();
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }
}

// Global functions for HTML onclick handlers
let chatApp;

function sendMessage() {
    if (!chatApp) return;
    chatApp.sendMessage();
}

function clearChat() {
    if (!chatApp) return;
    chatApp.clearChat();
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    chatApp = new ChatApp();
});

// Add some helpful features
document.addEventListener('DOMContentLoaded', () => {
    // Focus on input when page loads
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.focus();
    }

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            userInput.focus();
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            userInput.value = '';
            userInput.style.height = 'auto';
        }
    });
});