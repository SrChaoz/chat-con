import os
from dotenv import load_dotenv
from typing import List

# Cargar variables de entorno
load_dotenv()


class Settings:
    """Configuración de la aplicación - Patrón Singleton."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        # Configuración de Firebase
        self.FIREBASE_CONFIG = {
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
        }
        
        # Configuración de CORS
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        self.CORS_ORIGINS: List[str] = [origin.strip() for origin in cors_origins.split(",")]
        
        # Configuración del servidor
        self.HOST = "0.0.0.0"
        self.PORT = 8000
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        
        # Configuración de Socket.IO
        self.SOCKETIO_CORS_ORIGINS = self.CORS_ORIGINS
        
        self._initialized = True


# Instancia global de configuración
settings = Settings()
