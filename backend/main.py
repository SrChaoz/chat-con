import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from routers import users_router, messages_router
from services import create_chat_service
from services.firebase_async_wrapper import AsyncFirebaseService
from observers import ChatEventSubject, NotificationObserver, SocketIOObserver
from models import UserCreateRequest, MessageCreateRequest

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instancias globales
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.SOCKETIO_CORS_ORIGINS,
    logger=True,
    engineio_logger=True
)

# Patrón Observer - Subject para eventos del chat
event_subject = ChatEventSubject()

# Initialize Firebase service (async wrapper) - solo para observadores
firebase_service = AsyncFirebaseService()

# Create service layer - los repositorios manejan Firebase internamente
chat_service = create_chat_service(event_subject=event_subject, firebase_service=True)

# Observadores
from services.firebase_service import FirebaseService as SyncFirebaseService
sync_firebase_service = SyncFirebaseService()  # Para notificaciones
notification_observer = NotificationObserver(sync_firebase_service)
socketio_observer = SocketIOObserver(sio)

# Registrar observadores
event_subject.attach(notification_observer)
event_subject.attach(socketio_observer)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación."""
    logger.info("Starting Chat Application...")
    
    # Startup
    yield
    
    # Shutdown
    logger.info("Shutting down Chat Application...")


# Crear aplicación FastAPI
app = FastAPI(
    title="Chat Grupal API",
    description="API para chat grupal en tiempo real con Socket.IO y notificaciones",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users_router)
app.include_router(messages_router)

# Crear aplicación ASGI con Socket.IO
socket_app = socketio.ASGIApp(sio, app)


# Eventos de Socket.IO
@sio.event
async def connect(sid, environ):
    """Evento de conexión de Socket.IO."""
    logger.info(f"Client connected: {sid}")
    await sio.emit("connected", {"message": "Connected successfully"}, room=sid)


@sio.event
async def disconnect(sid):
    """Evento de desconexión de Socket.IO."""
    logger.info(f"Client disconnected: {sid}")
    
    # Desconectar usuario del chat
    user = chat_service.disconnect_user(sid)
    if user:
        logger.info(f"User {user.name} disconnected")
        
        # Actualizar lista de usuarios para todos los demás
        users = chat_service.get_all_users()
        await sio.emit("users_list", {
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "is_active": u.is_active,
                    "joined_at": u.joined_at.isoformat()
                }
                for u in users
            ]
        }, room="general")


@sio.event
async def join_chat(sid, data):
    """Evento para unirse al chat."""
    try:
        name = data.get("name", "").strip()
        if not name:
            await sio.emit("error", {"message": "Name is required"}, room=sid)
            return
        
        # Crear usuario
        user_request = UserCreateRequest(name=name)
        user = chat_service.create_user(user_request, sid)
        
        # Unir a la sala general
        await sio.enter_room(sid, "general")
        
        # Enviar confirmación al usuario
        await sio.emit("joined_chat", {
            "user": {
                "id": user.id,
                "name": user.name,
                "joined_at": user.joined_at.isoformat()
            },
            "message": f"Welcome to the chat, {user.name}!"
        }, room=sid)
        
        # Enviar lista de usuarios actuales solo al nuevo usuario
        users = chat_service.get_all_users()
        await sio.emit("users_list", {
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "is_active": u.is_active,
                    "joined_at": u.joined_at.isoformat()
                }
                for u in users
            ]
        }, room=sid)
        
        # Después de crear el usuario, notificar a TODOS en la sala sobre la lista actualizada
        await sio.emit("users_list", {
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "is_active": u.is_active,
                    "joined_at": u.joined_at.isoformat()
                }
                for u in users
            ]
        }, room="general")  # Enviar a toda la sala general
        
        # Enviar mensajes recientes
        messages = chat_service.get_messages_by_room("general", 20)
        await sio.emit("recent_messages", {
            "messages": [
                {
                    "id": msg.id,
                    "user_id": msg.user_id,
                    "user_name": msg.user_name,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "room_id": msg.room_id
                }
                for msg in messages
            ]
        }, room=sid)
        
        logger.info(f"User {name} joined the chat with ID {user.id}")
        
    except Exception as e:
        logger.error(f"Error in join_chat: {e}")
        await sio.emit("error", {"message": "Failed to join chat"}, room=sid)


@sio.event
async def send_message(sid, data):
    """Evento para enviar mensaje."""
    try:
        content = data.get("content", "").strip()
        room_id = data.get("room_id", "general")
        
        if not content:
            await sio.emit("error", {"message": "Message content is required"}, room=sid)
            return
        
        # Obtener usuario por socket ID
        user = chat_service.get_user_by_socket_id(sid)
        if not user:
            await sio.emit("error", {"message": "User not found"}, room=sid)
            return
        
        # Crear mensaje
        message_request = MessageCreateRequest(content=content, room_id=room_id)
        message = chat_service.create_message(user.id, message_request)
        
        if message:
            logger.info(f"Message sent by {user.name}: {content[:50]}...")
        else:
            await sio.emit("error", {"message": "Failed to send message"}, room=sid)
        
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        await sio.emit("error", {"message": "Failed to send message"}, room=sid)


@sio.event
async def get_users(sid):
    """Evento para obtener lista de usuarios."""
    try:
        users = chat_service.get_all_users()
        await sio.emit("users_list", {
            "users": [
                {
                    "id": user.id,
                    "name": user.name,
                    "is_active": user.is_active,
                    "joined_at": user.joined_at.isoformat()
                }
                for user in users
            ]
        }, room=sid)
        
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        await sio.emit("error", {"message": "Failed to get users"}, room=sid)


# Ruta de salud
@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud."""
    return {
        "status": "healthy",
        "service": "Chat Grupal API",
        "version": "1.0.0"
    }


# Ruta raíz
@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "Chat Grupal API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:socket_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
