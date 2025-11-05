export interface ActionResult {
  success: boolean;
  result?: unknown;
  error?: string;
}

// Weather action
export async function getWeather(location: string, unit: string = 'celsius'): Promise<ActionResult> {
  try {
    // Mock weather data - in a real app, you'd call a weather API
    const mockWeather = {
      location,
      temperature: unit === 'celsius' ? '22°C' : '72°F',
      condition: 'Partly cloudy',
      humidity: '65%',
      wind: '10 km/h',
    };
    
    return {
      success: true,
      result: `Current weather in ${location}: ${mockWeather.temperature}, ${mockWeather.condition}. Humidity: ${mockWeather.humidity}, Wind: ${mockWeather.wind}`,
    };
  } catch {
    return {
      success: false,
      error: 'Failed to get weather information',
    };
  }
}

// Calculator action
export async function calculate(expression: string): Promise<ActionResult> {
  try {
    // Simple math evaluation - in production, use a proper math parser
    const sanitizedExpression = expression.replace(/[^0-9+\-*/().\s]/g, '');
    const result = Function(`"use strict"; return (${sanitizedExpression})`)();
    
    return {
      success: true,
      result: `${expression} = ${result}`,
    };
  } catch {
    return {
      success: false,
      error: 'Invalid mathematical expression',
    };
  }
}

// Web search action
export async function searchWeb(query: string, limit: number = 5): Promise<ActionResult> {
  try {
    // Mock search results - in a real app, you'd call a search API
    const mockResults = [
      { title: `Search result 1 for "${query}"`, url: 'https://example.com/1', snippet: 'This is a mock search result...' },
      { title: `Search result 2 for "${query}"`, url: 'https://example.com/2', snippet: 'Another mock search result...' },
      { title: `Search result 3 for "${query}"`, url: 'https://example.com/3', snippet: 'Yet another mock search result...' },
    ].slice(0, limit);
    
    const formattedResults = mockResults.map((result, index) => 
      `${index + 1}. ${result.title}\n   ${result.snippet}\n   ${result.url}`
    ).join('\n\n');
    
    return {
      success: true,
      result: `Search results for "${query}":\n\n${formattedResults}`,
    };
  } catch {
    return {
      success: false,
      error: 'Failed to perform web search',
    };
  }
}

// Current time action
export async function getCurrentTime(timezone?: string): Promise<ActionResult> {
  try {
    const now = new Date();
    const timeString = timezone 
      ? now.toLocaleString('en-US', { timeZone: timezone })
      : now.toLocaleString();
    
    return {
      success: true,
      result: `Current time${timezone ? ` in ${timezone}` : ''}: ${timeString}`,
    };
  } catch {
    return {
      success: false,
      error: 'Failed to get current time',
    };
  }
}

// File operations
export async function createFile(filename: string, content: string): Promise<ActionResult> {
  try {
    // Mock file creation - in a real app, you'd write to the filesystem
    return {
      success: true,
      result: `File "${filename}" created successfully with ${content.length} characters.`,
    };
  } catch {
    return {
      success: false,
      error: 'Failed to create file',
    };
  }
}

export async function readFile(filename: string): Promise<ActionResult> {
  try {
    // Mock file reading - in a real app, you'd read from the filesystem
    const mockContent = `This is mock content for file "${filename}". In a real application, this would be the actual file content.`;
    
    return {
      success: true,
      result: `Contents of "${filename}":\n\n${mockContent}`,
    };
  } catch {
    return {
      success: false,
      error: 'Failed to read file',
    };
  }
}

// Action executor
export async function executeAction(functionName: string, parameters: Record<string, unknown>): Promise<ActionResult> {
  switch (functionName) {
    case 'get_weather':
      return await getWeather(parameters.location as string, parameters.unit as string);
    
    case 'calculate':
      return await calculate(parameters.expression as string);
    
    case 'search_web':
      return await searchWeb(parameters.query as string, parameters.limit as number);
    
    case 'get_current_time':
      return await getCurrentTime(parameters.timezone as string);
    
    case 'create_file':
      return await createFile(parameters.filename as string, parameters.content as string);
    
    case 'read_file':
      return await readFile(parameters.filename as string);
    
    default:
      return {
        success: false,
        error: `Unknown function: ${functionName}`,
      };
  }
}