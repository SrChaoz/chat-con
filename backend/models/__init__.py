from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    TEXT = "text"
    SYSTEM = "system"
    NOTIFICATION = "notification"


class User(BaseModel):
    """Modelo para representar un usuario del chat."""
    id: str = Field(..., description="ID único del usuario")
    name: str = Field(..., min_length=1, max_length=50, description="Nombre del usuario")
    room: str = Field(default="general", description="Sala de chat del usuario")
    socket_id: Optional[str] = Field(None, description="ID del socket de conexión")
    is_active: bool = Field(True, description="Estado de actividad del usuario")
    is_online: bool = Field(True, description="Estado de conexión del usuario")
    joined_at: datetime = Field(default_factory=datetime.now, description="Fecha de ingreso")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Message(BaseModel):
    """Modelo para representar un mensaje del chat."""
    id: str = Field(..., description="ID único del mensaje")
    user_id: str = Field(..., description="ID del usuario que envía el mensaje")
    user_name: str = Field(..., description="Nombre del usuario que envía el mensaje")
    content: str = Field(..., min_length=1, max_length=1000, description="Contenido del mensaje")
    message_type: MessageType = Field(MessageType.TEXT, description="Tipo de mensaje")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del mensaje")
    room_id: str = Field("general", description="ID de la sala de chat")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ChatRoom(BaseModel):
    """Modelo para representar una sala de chat."""
    id: str = Field(..., description="ID único de la sala")
    name: str = Field(..., description="Nombre de la sala")
    users: List[User] = Field(default_factory=list, description="Lista de usuarios en la sala")
    messages: List[Message] = Field(default_factory=list, description="Lista de mensajes de la sala")
    created_at: datetime = Field(default_factory=datetime.now, description="Fecha de creación")
    is_active: bool = Field(True, description="Estado de la sala")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class NotificationData(BaseModel):
    """Modelo para datos de notificación."""
    title: str = Field(..., description="Título de la notificación")
    body: str = Field(..., description="Cuerpo de la notificación")
    user_id: str = Field(..., description="ID del usuario destinatario")
    message_id: Optional[str] = Field(None, description="ID del mensaje relacionado")
    data: Optional[dict] = Field(default_factory=dict, description="Datos adicionales")


# DTOs (Data Transfer Objects)
class UserCreateRequest(BaseModel):
    """DTO para la creación de usuarios."""
    name: str = Field(..., min_length=1, max_length=50)


class MessageCreateRequest(BaseModel):
    """DTO para la creación de mensajes."""
    content: str = Field(..., min_length=1, max_length=1000)
    room_id: str = Field("general")


class UserResponse(BaseModel):
    """DTO para respuesta de usuario."""
    id: str
    name: str
    is_active: bool
    joined_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MessageResponse(BaseModel):
    """DTO para respuesta de mensaje."""
    id: str
    user_id: str
    user_name: str
    content: str
    message_type: MessageType
    timestamp: datetime
    room_id: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
