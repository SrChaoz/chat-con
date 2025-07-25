import React, { useState, useRef, useEffect } from 'react';
import { ChatInputProps } from '@/types';
import { validateMessage } from '@/utils';
import { Send, Smile } from 'lucide-react';

export const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  disabled = false,
  placeholder = "Escribe tu mensaje..." 
}) => {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize del textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const validation = validateMessage(message);
    if (!validation.isValid) {
      setError(validation.error || 'Mensaje inválido');
      return;
    }
    
    onSendMessage(message.trim());
    setMessage('');
    setError('');
    
    // Enfocar de nuevo el textarea
    textareaRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleMessageChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setMessage(value);
    
    // Limpiar error cuando el usuario empiece a escribir
    if (error) {
      setError('');
    }
  };

  const isMessageValid = message.trim().length > 0 && message.length <= 1000;

  return (
    <div className="border-t bg-white p-4">
      {error && (
        <div className="mb-3 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-600">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="flex items-end space-x-3">
        {/* Textarea para el mensaje */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleMessageChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className={`w-full px-4 py-3 pr-12 border rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors text-gray-900 bg-white placeholder-gray-500 ${
              error 
                ? 'border-red-300 bg-red-50' 
                : 'border-gray-300 hover:border-gray-400'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
            style={{ maxHeight: '120px' }}
            maxLength={1000}
          />
          
          {/* Contador de caracteres */}
          <div className="absolute bottom-2 right-2 text-xs text-gray-400">
            {message.length}/1000
          </div>
        </div>

        {/* Botón emoji (placeholder para futura implementación) */}
        <button
          type="button"
          className="p-3 text-gray-400 hover:text-gray-600 transition-colors"
          title="Emojis (próximamente)"
          disabled
        >
          <Smile className="w-5 h-5" />
        </button>

        {/* Botón enviar */}
        <button
          type="submit"
          disabled={disabled || !isMessageValid}
          className="bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          title="Enviar mensaje (Enter)"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>

      {/* Ayuda para atajos de teclado */}
      <div className="mt-2 text-xs text-gray-500 text-center">
        Presiona <kbd className="px-1 py-0.5 bg-gray-100 rounded text-xs">Enter</kbd> para enviar, 
        <kbd className="px-1 py-0.5 bg-gray-100 rounded text-xs ml-1">Shift + Enter</kbd> para nueva línea
      </div>
    </div>
  );
};
