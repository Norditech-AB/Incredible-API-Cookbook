import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || 'dummy-key-for-build',
});

export const openaiClient = openai;

export const availableFunctions = {
  get_weather: {
    name: 'get_weather',
    description: 'Get the current weather for a specific location',
    parameters: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'The city and state/country, e.g. San Francisco, CA',
        },
        unit: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
          description: 'The temperature unit to use',
        },
      },
      required: ['location'],
    },
  },
  calculate: {
    name: 'calculate',
    description: 'Perform mathematical calculations',
    parameters: {
      type: 'object',
      properties: {
        expression: {
          type: 'string',
          description: 'The mathematical expression to evaluate, e.g. "2 + 2" or "sqrt(16)"',
        },
      },
      required: ['expression'],
    },
  },
  search_web: {
    name: 'search_web',
    description: 'Search the web for information',
    parameters: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'The search query',
        },
        limit: {
          type: 'number',
          description: 'Number of results to return (default: 5)',
        },
      },
      required: ['query'],
    },
  },
  get_current_time: {
    name: 'get_current_time',
    description: 'Get the current date and time',
    parameters: {
      type: 'object',
      properties: {
        timezone: {
          type: 'string',
          description: 'The timezone to get time for (e.g., "UTC", "America/New_York")',
        },
      },
    },
  },
  create_file: {
    name: 'create_file',
    description: 'Create a new file with content',
    parameters: {
      type: 'object',
      properties: {
        filename: {
          type: 'string',
          description: 'The name of the file to create',
        },
        content: {
          type: 'string',
          description: 'The content to write to the file',
        },
      },
      required: ['filename', 'content'],
    },
  },
  read_file: {
    name: 'read_file',
    description: 'Read the contents of a file',
    parameters: {
      type: 'object',
      properties: {
        filename: {
          type: 'string',
          description: 'The name of the file to read',
        },
      },
      required: ['filename'],
    },
  },
};

export async function getChatCompletion(
  messages: Array<{ role: string; content: string }>,
  functions?: OpenAI.Chat.Completions.ChatCompletionCreateParams.Function[]
) {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: messages as OpenAI.Chat.Completions.ChatCompletionMessageParam[],
      functions: functions || Object.values(availableFunctions),
      function_call: 'auto',
      temperature: 0.7,
    });

    return response;
  } catch (error) {
    console.error('OpenAI API error:', error);
    throw new Error('Failed to get chat completion');
  }
}