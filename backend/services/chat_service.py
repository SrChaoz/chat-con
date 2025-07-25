from typing import List, Optional
from models import User, Message, ChatRoom, UserCreateRequest, MessageCreateRequest
from repositories import (
    IUserRepository, IMessageRepository, IChatRoomRepository,
    InMemoryUserRepository, InMemoryMessageRepository, InMemoryChatRoomRepository
)
from observers import ChatEventSubject
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Servicio principal para la gestión del chat."""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        message_repository: IMessageRepository,
        room_repository: IChatRoomRepository,
        event_subject: ChatEventSubject
    ):
        self.user_repository = user_repository
        self.message_repository = message_repository
        self.room_repository = room_repository
        self.event_subject = event_subject
    
    # Métodos para usuarios
    def create_user(self, user_request: UserCreateRequest, socket_id: Optional[str] = None) -> User:
        """Crear un nuevo usuario."""
        try:
            user = self.user_repository.create_user(user_request.name, socket_id)
            
            # Agregar usuario a la sala general
            self.room_repository.add_user_to_room("general", user)
            
            # Notificar que un usuario se unió
            active_users = self.user_repository.get_all_users()
            self.event_subject.notify("user_joined", {
                "user": user,
                "users": active_users
            })
            
            logger.info(f"User created: {user.name} (ID: {user.id})")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID."""
        return self.user_repository.get_user_by_id(user_id)
    
    def get_user_by_socket_id(self, socket_id: str) -> Optional[User]:
        """Obtener usuario por socket ID."""
        return self.user_repository.get_user_by_socket_id(socket_id)
    
    def get_all_users(self) -> List[User]:
        """Obtener todos los usuarios activos."""
        return self.user_repository.get_all_users()
    
    def update_user_socket(self, user_id: str, socket_id: str) -> bool:
        """Actualizar el socket de un usuario."""
        success = self.user_repository.update_user_socket(user_id, socket_id)
        
        if success:
            # Notificar actualización de usuarios
            active_users = self.user_repository.get_all_users()
            self.event_subject.notify("users_updated", {
                "users": active_users
            })
        
        return success
    
    def disconnect_user(self, socket_id: str) -> Optional[User]:
        """Desconectar un usuario por socket ID."""
        try:
            user = self.user_repository.get_user_by_socket_id(socket_id)
            if user:
                # Desactivar usuario
                self.user_repository.deactivate_user(user.id)
                
                # Remover de salas
                rooms = self.room_repository.get_all_rooms()
                for room in rooms:
                    self.room_repository.remove_user_from_room(room.id, user.id)
                
                # Notificar que el usuario salió
                active_users = self.user_repository.get_all_users()
                self.event_subject.notify("user_left", {
                    "user": user,
                    "users": active_users
                })
                
                logger.info(f"User disconnected: {user.name} (ID: {user.id})")
                return user
            
            return None
            
        except Exception as e:
            logger.error(f"Error disconnecting user: {e}")
            return None
    
    # Métodos para mensajes
    def create_message(self, user_id: str, message_request: MessageCreateRequest) -> Optional[Message]:
        """Crear un nuevo mensaje."""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                logger.warning(f"User not found: {user_id}")
                return None
            
            message = self.message_repository.create_message(
                user_id=user.id,
                user_name=user.name,
                content=message_request.content,
                room_id=message_request.room_id
            )
            
            # Notificar nuevo mensaje
            room_users = self._get_users_in_room(message_request.room_id)
            self.event_subject.notify("message_sent", {
                "message": message,
                "users": room_users,
                "room_id": message_request.room_id
            })
            
            logger.info(f"Message created by {user.name}: {message.content[:50]}...")
            return message
            
        except Exception as e:
            logger.error(f"Error creating message: {e}")
            return None
    
    def get_messages_by_room(self, room_id: str, limit: int = 50) -> List[Message]:
        """Obtener mensajes de una sala."""
        return self.message_repository.get_messages_by_room(room_id, limit)
    
    def get_recent_messages(self, limit: int = 50) -> List[Message]:
        """Obtener mensajes recientes."""
        return self.message_repository.get_recent_messages(limit)
    
    # Métodos para salas
    def get_room_by_id(self, room_id: str) -> Optional[ChatRoom]:
        """Obtener sala por ID."""
        return self.room_repository.get_room_by_id(room_id)
    
    def get_all_rooms(self) -> List[ChatRoom]:
        """Obtener todas las salas."""
        return self.room_repository.get_all_rooms()
    
    def join_room(self, user_id: str, room_id: str) -> bool:
        """Unir usuario a una sala."""
        user = self.user_repository.get_user_by_id(user_id)
        if user:
            return self.room_repository.add_user_to_room(room_id, user)
        return False
    
    def leave_room(self, user_id: str, room_id: str) -> bool:
        """Sacar usuario de una sala."""
        return self.room_repository.remove_user_from_room(room_id, user_id)
    
    def _get_users_in_room(self, room_id: str) -> List[User]:
        """Obtener usuarios en una sala específica."""
        room = self.room_repository.get_room_by_id(room_id)
        if room:
            return room.users
        return []


# Factory para crear instancia del servicio de chat
def create_chat_service(event_subject: ChatEventSubject, firebase_service=None) -> ChatService:
    """Factory para crear una instancia del servicio de chat."""
    if firebase_service:
        # Usar repositorios híbridos simples (memoria + Firebase background)
        from repositories.hybrid_repositories import HybridUserRepository, HybridMessageRepository
        user_repository = HybridUserRepository()
        message_repository = HybridMessageRepository()
    else:
        # Usar repositorios en memoria
        user_repository = InMemoryUserRepository()
        message_repository = InMemoryMessageRepository()
    
    room_repository = InMemoryChatRoomRepository()
    
    return ChatService(
        user_repository=user_repository,
        message_repository=message_repository,
        room_repository=room_repository,
        event_subject=event_subject
    )
