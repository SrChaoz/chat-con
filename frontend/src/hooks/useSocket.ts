import { useEffect, useRef, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { config, SOCKET_EVENTS } from '@/config';
import { UseSocketReturn } from '@/types';
import toast from 'react-hot-toast';

export const useSocket = (): UseSocketReturn => {
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    // Crear conexión de socket
    const socket = io(config.socketUrl, {
      transports: ['websocket', 'polling'],
      timeout: 20000,
    });

    socketRef.current = socket;

    // Eventos de conexión
    socket.on('connect', () => {
      console.log('Connected to server');
      setIsConnected(true);
      toast.success('Conectado al servidor');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from server');
      setIsConnected(false);
      toast.error('Desconectado del servidor');
    });

    socket.on('connect_error', (error) => {
      console.error('Connection error:', error);
      toast.error('Error de conexión');
    });

    // Limpiar al desmontar
    return () => {
      socket.disconnect();
    };
  }, []);

  const joinChat = useCallback((name: string) => {
    if (socketRef.current && isConnected) {
      socketRef.current.emit(SOCKET_EVENTS.JOIN_CHAT, { name });
    }
  }, [isConnected]);

  const sendMessage = useCallback((content: string, roomId: string = 'general') => {
    if (socketRef.current && isConnected) {
      socketRef.current.emit(SOCKET_EVENTS.SEND_MESSAGE, { content, room_id: roomId });
    }
  }, [isConnected]);

  const getUsers = useCallback(() => {
    if (socketRef.current && isConnected) {
      socketRef.current.emit(SOCKET_EVENTS.GET_USERS);
    }
  }, [isConnected]);

  return {
    socket: socketRef.current,
    isConnected,
    joinChat,
    sendMessage,
    getUsers,
  };
};
