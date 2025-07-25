from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import UserCreateRequest, UserResponse
from services import ChatService

router = APIRouter(prefix="/api/users", tags=["users"])


def get_chat_service() -> ChatService:
    """Dependency para obtener el servicio de chat."""
    # En una aplicación real, esto vendría de un contenedor de dependencias
    from main import chat_service
    return chat_service


@router.post("/", response_model=UserResponse)
async def create_user(
    user_request: UserCreateRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Crear un nuevo usuario."""
    try:
        user = chat_service.create_user(user_request)
        return UserResponse(
            id=user.id,
            name=user.name,
            is_active=user.is_active,
            joined_at=user.joined_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    chat_service: ChatService = Depends(get_chat_service)
):
    """Obtener todos los usuarios activos."""
    try:
        users = chat_service.get_all_users()
        return [
            UserResponse(
                id=user.id,
                name=user.name,
                is_active=user.is_active,
                joined_at=user.joined_at
            )
            for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Obtener un usuario por ID."""
    try:
        user = chat_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user.id,
            name=user.name,
            is_active=user.is_active,
            joined_at=user.joined_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
