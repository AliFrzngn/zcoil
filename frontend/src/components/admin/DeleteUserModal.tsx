'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api';
import { User } from '@/types/user';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface DeleteUserModalProps {
  user: User;
  onClose: () => void;
  onSuccess: () => void;
}

export function DeleteUserModal({ user, onClose, onSuccess }: DeleteUserModalProps) {
  const queryClient = useQueryClient();

  const deleteUserMutation = useMutation({
    mutationFn: () => userApi.deleteUser(user.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] });
      onSuccess();
    },
    onError: (error: any) => {
      console.error('Failed to delete user:', error);
    },
  });

  const handleDelete = () => {
    deleteUserMutation.mutate();
  };

  return (
    <Modal onClose={onClose} title="Delete User">
      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              Delete User
            </h3>
            <p className="text-sm text-gray-500">
              This action cannot be undone.
            </p>
          </div>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-2">User Details:</h4>
          <div className="space-y-1 text-sm text-gray-600">
            <p><strong>Name:</strong> {user.full_name || user.username}</p>
            <p><strong>Username:</strong> @{user.username}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Role:</strong> {user.role}</p>
            <p><strong>Status:</strong> {user.is_active ? 'Active' : 'Inactive'}</p>
          </div>
        </div>

        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-700">
            <strong>Warning:</strong> Deleting this user will permanently remove their account and all associated data. 
            This action cannot be undone.
          </p>
        </div>

        <div className="flex justify-end space-x-3">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={deleteUserMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            variant="danger"
            onClick={handleDelete}
            disabled={deleteUserMutation.isPending}
          >
            {deleteUserMutation.isPending ? 'Deleting...' : 'Delete User'}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
