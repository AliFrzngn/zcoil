'use client';

import { useState } from 'react';
import { User } from '@/types/user';
import { EditUserModal } from './EditUserModal';
import { DeleteUserModal } from './DeleteUserModal';
import { Button } from '@/components/ui/Button';
import { PencilIcon, TrashIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

interface UserCardProps {
  user: User;
  onRefresh: () => void;
}

export function UserCard({ user, onRefresh }: UserCardProps) {
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [deletingUser, setDeletingUser] = useState<User | null>(null);

  const getRoleBadge = (role: string) => {
    const roleColors = {
      admin: 'bg-red-100 text-red-800',
      manager: 'bg-blue-100 text-blue-800',
      customer: 'bg-green-100 text-green-800',
    };
    
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${roleColors[role as keyof typeof roleColors] || 'bg-gray-100 text-gray-800'}`}>
        {role.charAt(0).toUpperCase() + role.slice(1)}
      </span>
    );
  };

  const getVerificationBadge = (isVerified: boolean) => {
    return isVerified ? (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        <CheckCircleIcon className="h-3 w-3 mr-1" />
        Verified
      </span>
    ) : (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        <XCircleIcon className="h-3 w-3 mr-1" />
        Unverified
      </span>
    );
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <>
      <div className="card hover:shadow-md transition-shadow">
        <div className="card-content">
          {/* User Avatar */}
          <div className="flex items-center justify-center h-20 w-20 bg-gray-100 rounded-full mx-auto mb-4">
            <span className="text-2xl font-medium text-gray-500">
              {user.full_name?.charAt(0) || user.username.charAt(0).toUpperCase()}
            </span>
          </div>

          {/* User Info */}
          <div className="text-center space-y-2">
            <h3 className="text-lg font-medium text-gray-900">
              {user.full_name || user.username}
            </h3>
            <p className="text-sm text-gray-500">@{user.username}</p>
            <p className="text-sm text-gray-600">{user.email}</p>
            
            {/* Role and Status */}
            <div className="flex items-center justify-center space-x-2">
              {getRoleBadge(user.role)}
              {getVerificationBadge(user.is_verified)}
            </div>

            {/* Additional Info */}
            <div className="space-y-1 text-sm text-gray-500">
              <p>Joined: {formatDate(user.created_at)}</p>
              {user.last_login && (
                <p>Last login: {formatDate(user.last_login)}</p>
              )}
            </div>

            {/* Bio */}
            {user.bio && (
              <p className="text-sm text-gray-600 line-clamp-2">
                {user.bio}
              </p>
            )}
          </div>

          {/* Actions */}
          <div className="mt-4 flex items-center justify-center space-x-2">
            <Button
              onClick={() => setEditingUser(user)}
              variant="outline"
              size="sm"
            >
              <PencilIcon className="h-4 w-4 mr-1" />
              Edit
            </Button>
            <Button
              onClick={() => setDeletingUser(user)}
              variant="outline"
              size="sm"
              className="text-red-600 hover:text-red-700"
            >
              <TrashIcon className="h-4 w-4 mr-1" />
              Delete
            </Button>
          </div>
        </div>
      </div>

      {/* Edit User Modal */}
      {editingUser && (
        <EditUserModal
          user={editingUser}
          onClose={() => setEditingUser(null)}
          onSuccess={() => {
            setEditingUser(null);
            onRefresh();
          }}
        />
      )}

      {/* Delete User Modal */}
      {deletingUser && (
        <DeleteUserModal
          user={deletingUser}
          onClose={() => setDeletingUser(null)}
          onSuccess={() => {
            setDeletingUser(null);
            onRefresh();
          }}
        />
      )}
    </>
  );
}