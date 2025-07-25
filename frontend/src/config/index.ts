import { AppConfig } from '@/types';

export const config: AppConfig = {
  socketUrl: process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:8000',
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  maxMessageLength: 1000,
  maxNameLength: 50,
  reconnectAttempts: 5,
  reconnectDelay: 1000,
};

export const SOCKET_EVENTS = {
  // Cliente a servidor
  JOIN_CHAT: 'join_chat',
  SEND_MESSAGE: 'send_message',
  GET_USERS: 'get_users',
  
  // Servidor a cliente
  CONNECTED: 'connected',
  JOINED_CHAT: 'joined_chat',
  NEW_MESSAGE: 'new_message',
  USER_JOINED: 'user_joined',
  USER_LEFT: 'user_left',
  USERS_UPDATED: 'users_updated',
  USERS_LIST: 'users_list',
  RECENT_MESSAGES: 'recent_messages',
  ERROR: 'error',
} as const;
