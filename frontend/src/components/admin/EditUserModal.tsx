'use client';

import { useState, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api';
import { User, UserUpdate } from '@/types/user';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';

interface EditUserModalProps {
  user: User;
  onClose: () => void;
  onSuccess: () => void;
}

const roleOptions = [
  { value: 'customer', label: 'Customer' },
  { value: 'manager', label: 'Manager' },
  { value: 'admin', label: 'Admin' },
];

export function EditUserModal({ user, onClose, onSuccess }: EditUserModalProps) {
  const [formData, setFormData] = useState<UserUpdate>({
    username: '',
    email: '',
    full_name: '',
    phone: '',
    bio: '',
    role: 'customer',
    is_verified: false,
    is_active: true,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const queryClient = useQueryClient();

  useEffect(() => {
    setFormData({
      username: user.username || '',
      email: user.email || '',
      full_name: user.full_name || '',
      phone: user.phone || '',
      bio: user.bio || '',
      role: user.role || 'customer',
      is_verified: user.is_verified || false,
      is_active: user.is_active ?? true,
    });
  }, [user]);

  const updateUserMutation = useMutation({
    mutationFn: (data: UserUpdate) => userApi.updateUser(user.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] });
      onSuccess();
    },
    onError: (error: any) => {
      if (error.response?.data?.detail) {
        setErrors({ general: error.response.data.detail });
      } else if (error.response?.data?.errors) {
        setErrors(error.response.data.errors);
      } else {
        setErrors({ general: 'Failed to update user' });
      }
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validation
    const newErrors: Record<string, string> = {};
    if (!formData.username?.trim()) newErrors.username = 'Username is required';
    if (!formData.email?.trim()) newErrors.email = 'Email is required';
    if (!formData.full_name?.trim()) newErrors.full_name = 'Full name is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    updateUserMutation.mutate(formData);
  };

  const handleChange = (field: keyof UserUpdate, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <Modal onClose={onClose} title="Edit User" size="lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        {errors.general && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {errors.general}
          </div>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {/* Username */}
          <div>
            <Input
              label="Username *"
              type="text"
              value={formData.username || ''}
              onChange={(e) => handleChange('username', e.target.value)}
              placeholder="Enter username"
              error={errors.username}
            />
          </div>

          {/* Email */}
          <div>
            <Input
              label="Email *"
              type="email"
              value={formData.email || ''}
              onChange={(e) => handleChange('email', e.target.value)}
              placeholder="Enter email"
              error={errors.email}
            />
          </div>

          {/* Full Name */}
          <div>
            <Input
              label="Full Name *"
              type="text"
              value={formData.full_name || ''}
              onChange={(e) => handleChange('full_name', e.target.value)}
              placeholder="Enter full name"
              error={errors.full_name}
            />
          </div>

          {/* Phone */}
          <div>
            <Input
              label="Phone"
              type="tel"
              value={formData.phone || ''}
              onChange={(e) => handleChange('phone', e.target.value)}
              placeholder="Enter phone number"
              error={errors.phone}
            />
          </div>

          {/* Role */}
          <div>
            <Select
              label="Role *"
              value={formData.role || 'customer'}
              onChange={(e) => handleChange('role', e.target.value)}
              options={roleOptions}
            />
          </div>

          {/* Status */}
          <div>
            <Select
              label="Account Status"
              value={formData.is_active?.toString() || 'true'}
              onChange={(e) => handleChange('is_active', e.target.value === 'true')}
              options={[
                { value: 'true', label: 'Active' },
                { value: 'false', label: 'Inactive' },
              ]}
            />
          </div>
        </div>

        {/* Bio */}
        <div>
          <Textarea
            label="Bio"
            value={formData.bio || ''}
            onChange={(e) => handleChange('bio', e.target.value)}
            placeholder="Enter user bio"
            rows={3}
          />
        </div>

        {/* Verification Status */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_verified"
              checked={formData.is_verified || false}
              onChange={(e) => handleChange('is_verified', e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="is_verified" className="ml-2 block text-sm text-gray-900">
              Email Verified
            </label>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-3 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={updateUserMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={updateUserMutation.isPending}
          >
            {updateUserMutation.isPending ? 'Updating...' : 'Update User'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
