'use client';

import { Message } from '@/types/chat';
import { formatTime } from '@/lib/utils';
import { Bot, User, Loader2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';

interface MessageBubbleProps {
  message: Message;
  isTyping?: boolean;
}

export function MessageBubble({ message, isTyping = false }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-in fade-in-0 slide-in-from-bottom-2 duration-300`}>
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
            <Bot className="w-4 h-4 text-primary-foreground" />
          </div>
        </div>
      )}
      
      <div className={`flex flex-col max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`flex items-center gap-2 mb-1 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          <span className="text-sm font-medium text-muted-foreground">
            {isUser ? 'You' : 'Assistant'}
          </span>
          <span className="text-xs text-muted-foreground">
            {formatTime(message.timestamp)}
          </span>
        </div>
        
        <Card className={`p-3 ${isUser ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
          {isTyping ? (
            <div className="flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Thinking...</span>
            </div>
          ) : (
            <div className="whitespace-pre-wrap">{message.content}</div>
          )}
        </Card>
        
        {message.actions && message.actions.length > 0 && (
          <div className="mt-2 space-y-2">
            {message.actions.map((action) => (
              <div key={action.id} className="text-sm">
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant="outline" className="text-xs">
                    {action.name}
                  </Badge>
                  <span className="text-muted-foreground">
                    {action.status === 'pending' && 'Executing...'}
                    {action.status === 'completed' && 'Completed'}
                    {action.status === 'failed' && 'Failed'}
                  </span>
                </div>
                {action.result && (
                  <Card className="p-2 bg-muted/50">
                    <pre className="text-xs overflow-x-auto">
                      {typeof action.result === 'string' 
                        ? action.result 
                        : JSON.stringify(action.result, null, 2)
                      }
                    </pre>
                  </Card>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
      
      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
            <User className="w-4 h-4 text-secondary-foreground" />
          </div>
        </div>
      )}
    </div>
  );
}