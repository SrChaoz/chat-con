from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models import User, Message, NotificationData
import logging
import asyncio

logger = logging.getLogger(__name__)


class IObserver(ABC):
    """Interfaz para observadores."""
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        pass


class ISubject(ABC):
    """Interfaz para sujetos observables."""
    
    @abstractmethod
    def attach(self, observer: IObserver) -> None:
        pass
    
    @abstractmethod
    def detach(self, observer: IObserver) -> None:
        pass
    
    @abstractmethod
    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        pass


class ChatEventSubject(ISubject):
    """Sujeto observable para eventos del chat."""
    
    def __init__(self):
        self._observers: List[IObserver] = []
    
    def attach(self, observer: IObserver) -> None:
        """Agregar un observador."""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Observer {observer.__class__.__name__} attached")
    
    def detach(self, observer: IObserver) -> None:
        """Remover un observador."""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Observer {observer.__class__.__name__} detached")
    
    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        """Notificar a todos los observadores."""
        logger.info(f"Notifying {len(self._observers)} observers about event: {event_type}")
        for observer in self._observers:
            try:
                observer.update(event_type, data)
            except Exception as e:
                logger.error(f"Error notifying observer {observer.__class__.__name__}: {e}")


class NotificationObserver(IObserver):
    """Observador para el manejo de notificaciones."""
    
    def __init__(self, notification_service):
        self.notification_service = notification_service
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Procesar eventos y generar notificaciones."""
        try:
            if event_type == "message_sent":
                self._handle_message_notification(data)
            elif event_type == "user_joined":
                self._handle_user_joined_notification(data)
            elif event_type == "user_left":
                self._handle_user_left_notification(data)
        except Exception as e:
            logger.error(f"Error processing notification for event {event_type}: {e}")
    
    def _handle_message_notification(self, data: Dict[str, Any]) -> None:
        """Manejar notificaciones de mensajes."""
        message: Message = data.get("message")
        users: List[User] = data.get("users", [])
        
        if not message or not users:
            return
        
        # Crear notificación para todos los usuarios excepto el remitente
        for user in users:
            if user.id != message.user_id:
                notification_data = NotificationData(
                    title=f"Nuevo mensaje de {message.user_name}",
                    body=message.content[:100] + "..." if len(message.content) > 100 else message.content,
                    user_id=user.id,
                    message_id=message.id,
                    data={
                        "type": "new_message",
                        "room_id": message.room_id,
                        "sender_name": message.user_name
                    }
                )
                
                # Enviar notificación (si el servicio está configurado)
                self.notification_service.send_notification(notification_data)
    
    def _handle_user_joined_notification(self, data: Dict[str, Any]) -> None:
        """Manejar notificaciones de usuario que se une."""
        user: User = data.get("user")
        users: List[User] = data.get("users", [])
        
        if not user or not users:
            return
        
        # Notificar a todos los usuarios existentes
        for existing_user in users:
            if existing_user.id != user.id:
                notification_data = NotificationData(
                    title="Nuevo participante",
                    body=f"{user.name} se ha unido al chat",
                    user_id=existing_user.id,
                    data={
                        "type": "user_joined",
                        "user_name": user.name,
                        "user_id": user.id
                    }
                )
                
                self.notification_service.send_notification(notification_data)
    
    def _handle_user_left_notification(self, data: Dict[str, Any]) -> None:
        """Manejar notificaciones de usuario que sale."""
        user: User = data.get("user")
        users: List[User] = data.get("users", [])
        
        if not user or not users:
            return
        
        # Notificar a todos los usuarios restantes
        for existing_user in users:
            notification_data = NotificationData(
                title="Participante salió",
                body=f"{user.name} ha salido del chat",
                user_id=existing_user.id,
                data={
                    "type": "user_left",
                    "user_name": user.name,
                    "user_id": user.id
                }
            )
            
            self.notification_service.send_notification(notification_data)


import asyncio

class SocketIOObserver(IObserver):
    """Observador para eventos de Socket.IO."""
    
    def __init__(self, socketio_instance):
        self.sio = socketio_instance
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Procesar eventos y emitir via Socket.IO usando asyncio.create_task."""
        try:
            # Crear una tarea asíncrona para manejar el evento
            asyncio.create_task(self._async_update(event_type, data))
        except Exception as e:
            logger.error(f"Error creating async task for SocketIO event {event_type}: {e}")
    
    async def _async_update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Versión asíncrona del update."""
        try:
            if event_type == "message_sent":
                await self._handle_message_broadcast(data)
            elif event_type == "user_joined":
                await self._handle_user_joined_broadcast(data)
            elif event_type == "user_left":
                await self._handle_user_left_broadcast(data)
            elif event_type == "users_updated":
                await self._handle_users_updated_broadcast(data)
        except Exception as e:
            logger.error(f"Error broadcasting via SocketIO for event {event_type}: {e}")
    
    async def _handle_message_broadcast(self, data: Dict[str, Any]) -> None:
        """Broadcast de mensajes a todos los clientes."""
        message: Message = data.get("message")
        room_id = data.get("room_id", "general")
        
        if message:
            await self.sio.emit("new_message", {
                "id": message.id,
                "user_id": message.user_id,
                "user_name": message.user_name,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "room_id": message.room_id
            }, room=room_id)
            logger.info(f"Broadcasted message from {message.user_name} to room {room_id}")
    
    async def _handle_user_joined_broadcast(self, data: Dict[str, Any]) -> None:
        """Broadcast cuando un usuario se une."""
        user: User = data.get("user")
        users: List[User] = data.get("users", [])
        
        if user:
            # Emitir evento de usuario que se unió
            await self.sio.emit("user_joined", {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "joined_at": user.joined_at.isoformat()
                },
                "users_count": len(users)
            }, room="general")
            
            # También emitir la lista actualizada de usuarios
            users_data = [
                {
                    "id": u.id,
                    "name": u.name,
                    "is_active": u.is_active,
                    "joined_at": u.joined_at.isoformat()
                }
                for u in users
            ]
            
            await self.sio.emit("users_list", {
                "users": users_data,
                "count": len(users_data)
            }, room="general")
    
    async def _handle_user_left_broadcast(self, data: Dict[str, Any]) -> None:
        """Broadcast cuando un usuario sale."""
        user: User = data.get("user")
        users: List[User] = data.get("users", [])
        
        if user:
            # Emitir evento de usuario que salió
            await self.sio.emit("user_left", {
                "user": {
                    "id": user.id,
                    "name": user.name
                },
                "users_count": len(users)
            }, room="general")
            
            # También emitir la lista actualizada de usuarios
            users_data = [
                {
                    "id": u.id,
                    "name": u.name,
                    "is_active": u.is_active,
                    "joined_at": u.joined_at.isoformat()
                }
                for u in users
            ]
            
            await self.sio.emit("users_list", {
                "users": users_data,
                "count": len(users_data)
            }, room="general")
    
    async def _handle_users_updated_broadcast(self, data: Dict[str, Any]) -> None:
        """Broadcast cuando la lista de usuarios se actualiza."""
        users: List[User] = data.get("users", [])
        
        users_data = [
            {
                "id": user.id,
                "name": user.name,
                "is_active": user.is_active,
                "joined_at": user.joined_at.isoformat()
            }
            for user in users
        ]
        
        await self.sio.emit("users_updated", {
            "users": users_data,
            "count": len(users_data)
        }, room="general")
