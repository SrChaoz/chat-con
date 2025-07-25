from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from models import User, Message, ChatRoom
import uuid
from datetime import datetime


class IUserRepository(ABC):
    """Interfaz para el repositorio de usuarios."""
    
    @abstractmethod
    def create_user(self, name: str, socket_id: Optional[str] = None) -> User:
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_user_by_socket_id(self, socket_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass
    
    @abstractmethod
    def update_user_socket(self, user_id: str, socket_id: str) -> bool:
        pass
    
    @abstractmethod
    def deactivate_user(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        pass


class IMessageRepository(ABC):
    """Interfaz para el repositorio de mensajes."""
    
    @abstractmethod
    def create_message(self, user_id: str, user_name: str, content: str, room_id: str = "general") -> Message:
        pass
    
    @abstractmethod
    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        pass
    
    @abstractmethod
    def get_messages_by_room(self, room_id: str, limit: int = 50) -> List[Message]:
        pass
    
    @abstractmethod
    def get_recent_messages(self, limit: int = 50) -> List[Message]:
        pass


class IChatRoomRepository(ABC):
    """Interfaz para el repositorio de salas de chat."""
    
    @abstractmethod
    def create_room(self, name: str) -> ChatRoom:
        pass
    
    @abstractmethod
    def get_room_by_id(self, room_id: str) -> Optional[ChatRoom]:
        pass
    
    @abstractmethod
    def get_all_rooms(self) -> List[ChatRoom]:
        pass
    
    @abstractmethod
    def add_user_to_room(self, room_id: str, user: User) -> bool:
        pass
    
    @abstractmethod
    def remove_user_from_room(self, room_id: str, user_id: str) -> bool:
        pass


class InMemoryUserRepository(IUserRepository):
    """Implementación en memoria del repositorio de usuarios."""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._socket_to_user: Dict[str, str] = {}
    
    def create_user(self, name: str, socket_id: Optional[str] = None) -> User:
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            name=name,
            socket_id=socket_id,
            is_active=True,
            joined_at=datetime.now()
        )
        self._users[user_id] = user
        
        if socket_id:
            self._socket_to_user[socket_id] = user_id
            
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def get_user_by_socket_id(self, socket_id: str) -> Optional[User]:
        user_id = self._socket_to_user.get(socket_id)
        if user_id:
            return self._users.get(user_id)
        return None
    
    def get_all_users(self) -> List[User]:
        return [user for user in self._users.values() if user.is_active]
    
    def update_user_socket(self, user_id: str, socket_id: str) -> bool:
        if user_id in self._users:
            # Remover mapping anterior si existe
            old_socket = self._users[user_id].socket_id
            if old_socket and old_socket in self._socket_to_user:
                del self._socket_to_user[old_socket]
            
            # Actualizar usuario y mapping
            self._users[user_id].socket_id = socket_id
            self._socket_to_user[socket_id] = user_id
            return True
        return False
    
    def deactivate_user(self, user_id: str) -> bool:
        if user_id in self._users:
            user = self._users[user_id]
            user.is_active = False
            
            # Remover socket mapping
            if user.socket_id and user.socket_id in self._socket_to_user:
                del self._socket_to_user[user.socket_id]
            user.socket_id = None
            
            return True
        return False
    
    def delete_user(self, user_id: str) -> bool:
        if user_id in self._users:
            user = self._users[user_id]
            
            # Remover socket mapping
            if user.socket_id and user.socket_id in self._socket_to_user:
                del self._socket_to_user[user.socket_id]
            
            del self._users[user_id]
            return True
        return False


class InMemoryMessageRepository(IMessageRepository):
    """Implementación en memoria del repositorio de mensajes."""
    
    def __init__(self):
        self._messages: Dict[str, Message] = {}
        self._room_messages: Dict[str, List[str]] = {}
    
    def create_message(self, user_id: str, user_name: str, content: str, room_id: str = "general") -> Message:
        message_id = str(uuid.uuid4())
        message = Message(
            id=message_id,
            user_id=user_id,
            user_name=user_name,
            content=content,
            room_id=room_id,
            timestamp=datetime.now()
        )
        
        self._messages[message_id] = message
        
        # Agregar a la lista de mensajes de la sala
        if room_id not in self._room_messages:
            self._room_messages[room_id] = []
        self._room_messages[room_id].append(message_id)
        
        return message
    
    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        return self._messages.get(message_id)
    
    def get_messages_by_room(self, room_id: str, limit: int = 50) -> List[Message]:
        message_ids = self._room_messages.get(room_id, [])
        messages = [self._messages[msg_id] for msg_id in message_ids[-limit:]]
        return sorted(messages, key=lambda x: x.timestamp)
    
    def get_recent_messages(self, limit: int = 50) -> List[Message]:
        all_messages = list(self._messages.values())
        return sorted(all_messages, key=lambda x: x.timestamp, reverse=True)[:limit]


class InMemoryChatRoomRepository(IChatRoomRepository):
    """Implementación en memoria del repositorio de salas de chat."""
    
    def __init__(self):
        self._rooms: Dict[str, ChatRoom] = {}
        # Crear sala general por defecto
        self.create_room("General")
    
    def create_room(self, name: str) -> ChatRoom:
        room_id = name.lower().replace(" ", "_")
        room = ChatRoom(
            id=room_id,
            name=name,
            users=[],
            messages=[],
            created_at=datetime.now(),
            is_active=True
        )
        self._rooms[room_id] = room
        return room
    
    def get_room_by_id(self, room_id: str) -> Optional[ChatRoom]:
        return self._rooms.get(room_id)
    
    def get_all_rooms(self) -> List[ChatRoom]:
        return [room for room in self._rooms.values() if room.is_active]
    
    def add_user_to_room(self, room_id: str, user: User) -> bool:
        room = self._rooms.get(room_id)
        if room:
            # Verificar si el usuario ya está en la sala
            for existing_user in room.users:
                if existing_user.id == user.id:
                    return True
            
            room.users.append(user)
            return True
        return False
    
    def remove_user_from_room(self, room_id: str, user_id: str) -> bool:
        room = self._rooms.get(room_id)
        if room:
            room.users = [user for user in room.users if user.id != user_id]
            return True
        return False
