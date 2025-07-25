/**
 * Formatear fecha/hora para mostrar en el chat
 */
export const formatTimestamp = (timestamp: string): string => {
  const date = new Date(timestamp);
  const now = new Date();
  
  // Si es hoy, mostrar solo la hora
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    });
  }
  
  // Si es ayer, mostrar "Ayer HH:MM"
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  if (date.toDateString() === yesterday.toDateString()) {
    return `Ayer ${date.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    })}`;
  }
  
  // Si es otra fecha, mostrar fecha completa
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Truncar texto si es muy largo
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

/**
 * Validar nombre de usuario
 */
export const validateUsername = (name: string): { isValid: boolean; error?: string } => {
  const trimmedName = name.trim();
  
  if (!trimmedName) {
    return { isValid: false, error: 'El nombre es requerido' };
  }
  
  if (trimmedName.length < 2) {
    return { isValid: false, error: 'El nombre debe tener al menos 2 caracteres' };
  }
  
  if (trimmedName.length > 50) {
    return { isValid: false, error: 'El nombre no puede tener más de 50 caracteres' };
  }
  
  // Verificar caracteres válidos (solo letras, números, espacios y algunos caracteres especiales)
  const validNameRegex = /^[a-zA-Z0-9\s\-_\.]+$/;
  if (!validNameRegex.test(trimmedName)) {
    return { isValid: false, error: 'El nombre contiene caracteres no válidos' };
  }
  
  return { isValid: true };
};

/**
 * Validar contenido de mensaje
 */
export const validateMessage = (content: string): { isValid: boolean; error?: string } => {
  const trimmedContent = content.trim();
  
  if (!trimmedContent) {
    return { isValid: false, error: 'El mensaje no puede estar vacío' };
  }
  
  if (trimmedContent.length > 1000) {
    return { isValid: false, error: 'El mensaje no puede tener más de 1000 caracteres' };
  }
  
  return { isValid: true };
};

/**
 * Generar color único para usuario basado en su ID
 */
export const getUserColor = (userId: string): string => {
  const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
    '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2'
  ];
  
  // Usar hash simple del userId para seleccionar color
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    hash = userId.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  return colors[Math.abs(hash) % colors.length];
};

/**
 * Escapar HTML para prevenir XSS
 */
export const escapeHtml = (text: string): string => {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
};

/**
 * Detectar URLs en texto y convertirlas a enlaces
 */
export const linkifyText = (text: string): string => {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  return escapeHtml(text).replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">$1</a>');
};

/**
 * Formatear tiempo relativo (hace X minutos, hace X horas, etc.)
 */
export const getRelativeTime = (timestamp: string): string => {
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffMinutes < 1) {
    return 'ahora';
  } else if (diffMinutes < 60) {
    return `hace ${diffMinutes} min`;
  } else if (diffHours < 24) {
    return `hace ${diffHours} h`;
  } else {
    return `hace ${diffDays} d`;
  }
};

/**
 * Debounce function para limitar llamadas frecuentes
 */
export const debounce = <T extends (...args: unknown[]) => unknown>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void => {
  let timeoutId: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

/**
 * Throttle function para limitar frecuencia de ejecución
 */
export const throttle = <T extends (...args: unknown[]) => unknown>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void => {
  let lastCall = 0;
  
  return (...args: Parameters<T>) => {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      func(...args);
    }
  };
};
