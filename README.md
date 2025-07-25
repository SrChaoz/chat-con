
Una aplicación de chat grupal desarrollada con **Next.js** y **FastAPI** que permite a los usuarios comunicarse en tiempo real con notificaciones push integradas.

## 🚀 Características

- ✅ **Chat grupal en tiempo real** con Socket.IO
- ✅ **Interfaz moderna** desarrollada con Next.js y TypeScript
- ✅ **Backend robusto** con FastAPI y Python
- ✅ **Notificaciones push** con Firebase Cloud Messaging
- ✅ **Persistencia de datos** con Firebase Firestore
- ✅ **Lista de usuarios activos** en tiempo real
- ✅ **Arquitectura escalable** con patrón Observer

## 🛠️ Tecnologías

### Frontend
- **Next.js 14** - Framework de React
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos utilitarios
- **Socket.IO Client** - Comunicación en tiempo real
- **Lucide React** - Iconos

### Backend
- **FastAPI** - Framework web de Python
- **Socket.IO** - Comunicación bidireccional
- **Firebase Admin SDK** - Firestore y Cloud Messaging
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI

## 📋 Requisitos Previos

- **Node.js** 18+ y npm/yarn
- **Python** 3.11+ y pip
- **Cuenta de Firebase** con proyecto configurado

## 🔧 Instalación

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd CHAT-CON
```

### 2. Configurar el Backend

```bash
# Navegar al directorio del backend
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Crear archivo .env 
# Editar .env con tus credenciales de Firebase
# FIREBASE_PROJECT_ID=tu-proyecto-id
# FIREBASE_PRIVATE_KEY=tu-private-key
# etc.
```

### 3. Configurar el Frontend

```bash
# Navegar al directorio del frontend
cd ../frontend

# Instalar dependencias
npm install
# o con yarn:
yarn install
```

## 🚀 Ejecutar la Aplicación

### Iniciar el Backend

```bash
cd backend

# Activar entorno virtual si no está activo
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate     # Windows

# Ejecutar el servidor
python main.py
```

El backend estará disponible en: `http://localhost:8000`

### Iniciar el Frontend

```bash
cd frontend

# Ejecutar en modo desarrollo
npm run dev
# o con yarn:
yarn dev
```

El frontend estará disponible en: `http://localhost:3000`

## 📱 Uso de la Aplicación

1. **Acceder** a `http://localhost:3000`
2. **Ingresar tu nombre** en el formulario de entrada
3. **Unirse al chat** haciendo clic en "Unirse al Chat"
4. **Enviar mensajes** escribiendo en la caja de texto
5. **Ver usuarios activos** en la lista lateral
6. **Recibir notificaciones** cuando otros usuarios envíen mensajes

## 🔥 Configuración de Firebase

### 1. Crear Proyecto en Firebase
1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto
3. Habilita **Firestore Database**
4. Habilita **Cloud Messaging**

### 2. Obtener Credenciales
1. Ve a **Configuración del proyecto** → **Cuentas de servicio**
2. Genera una nueva clave privada
3. Descarga el archivo JSON
4. Renombra el archivo a `firebase-adminsdk.json`
5. Colócalo en el directorio `backend/`

### 3. Configurar Variables de Entorno
Completa el archivo `backend/.env` con los datos del archivo JSON:

```env
FIREBASE_PROJECT_ID=tu-proyecto-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-...@tu-proyecto.iam.gserviceaccount.com
# etc.
```

## 📁 Estructura del Proyecto

```
CHAT-CON/
├── backend/                  # Servidor FastAPI
│   ├── config/              # Configuraciones
│   ├── models/              # Modelos de datos
│   ├── repositories/        # Capa de datos
│   ├── services/            # Lógica de negocio
│   ├── routers/             # Endpoints API
│   ├── observers/           # Patrón Observer
│   ├── main.py              # Punto de entrada
│   ├── requirements.txt     # Dependencias Python
│   └── .env                 # Variables de entorno
│
├── frontend/                 # Aplicación Next.js
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── hooks/           # Custom hooks
│   │   ├── types/           # Definiciones TypeScript
│   │   ├── utils/           # Utilidades
│   │   └── app/             # Páginas Next.js
│   ├── package.json         # Dependencias Node.js
│   └── tailwind.config.js   # Configuración Tailwind
│
└── README.md                # Este archivo
```

## 🐛 Solución de Problemas

### Backend no se conecta a Firebase
- Verifica que el archivo `firebase-adminsdk.json` esté en `backend/`
- Revisa que las variables de entorno en `.env` sean correctas
- Asegúrate de que Firestore esté habilitado en Firebase Console

### Frontend no se conecta al backend
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Revisa la consola del navegador para errores de CORS
- Asegúrate de que Socket.IO esté funcionando

### Notificaciones no funcionan
- Las notificaciones push requieren configuración adicional del frontend
- Actualmente solo están implementadas en el backend
- Para notificaciones completas, se necesita registrar service workers

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autor

Desarrollado como proyecto de demostración de chat en tiempo real con Next.js y FastAPI.

---

## 🔍 Comandos Útiles

### Backend
```bash
# Ejecutar tests
python -m pytest

# Verificar conexión Firebase
python test_firebase.py

# Instalar nueva dependencia
pip install nueva-dependencia
pip freeze > requirements.txt
```

### Frontend
```bash
# Construir para producción
npm run build

# Ejecutar linter
npm run lint

# Verificar tipos TypeScript
npm run type-check
```

---

**¡Disfruta chateando! 💬✨**
