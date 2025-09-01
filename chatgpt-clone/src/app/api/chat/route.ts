import { NextRequest, NextResponse } from 'next/server';
import { getChatCompletion } from '@/lib/openai';
import { executeAction } from '@/lib/actions';

export async function POST(request: NextRequest) {
  try {
    if (!process.env.OPENAI_API_KEY || process.env.OPENAI_API_KEY === 'dummy-key-for-build') {
      return NextResponse.json(
        { error: 'OpenAI API key not configured. Please set OPENAI_API_KEY in your environment variables.' },
        { status: 500 }
      );
    }

    const { messages } = await request.json();

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json(
        { error: 'Messages array is required' },
        { status: 400 }
      );
    }

    // Get initial completion
    const completion = await getChatCompletion(messages);
    const message = completion.choices[0]?.message;

    if (!message) {
      return NextResponse.json(
        { error: 'No response from OpenAI' },
        { status: 500 }
      );
    }

    // If the model wants to call a function
    if (message.function_call) {
      const functionName = message.function_call.name;
      const functionArgs = JSON.parse(message.function_call.arguments || '{}');

      // Execute the function
      const actionResult = await executeAction(functionName, functionArgs);

      // Add the function call and result to the conversation
      const updatedMessages = [
        ...messages,
        {
          role: 'assistant',
          content: null,
          function_call: message.function_call,
        },
        {
          role: 'function',
          name: functionName,
          content: actionResult.success 
            ? JSON.stringify(actionResult.result)
            : JSON.stringify({ error: actionResult.error }),
        },
      ];

      // Get the final response
      const finalCompletion = await getChatCompletion(updatedMessages);
      const finalMessage = finalCompletion.choices[0]?.message;

      return NextResponse.json({
        message: finalMessage,
        action: {
          name: functionName,
          parameters: functionArgs,
          result: actionResult.result,
          success: actionResult.success,
          error: actionResult.error,
        },
      });
    }

    // Regular response without function calls
    return NextResponse.json({
      message,
      action: null,
    });

  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}