# ChatGPT Clone with Actions

A full-featured ChatGPT clone built with Next.js that includes action capabilities, allowing the AI to perform various tasks and integrations.

## Features

- 🤖 **AI Chat Interface**: Clean, modern chat interface similar to ChatGPT
- ⚡ **Action System**: AI can execute functions and take actions
- 🌤️ **Weather Integration**: Get current weather information
- 🧮 **Calculator**: Perform mathematical calculations
- 🔍 **Web Search**: Search the web for information
- ⏰ **Time Functions**: Get current time in different timezones
- 📁 **File Operations**: Create and read files (mock implementation)
- 💾 **Conversation Memory**: Persistent conversation history
- 🌙 **Dark Mode**: Toggle between light and dark themes
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Available Actions

The AI can perform the following actions:

1. **Weather**: `get_weather(location, unit)` - Get weather information
2. **Calculator**: `calculate(expression)` - Perform math calculations
3. **Web Search**: `search_web(query, limit)` - Search the internet
4. **Current Time**: `get_current_time(timezone)` - Get current date/time
5. **File Operations**: `create_file(filename, content)` and `read_file(filename)`

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chatgpt-clone
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
```

4. Add your OpenAI API key to `.env.local`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the development server:
```bash
npm run dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. **Start a New Chat**: Click "New Chat" to begin a conversation
2. **Ask Questions**: Type your questions or requests in the chat input
3. **AI Actions**: The AI will automatically use available functions when appropriate
4. **View Actions**: See executed actions and their results below AI responses
5. **Manage Conversations**: Use the sidebar to switch between conversations
6. **Toggle Theme**: Use the theme toggle in the header

## Example Interactions

- "What's the weather like in New York?"
- "Calculate 15 * 23 + 45"
- "Search for information about Next.js"
- "What time is it in Tokyo?"
- "Create a file called 'notes.txt' with some content"

## Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── api/chat/          # Chat API endpoint
│   ├── globals.css        # Global styles
│   └── page.tsx           # Main page
├── components/            # React components
│   ├── chat/              # Chat-related components
│   └── ui/                # Reusable UI components
├── hooks/                 # Custom React hooks
├── lib/                   # Utility libraries
│   ├── actions.ts         # Action implementations
│   ├── openai.ts          # OpenAI integration
│   └── utils.ts           # Utility functions
└── types/                 # TypeScript type definitions
```

## Technologies Used

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **OpenAI API**: GPT-4 integration with function calling
- **Radix UI**: Accessible UI components
- **Lucide React**: Beautiful icons

## Customization

### Adding New Actions

1. Define the function in `src/lib/actions.ts`
2. Add the function schema to `src/lib/openai.ts`
3. Update the `executeAction` function to handle your new action

### Styling

The app uses Tailwind CSS with a custom design system. You can customize:
- Colors in `src/app/globals.css`
- Component styles in individual component files
- Layout in `src/components/chat/ChatContainer.tsx`

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Add your `OPENAI_API_KEY` environment variable
4. Deploy!

### Other Platforms

The app can be deployed to any platform that supports Next.js:
- Netlify
- Railway
- DigitalOcean App Platform
- AWS Amplify

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

If you encounter any issues or have questions, please open an issue on GitHub.