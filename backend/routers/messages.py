from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from models import MessageCreateRequest, MessageResponse
from services import ChatService

router = APIRouter(prefix="/api/messages", tags=["messages"])


def get_chat_service() -> ChatService:
    """Dependency para obtener el servicio de chat."""
    from main import chat_service
    return chat_service


@router.post("/", response_model=MessageResponse)
async def create_message(
    message_request: MessageCreateRequest,
    user_id: str = Query(..., description="ID del usuario que envía el mensaje"),
    chat_service: ChatService = Depends(get_chat_service)
):
    """Crear un nuevo mensaje."""
    try:
        message = chat_service.create_message(user_id, message_request)
        if not message:
            raise HTTPException(status_code=400, detail="Failed to create message")
        
        return MessageResponse(
            id=message.id,
            user_id=message.user_id,
            user_name=message.user_name,
            content=message.content,
            message_type=message.message_type,
            timestamp=message.timestamp,
            room_id=message.room_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/room/{room_id}", response_model=List[MessageResponse])
async def get_messages_by_room(
    room_id: str,
    limit: int = Query(50, ge=1, le=100, description="Número máximo de mensajes"),
    chat_service: ChatService = Depends(get_chat_service)
):
    """Obtener mensajes de una sala específica."""
    try:
        messages = chat_service.get_messages_by_room(room_id, limit)
        return [
            MessageResponse(
                id=message.id,
                user_id=message.user_id,
                user_name=message.user_name,
                content=message.content,
                message_type=message.message_type,
                timestamp=message.timestamp,
                room_id=message.room_id
            )
            for message in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent", response_model=List[MessageResponse])
async def get_recent_messages(
    limit: int = Query(50, ge=1, le=100, description="Número máximo de mensajes"),
    chat_service: ChatService = Depends(get_chat_service)
):
    """Obtener mensajes recientes."""
    try:
        messages = chat_service.get_recent_messages(limit)
        return [
            MessageResponse(
                id=message.id,
                user_id=message.user_id,
                user_name=message.user_name,
                content=message.content,
                message_type=message.message_type,
                timestamp=message.timestamp,
                room_id=message.room_id
            )
            for message in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
