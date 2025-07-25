import React, { useState } from 'react';
import { JoinChatFormProps } from '@/types';
import { validateUsername } from '@/utils';
import { User, Loader2 } from 'lucide-react';

export const JoinChatForm: React.FC<JoinChatFormProps> = ({ onJoin, isLoading = false }) => {
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const validation = validateUsername(name);
    if (!validation.isValid) {
      setError(validation.error || 'Nombre inválido');
      return;
    }
    
    setError('');
    onJoin(name.trim());
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setName(value);
    
    // Limpiar error cuando el usuario empiece a escribir
    if (error) {
      setError('');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
            <User className="w-8 h-8 text-blue-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Únete al Chat
          </h1>
          <p className="text-gray-600">
            Ingresa tu nombre para comenzar a chatear
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Tu nombre
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={handleNameChange}
              placeholder="Escribe tu nombre aquí..."
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors text-gray-900 bg-white placeholder-gray-500 ${
                error 
                  ? 'border-red-300 bg-red-50' 
                  : 'border-gray-300 hover:border-gray-400'
              }`}
              disabled={isLoading}
              maxLength={50}
              autoComplete="name"
              autoFocus
            />
            {error && (
              <p className="mt-2 text-sm text-red-600">{error}</p>
            )}
            <p className="mt-2 text-xs text-gray-500">
              {name.length}/50 caracteres
            </p>
          </div>

          <button
            type="submit"
            disabled={isLoading || !name.trim()}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Conectando...
              </>
            ) : (
              'Entrar al Chat'
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-xs text-gray-500">
            Al unirte, aceptas seguir las reglas de cortesía del chat
          </p>
        </div>
      </div>
    </div>
  );
};
