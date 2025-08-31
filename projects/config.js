// Configuration file for AI Chat Assistant
const CONFIG = {
    // API Configuration
    API: {
        // Replace with your actual API endpoint
        ENDPOINT: 'YOUR_API_ENDPOINT_HERE',
        
        // Replace with your actual API key
        API_KEY: 'YOUR_API_KEY_HERE',
        
        // API request settings
        MAX_TOKENS: 1000,
        TEMPERATURE: 0.7,
        MODEL: 'gpt-3.5-turbo' // or your preferred model
    },
    
    // App Settings
    APP: {
        NAME: 'AI Chat Assistant',
        VERSION: '1.0.0',
        MAX_MESSAGE_LENGTH: 4000,
        TYPING_DELAY: 1000, // milliseconds
        AUTO_SAVE_INTERVAL: 5000 // milliseconds
    },
    
    // UI Settings
    UI: {
        THEME: 'light', // 'light' or 'dark'
        ANIMATIONS: true,
        SOUND_EFFECTS: false,
        COMPACT_MODE: false
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
}