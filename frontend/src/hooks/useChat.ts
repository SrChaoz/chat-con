import { useState, useEffect, useCallback } from 'react';
import { useSocket } from './useSocket';
import { User, Message, UseChatReturn } from '@/types';
import { SOCKET_EVENTS } from '@/config';
import toast from 'react-hot-toast';

export const useChat = (): UseChatReturn => {
  const { socket, isConnected, joinChat: socketJoinChat, sendMessage: socketSendMessage, getUsers } = useSocket();
  
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentRoom] = useState<string>('general');

  // Configurar listeners de socket
  useEffect(() => {
    if (!socket) return;

    // Evento: Usuario se unió al chat exitosamente
    const handleJoinedChat = (data: { user: User; message: string }) => {
      console.log('Joined chat:', data);
      setCurrentUser(data.user);
      toast.success(data.message);
    };

    // Evento: Nuevo mensaje recibido
    const handleNewMessage = (message: Message) => {
      console.log('New message:', message);
      setMessages(prev => [...prev, message]);
      
      // Mostrar notificación si no es del usuario actual
      if (currentUser && message.user_id !== currentUser.id) {
        toast(`${message.user_name}: ${message.content.substring(0, 50)}${message.content.length > 50 ? '...' : ''}`, {
          icon: '💬',
        });
      }
    };

    // Evento: Usuario se unió
    const handleUserJoined = (data: { user: User; users_count: number }) => {
      console.log('User joined:', data);
      if (currentUser && data.user.id !== currentUser.id) {
        toast.success(`${data.user.name} se unió al chat`);
      }
    };

    // Evento: Usuario salió
    const handleUserLeft = (data: { user: User; users_count: number }) => {
      console.log('User left:', data);
      toast(`${data.user.name} salió del chat`, { icon: '👋' });
    };

    // Evento: Lista de usuarios actualizada
    const handleUsersUpdated = (data: { users: User[]; count: number }) => {
      console.log('Users updated:', data);
      setUsers(data.users);
    };

    // Evento: Lista de usuarios
    const handleUsersList = (data: { users: User[] }) => {
      console.log('Users list:', data);
      setUsers(data.users);
    };

    // Evento: Mensajes recientes
    const handleRecentMessages = (data: { messages: Message[] }) => {
      console.log('Recent messages:', data);
      setMessages(data.messages);
    };

    // Evento: Error
    const handleError = (data: { message: string }) => {
      console.error('Socket error:', data);
      toast.error(data.message);
    };

    // Registrar listeners
    socket.on(SOCKET_EVENTS.JOINED_CHAT, handleJoinedChat);
    socket.on(SOCKET_EVENTS.NEW_MESSAGE, handleNewMessage);
    socket.on(SOCKET_EVENTS.USER_JOINED, handleUserJoined);
    socket.on(SOCKET_EVENTS.USER_LEFT, handleUserLeft);
    socket.on(SOCKET_EVENTS.USERS_UPDATED, handleUsersUpdated);
    socket.on(SOCKET_EVENTS.USERS_LIST, handleUsersList);
    socket.on(SOCKET_EVENTS.RECENT_MESSAGES, handleRecentMessages);
    socket.on(SOCKET_EVENTS.ERROR, handleError);

    // Limpiar listeners
    return () => {
      socket.off(SOCKET_EVENTS.JOINED_CHAT, handleJoinedChat);
      socket.off(SOCKET_EVENTS.NEW_MESSAGE, handleNewMessage);
      socket.off(SOCKET_EVENTS.USER_JOINED, handleUserJoined);
      socket.off(SOCKET_EVENTS.USER_LEFT, handleUserLeft);
      socket.off(SOCKET_EVENTS.USERS_UPDATED, handleUsersUpdated);
      socket.off(SOCKET_EVENTS.USERS_LIST, handleUsersList);
      socket.off(SOCKET_EVENTS.RECENT_MESSAGES, handleRecentMessages);
      socket.off(SOCKET_EVENTS.ERROR, handleError);
    };
  }, [socket, currentUser]);

  const joinChat = useCallback((name: string) => {
    if (!name.trim()) {
      toast.error('El nombre es requerido');
      return;
    }
    
    socketJoinChat(name.trim());
  }, [socketJoinChat]);

  const sendMessage = useCallback((content: string) => {
    if (!content.trim()) {
      toast.error('El mensaje no puede estar vacío');
      return;
    }
    
    if (!currentUser) {
      toast.error('Debes unirte al chat primero');
      return;
    }
    
    socketSendMessage(content.trim(), currentRoom);
  }, [socketSendMessage, currentUser, currentRoom]);

  const refreshUsers = useCallback(() => {
    getUsers();
  }, [getUsers]);

  return {
    isConnected,
    currentUser,
    users,
    messages,
    currentRoom,
    joinChat,
    sendMessage,
    refreshUsers,
  };
};
