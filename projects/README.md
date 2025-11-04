# AI Chat Assistant - React Edition 🚀

A modern, feature-rich ChatGPT clone built with React, featuring beautiful animations, dark/light themes, and seamless API integration.

## ✨ Features

- 🎨 **Modern React Architecture**: Built with functional components and hooks
- 🌓 **Theme Switching**: Beautiful light and dark themes with smooth transitions
- 🎭 **Smooth Animations**: Powered by Framer Motion for delightful interactions
- 💬 **Real-time Chat**: Instant messaging with typing indicators
- 🔄 **Persistent Storage**: Chat history saved in localStorage
- 📱 **Responsive Design**: Works perfectly on all devices
- ⚙️ **Customizable Settings**: Toggle animations, sound effects, and themes
- 🎯 **API Ready**: Easy integration with OpenAI or custom AI APIs
- 🧹 **Chat Management**: Clear chat functionality with confirmation
- ⌨️ **Keyboard Shortcuts**: Enter to send, Shift+Enter for new lines

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd projects

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **Emotion** - CSS-in-JS styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons
- **CSS Variables** - Dynamic theming

## 🔧 Configuration

### API Setup

1. **Edit `src/config.js`**:
```javascript
export const CONFIG = {
  API: {
    ENDPOINT: 'https://api.openai.com/v1/chat/completions',
    API_KEY: 'your_openai_api_key_here',
    MODEL: 'gpt-3.5-turbo'
  }
  // ... other settings
};
```

2. **For Demo Mode** (no API required):
```javascript
// Uncomment this line in config.js
CONFIG.API.ENDPOINT = 'DEMO_MODE';
```

### Available Scripts

```bash
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
npm run eject      # Eject from Create React App
```

## 🏗️ Project Structure

```
src/
├── components/          # React components
│   ├── ChatApp.js      # Main chat application
│   ├── ChatMessage.js  # Individual message component
│   └── WelcomeMessage.js # Welcome screen component
├── context/            # React context
│   └── ThemeContext.js # Theme management
├── hooks/              # Custom React hooks
│   └── useChat.js      # Chat logic and API calls
├── config.js           # Configuration settings
├── App.js              # Main app component
├── App.css             # Global styles and CSS variables
└── index.js            # App entry point
```

## 🎨 Customization

### Themes
The app supports light and dark themes with CSS variables. Customize colors in `src/App.css`:

```css
:root {
  --primary-color: #667eea;
  --bg-primary: rgba(255, 255, 255, 0.95);
  /* ... more variables */
}
```

### Styling
- **Emotion**: Use styled components for component-specific styles
- **CSS Variables**: Modify global theme colors and properties
- **Responsive**: Mobile-first design with breakpoints

### Components
Each component is modular and can be easily customized:
- `ChatApp.js` - Main layout and functionality
- `ChatMessage.js` - Message display and animations
- `WelcomeMessage.js` - Welcome screen with features

## 🔌 API Integration

### OpenAI API
```javascript
// Example API request format
{
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
  ],
  "max_tokens": 1000,
  "temperature": 0.7,
  "model": "gpt-3.5-turbo"
}
```

### Custom API
Ensure your API accepts the same request format and returns:
```json
{
  "choices": [
    {
      "message": {
        "content": "AI response here"
      }
    }
  ]
}
```

## 📱 Responsive Design

- **Desktop**: Full-featured layout with sidebar options
- **Tablet**: Optimized for medium screens
- **Mobile**: Touch-friendly interface with mobile-first design

## 🎭 Animations

Powered by Framer Motion with configurable settings:
- Message entrance/exit animations
- Theme transition effects
- Interactive hover states
- Smooth page transitions

## 🔒 Security

- API keys stored in client-side config (use environment variables in production)
- Input sanitization and validation
- Secure API communication

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy Options
- **Netlify**: Drag and drop `build/` folder
- **Vercel**: Connect your GitHub repository
- **AWS S3**: Upload `build/` contents
- **GitHub Pages**: Use `gh-pages` package

### Environment Variables
For production, use environment variables:
```bash
REACT_APP_API_ENDPOINT=your_api_endpoint
REACT_APP_API_KEY=your_api_key
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 🐛 Troubleshooting

### Common Issues

1. **API Errors**: Check your API key and endpoint configuration
2. **Styling Issues**: Ensure all dependencies are installed
3. **Build Errors**: Clear `node_modules` and reinstall

### Debug Mode
Enable debug logging in the browser console for detailed error information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- React team for the amazing framework
- Framer Motion for smooth animations
- Lucide for beautiful icons
- OpenAI for the API inspiration

---

**Happy Chatting! 🤖💬**

For questions or support, please open an issue on GitHub.
