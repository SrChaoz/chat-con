import React from 'react';
import { UserListProps } from '@/types';
import { getUserColor, getRelativeTime } from '@/utils';
import { Users, Crown, Circle } from 'lucide-react';

export const UserList: React.FC<UserListProps> = ({ users, currentUserId }) => {
  if (users.length === 0) {
    return (
      <div className="bg-white border-l h-full">
        <div className="p-4 border-b">
          <div className="flex items-center space-x-2">
            <Users className="w-5 h-5 text-gray-600" />
            <h3 className="font-semibold text-gray-900">Participantes</h3>
            <span className="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-full">
              0
            </span>
          </div>
        </div>
        <div className="p-4 text-center text-gray-500">
          <Users className="w-8 h-8 mx-auto mb-2 text-gray-300" />
          <p className="text-sm">No hay usuarios conectados</p>
        </div>
      </div>
    );
  }

  // Ordenar usuarios: usuario actual primero, luego por orden alfabético
  const sortedUsers = [...users].sort((a, b) => {
    if (a.id === currentUserId) return -1;
    if (b.id === currentUserId) return 1;
    return a.name.localeCompare(b.name);
  });

  return (
    <div className="bg-white border-l h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b bg-gray-50">
        <div className="flex items-center space-x-2">
          <Users className="w-5 h-5 text-gray-600" />
          <h3 className="font-semibold text-gray-900">Participantes</h3>
          <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full">
            {users.length}
          </span>
        </div>
      </div>

      {/* Lista de usuarios */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-2">
          {sortedUsers.map((user) => {
            const isCurrentUser = user.id === currentUserId;
            const userColor = getUserColor(user.id);
            
            return (
              <div
                key={user.id}
                className={`flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors ${
                  isCurrentUser ? 'bg-blue-50 border border-blue-200' : ''
                }`}
              >
                {/* Avatar */}
                <div 
                  className="relative w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-medium"
                  style={{ backgroundColor: userColor }}
                >
                  {user.name.charAt(0).toUpperCase()}
                  
                  {/* Indicador de estado online */}
                  <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-400 border-2 border-white rounded-full" />
                </div>

                {/* Información del usuario */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-1">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {user.name}
                    </p>
                    {isCurrentUser && (
                      <div title="Tú">
                        <Crown className="w-3 h-3 text-yellow-500" />
                      </div>
                    )}
                  </div>
                  
                  <div className="flex items-center space-x-1">
                    <Circle className="w-2 h-2 text-green-400 fill-current" />
                    <p className="text-xs text-gray-500">
                      {isCurrentUser ? 'Tú' : `Conectado ${getRelativeTime(user.joined_at)}`}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Footer con estadísticas */}
      <div className="p-3 border-t bg-gray-50">
        <div className="text-xs text-gray-500 text-center">
          {users.length === 1 ? '1 persona conectada' : `${users.length} personas conectadas`}
        </div>
      </div>
    </div>
  );
};
