'use client';

import { useState } from 'react';
import { useChat } from '@/hooks';
import { 
  JoinChatForm, 
  MessageList, 
  ChatInput, 
  UserList, 
  ConnectionStatus,
  LoadingSpinner 
} from '@/components';
import { Settings, Menu, X } from 'lucide-react';
import { Toaster } from 'react-hot-toast';

export default function Home() {
  const { 
    isConnected, 
    currentUser, 
    users, 
    messages, 
    joinChat, 
    sendMessage,
    refreshUsers 
  } = useChat();
  
  const [showUserList, setShowUserList] = useState(false);
  const [isJoining, setIsJoining] = useState(false);

  const handleJoinChat = async (name: string) => {
    setIsJoining(true);
    try {
      joinChat(name);
      // El estado se actualizará automáticamente cuando recibamos la respuesta del servidor
    } catch (error) {
      console.error('Error joining chat:', error);
    } finally {
      setIsJoining(false);
    }
  };

  const handleSendMessage = (content: string) => {
    sendMessage(content);
  };

  const toggleUserList = () => {
    setShowUserList(!showUserList);
  };

  // Si no hay usuario actual, mostrar formulario de unión
  if (!currentUser) {
    return (
      <>
        <JoinChatForm onJoin={handleJoinChat} isLoading={isJoining} />
        <Toaster 
          position="top-center"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
      
      {/* Header */}
      <header className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold text-gray-900">Chat Grupal</h1>
          <ConnectionStatus isConnected={isConnected} />
        </div>
        
        <div className="flex items-center space-x-2">
          {/* Contador de usuarios en móvil */}
          <div className="sm:hidden bg-gray-100 px-3 py-1 rounded-full text-sm text-gray-600">
            {users.length} {users.length === 1 ? 'usuario' : 'usuarios'}
          </div>
          
          {/* Botón para mostrar/ocultar lista de usuarios en móvil */}
          <button
            onClick={toggleUserList}
            className="sm:hidden p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            aria-label={showUserList ? 'Ocultar usuarios' : 'Mostrar usuarios'}
          >
            {showUserList ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          
          {/* Botón de configuración (placeholder) */}
          <button
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            title="Configuración"
          >
            <Settings className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Contenido principal */}
      <div className="flex-1 flex overflow-hidden">
        {/* Área del chat */}
        <div className="flex-1 flex flex-col">
          {/* Lista de mensajes */}
          <MessageList 
            messages={messages} 
            currentUserId={currentUser?.id}
          />
          
          {/* Input para enviar mensajes */}
          <ChatInput 
            onSendMessage={handleSendMessage}
            disabled={!isConnected}
            placeholder={
              isConnected 
                ? "Escribe tu mensaje..." 
                : "Conectando..."
            }
          />
        </div>

        {/* Lista de usuarios - Desktop */}
        <div className="hidden sm:block w-80">
          <UserList 
            users={users} 
            currentUserId={currentUser?.id}
          />
        </div>
      </div>

      {/* Lista de usuarios - Mobile Overlay */}
      {showUserList && (
        <div className="sm:hidden fixed inset-0 bg-black bg-opacity-50 z-50">
          <div className="absolute right-0 top-0 h-full w-80 max-w-full">
            <UserList 
              users={users} 
              currentUserId={currentUser?.id}
            />
          </div>
          {/* Overlay para cerrar */}
          <div 
            className="absolute inset-0 -z-10"
            onClick={() => setShowUserList(false)}
          />
        </div>
      )}

      {/* Loading overlay cuando no está conectado */}
      {!isConnected && currentUser && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-40">
          <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
            <LoadingSpinner />
            <span className="text-gray-700">Reconectando...</span>
          </div>
        </div>
      )}
    </div>
  );
}
