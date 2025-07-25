"""
Wrapper asíncrono para FirebaseService
"""

import asyncio
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

from services.firebase_service import FirebaseService as SyncFirebaseService
from models import User, Message

class AsyncFirebaseService:
    """Wrapper asíncrono para el servicio Firebase síncrono."""
    
    def __init__(self):
        self._sync_service = SyncFirebaseService()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    async def create_user(self, user: User) -> bool:
        """Crear usuario de forma asíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, 
            self._sync_service.create_user, 
            user
        )
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Obtener usuario de forma asíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, 
            self._sync_service.get_user, 
            user_id
        )
    
    async def save_message(self, message: Message) -> bool:
        """Guardar mensaje de forma asíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, 
            self._sync_service.save_message, 
            message
        )
    
    async def get_messages_by_room(self, room: str, limit: int = 50) -> List[Message]:
        """Obtener mensajes de una sala de forma asíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, 
            self._sync_service.get_messages_by_room, 
            room, 
            limit
        )
    
    async def get_users_by_room(self, room: str) -> List[User]:
        """Obtener usuarios de una sala de forma asíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, 
            self._sync_service.get_users_by_room, 
            room
        )
    
    async def update_user_status(self, user_id: str, is_online: bool) -> bool:
        """Actualizar estado del usuario de forma asíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, 
            self._sync_service.update_user_status, 
            user_id, 
            is_online
        )
    
    async def send_notification(self, token: str, title: str, body: str, data: dict = None) -> bool:
        """Enviar notificación de forma asíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, 
            self._sync_service.send_notification, 
            token, 
            title, 
            body, 
            data
        )
    
    def __del__(self):
        """Cleanup del executor."""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False)
