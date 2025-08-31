# AI Chat Assistant - ChatGPT Clone

A beautiful, modern ChatGPT clone built with vanilla HTML, CSS, and JavaScript. Features a responsive design, smooth animations, and easy API integration.

## Features

- 🎨 **Modern UI/UX**: Clean, responsive design with smooth animations
- 💬 **Real-time Chat**: Instant messaging with typing indicators
- 🔄 **Chat History**: Persistent chat history using localStorage
- ⌨️ **Keyboard Shortcuts**: Ctrl/Cmd+K to focus, Enter to send, Escape to clear
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- 🎯 **Easy API Integration**: Simple configuration for your AI API
- 🧹 **Chat Management**: Clear chat history functionality

## Quick Start

1. **Clone or download** the project files
2. **Configure your API** (see API Setup below)
3. **Open `index.html`** in your web browser
4. **Start chatting!**

## API Setup

### Option 1: OpenAI API (Recommended)

1. Get your API key from [OpenAI](https://platform.openai.com/api-keys)
2. Edit `config.js` and update:
   ```javascript
   API: {
       ENDPOINT: 'https://api.openai.com/v1/chat/completions',
       API_KEY: 'your_openai_api_key_here',
       MODEL: 'gpt-3.5-turbo'
   }
   ```

### Option 2: Custom AI API

1. Update `config.js` with your API details:
   ```javascript
   API: {
       ENDPOINT: 'https://your-api-endpoint.com/chat',
       API_KEY: 'your_api_key_here',
       MODEL: 'your_model_name'
   }
   ```

2. Ensure your API accepts requests in this format:
   ```json
   {
       "messages": [
           {"role": "user", "content": "Hello"},
           {"role": "assistant", "content": "Hi there!"}
       ],
       "max_tokens": 1000,
       "temperature": 0.7
   }
   ```

3. And returns responses in this format:
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

### Option 3: Mock Mode (Development)

The app includes mock responses for development and testing. No API setup required!

## File Structure

```
projects/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and animations
├── script.js           # JavaScript functionality
├── config.js           # Configuration and API settings
└── README.md           # This file
```

## Customization

### Styling
- Edit `styles.css` to change colors, fonts, and layout
- Modify CSS variables for easy theme changes
- Add custom animations and transitions

### Functionality
- Edit `script.js` to add new features
- Modify the `ChatApp` class for advanced functionality
- Add new keyboard shortcuts or UI interactions

### Configuration
- Update `config.js` for app-wide settings
- Modify API parameters and app behavior
- Add new configuration options

## Browser Support

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

## Security Notes

- **Never commit API keys** to version control
- Use environment variables for production deployments
- Consider implementing rate limiting for API calls
- Validate user input before sending to API

## Deployment

### Local Development
Simply open `index.html` in your browser. No build process required!

### Web Server
Upload files to any web server (Apache, Nginx, etc.)

### Static Hosting
Deploy to services like:
- GitHub Pages
- Netlify
- Vercel
- AWS S3

## Troubleshooting

### API Issues
- Check your API key and endpoint
- Verify API request format matches your service
- Check browser console for error messages
- Ensure CORS is enabled if testing locally

### UI Issues
- Clear browser cache and localStorage
- Check for JavaScript errors in console
- Verify all files are in the same directory

### Performance
- Disable animations in `config.js` if needed
- Reduce `MAX_TOKENS` for faster responses
- Implement message pagination for long chats

## Contributing

Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review browser console for errors
3. Verify API configuration
4. Test with mock mode first

---

**Happy Chatting! 🤖💬**