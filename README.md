
Una aplicación de chat grupal desarrollada con **Next.js** y **FastAPI** que permite a los usuarios comunicarse en tiempo real con notificaciones push integradas.


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

### Configurar Variables de Entorno
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


