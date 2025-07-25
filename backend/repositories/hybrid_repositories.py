"""
Repositorios Híbridos - Memoria + Firebase Background

Este módulo implementa repositorios que combinan:
- Memoria: Para operaciones rápidas y síncronas
- Firebase: Para persistencia en background usando threading

Resuelve el problema de async/sync conflicts al mantener todas las operaciones
síncronas para el usuario mientras persiste datos a Firebase en background.
"""

import uuid
import logging
from datetime import datetime
from typing import List, Optional
import threading

from models import User, Message
from repositories import IUserRepository, IMessageRepository, InMemoryUserRepository, InMemoryMessageRepository

logger = logging.getLogger(__name__)

class HybridUserRepository(IUserRepository):
    """Repositorio híbrido: memoria para velocidad + Firebase para persistencia."""
    
    def __init__(self):
        # Usar solo memoria para operaciones síncronas
        self.memory_repo = InMemoryUserRepository()
        # Firebase se maneja en background
        self._firebase_enabled = False
        self._init_firebase()
    
    def _init_firebase(self):
        """Inicializar Firebase en background."""
        try:
            from services.firebase_service import FirebaseService
            self.firebase_service = FirebaseService()
            self._firebase_enabled = True
            logger.info("Firebase service initialized for background persistence")
        except Exception as e:
            logger.warning(f"Firebase not available: {e}")
            self._firebase_enabled = False
    
    def _persist_to_firebase(self, user: User):
        """Persistir usuario a Firebase en background."""
        if not self._firebase_enabled:
            return
        
        def background_save():
            try:
                self.firebase_service.create_user(user)
                logger.debug(f"User {user.name} persisted to Firebase")
            except Exception as e:
                logger.warning(f"Failed to persist user to Firebase: {e}")
        
        # Ejecutar en background thread
        thread = threading.Thread(target=background_save, daemon=True)
        thread.start()
    
    def create_user(self, name: str, socket_id: str = None) -> User:
        """Crear usuario en memoria y persistir a Firebase en background."""
        # Crear en memoria (operación síncrona rápida)
        user = self.memory_repo.create_user(name, socket_id)
        
        # Persistir a Firebase en background
        self._persist_to_firebase(user)
        
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID desde memoria."""
        return self.memory_repo.get_user_by_id(user_id)
    
    def get_user_by_socket_id(self, socket_id: str) -> Optional[User]:
        """Obtener usuario por socket ID desde memoria."""
        return self.memory_repo.get_user_by_socket_id(socket_id)
    
    def get_all_users(self) -> List[User]:
        """Obtener todos los usuarios desde memoria."""
        return self.memory_repo.get_all_users()
    
    def update_user_socket(self, user_id: str, socket_id: str) -> bool:
        """Actualizar socket ID del usuario."""
        return self.memory_repo.update_user_socket(user_id, socket_id)
    
    def deactivate_user(self, user_id: str) -> bool:
        """Desactivar usuario."""
        # Desactivar en memoria
        result = self.memory_repo.deactivate_user(user_id)
        
        # Actualizar estado en Firebase en background
        if self._firebase_enabled and result:
            def background_update():
                try:
                    self.firebase_service.update_user_status(user_id, False)
                    logger.debug(f"User {user_id} status updated in Firebase")
                except Exception as e:
                    logger.warning(f"Failed to update user status in Firebase: {e}")
            
            thread = threading.Thread(target=background_update, daemon=True)
            thread.start()
        
        return result
    
    def delete_user(self, user_id: str) -> bool:
        """Eliminar usuario."""
        return self.memory_repo.delete_user(user_id)


class HybridMessageRepository(IMessageRepository):
    """Repositorio híbrido para mensajes: memoria + Firebase background."""
    
    def __init__(self):
        # Usar solo memoria para operaciones síncronas
        self.memory_repo = InMemoryMessageRepository()
        # Firebase se maneja en background
        self._firebase_enabled = False
        self._init_firebase()
    
    def _init_firebase(self):
        """Inicializar Firebase en background."""
        try:
            from services.firebase_service import FirebaseService
            self.firebase_service = FirebaseService()
            self._firebase_enabled = True
            logger.info("Firebase service initialized for message persistence")
        except Exception as e:
            logger.warning(f"Firebase not available for messages: {e}")
            self._firebase_enabled = False
    
    def _persist_to_firebase(self, message: Message):
        """Persistir mensaje a Firebase en background."""
        if not self._firebase_enabled:
            return
        
        def background_save():
            try:
                self.firebase_service.save_message(message)
                logger.debug(f"Message {message.id} persisted to Firebase")
            except Exception as e:
                logger.warning(f"Failed to persist message to Firebase: {e}")
        
        # Ejecutar en background thread
        thread = threading.Thread(target=background_save, daemon=True)
        thread.start()
    
    def create_message(self, user_id: str, user_name: str, content: str, room_id: str = "general") -> Message:
        """Crear mensaje en memoria y persistir a Firebase en background."""
        # Crear en memoria (operación síncrona rápida)
        message = self.memory_repo.create_message(user_id, user_name, content, room_id)
        
        # Persistir a Firebase en background
        self._persist_to_firebase(message)
        
        return message
    
    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Obtener mensaje por ID desde memoria."""
        return self.memory_repo.get_message_by_id(message_id)
    
    def get_messages_by_room(self, room_id: str, limit: int = 50) -> List[Message]:
        """Obtener mensajes por sala desde memoria."""
        return self.memory_repo.get_messages_by_room(room_id, limit)
    
    def get_all_messages(self) -> List[Message]:
        """Obtener todos los mensajes desde memoria."""
        return self.memory_repo.get_all_messages()
    
    def get_recent_messages(self, limit: int = 50) -> List[Message]:
        """Obtener mensajes recientes desde memoria."""
        return self.memory_repo.get_recent_messages(limit)
    
    def delete_message(self, message_id: str) -> bool:
        """Eliminar mensaje."""
        return self.memory_repo.delete_message(message_id)
