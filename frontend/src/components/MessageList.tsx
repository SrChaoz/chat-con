import React, { useEffect, useRef } from 'react';
import { MessageListProps, Message } from '@/types';
import { formatTimestamp, getUserColor, linkifyText } from '@/utils';

interface MessageItemProps {
  message: Message;
  isOwn: boolean;
  showAvatar: boolean;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, isOwn, showAvatar }) => {
  const userColor = getUserColor(message.user_id);
  
  return (
    <div className={`flex ${isOwn ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-xs lg:max-w-md ${isOwn ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        {showAvatar && (
          <div 
            className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium ${
              isOwn ? 'ml-2' : 'mr-2'
            }`}
            style={{ backgroundColor: userColor }}
          >
            {message.user_name.charAt(0).toUpperCase()}
          </div>
        )}
        
        {/* Spacer cuando no se muestra avatar */}
        {!showAvatar && (
          <div className={`w-8 ${isOwn ? 'ml-2' : 'mr-2'}`} />
        )}
        
        {/* Mensaje */}
        <div className="flex flex-col">
          {/* Nombre del usuario */}
          {showAvatar && !isOwn && (
            <span 
              className="text-xs font-medium mb-1"
              style={{ color: userColor }}
            >
              {message.user_name}
            </span>
          )}
          
          {/* Bubble del mensaje */}
          <div
            className={`px-4 py-2 rounded-lg ${
              isOwn
                ? 'bg-blue-600 text-white rounded-br-sm'
                : 'bg-gray-200 text-gray-900 rounded-bl-sm'
            }`}
          >
            <div 
              className="text-sm break-words"
              dangerouslySetInnerHTML={{ __html: linkifyText(message.content) }}
            />
          </div>
          
          {/* Timestamp */}
          <span className={`text-xs text-gray-500 mt-1 ${isOwn ? 'text-right' : 'text-left'}`}>
            {formatTimestamp(message.timestamp)}
          </span>
        </div>
      </div>
    </div>
  );
};

export const MessageList: React.FC<MessageListProps> = ({ messages, currentUserId }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll al final cuando hay mensajes nuevos
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center text-gray-500">
          <div className="text-4xl mb-4">💬</div>
          <p className="text-lg font-medium mb-2">¡Bienvenido al chat!</p>
          <p className="text-sm">Sé el primero en enviar un mensaje</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-2">
      {messages.map((message, index) => {
        const isOwn = message.user_id === currentUserId;
        const prevMessage = index > 0 ? messages[index - 1] : null;
        
        // Mostrar avatar solo si es el primer mensaje del usuario o si pasó más de 5 minutos
        const showAvatar = !prevMessage || 
          prevMessage.user_id !== message.user_id ||
          (new Date(message.timestamp).getTime() - new Date(prevMessage.timestamp).getTime()) > 5 * 60 * 1000;

        return (
          <MessageItem
            key={message.id}
            message={message}
            isOwn={isOwn}
            showAvatar={showAvatar}
          />
        );
      })}
      <div ref={messagesEndRef} />
    </div>
  );
};
