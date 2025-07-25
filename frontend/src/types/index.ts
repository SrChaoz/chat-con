// Tipos para usuarios
export interface User {
  id: string;
  name: string;
  is_active: boolean;
  joined_at: string;
}

// Tipos para mensajes
export enum MessageType {
  TEXT = "text",
  SYSTEM = "system",
  NOTIFICATION = "notification"
}

export interface Message {
  id: string;
  user_id: string;
  user_name: string;
  content: string;
  message_type: MessageType;
  timestamp: string;
  room_id: string;
}

// Tipos para salas de chat
export interface ChatRoom {
  id: string;
  name: string;
  users: User[];
  messages: Message[];
  created_at: string;
  is_active: boolean;
}

// Tipos para eventos de Socket.IO
export interface SocketEvents {
  // Eventos del cliente al servidor
  join_chat: (data: { name: string }) => void;
  send_message: (data: { content: string; room_id?: string }) => void;
  get_users: () => void;
  
  // Eventos del servidor al cliente
  connected: (data: { message: string }) => void;
  joined_chat: (data: { user: User; message: string }) => void;
  new_message: (message: Message) => void;
  user_joined: (data: { user: User; users_count: number }) => void;
  user_left: (data: { user: User; users_count: number }) => void;
  users_updated: (data: { users: User[]; count: number }) => void;
  users_list: (data: { users: User[] }) => void;
  recent_messages: (data: { messages: Message[] }) => void;
  error: (data: { message: string }) => void;
}

// Estados de la aplicación
export interface ChatState {
  isConnected: boolean;
  currentUser: User | null;
  users: User[];
  messages: Message[];
  currentRoom: string;
}

// Tipos para notificaciones
export interface NotificationData {
  title: string;
  body: string;
  type?: 'info' | 'success' | 'warning' | 'error';
  autoHide?: boolean;
  duration?: number;
}

// Props para componentes
export interface ChatInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export interface MessageListProps {
  messages: Message[];
  currentUserId?: string;
}

export interface UserListProps {
  users: User[];
  currentUserId?: string;
}

export interface JoinChatFormProps {
  onJoin: (name: string) => void;
  isLoading?: boolean;
}

// Tipos para hooks personalizados
export interface UseSocketReturn {
  socket: import('socket.io-client').Socket | null;
  isConnected: boolean;
  joinChat: (name: string) => void;
  sendMessage: (content: string, roomId?: string) => void;
  getUsers: () => void;
}

export interface UseChatReturn extends ChatState {
  joinChat: (name: string) => void;
  sendMessage: (content: string) => void;
  refreshUsers: () => void;
}

// Configuración de la aplicación
export interface AppConfig {
  socketUrl: string;
  apiUrl: string;
  maxMessageLength: number;
  maxNameLength: number;
  reconnectAttempts: number;
  reconnectDelay: number;
}
