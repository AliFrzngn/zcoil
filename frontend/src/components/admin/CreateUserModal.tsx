'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api';
import { UserCreate } from '@/types/user';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';

interface CreateUserModalProps {
  onClose: () => void;
  onSuccess: () => void;
}

const roleOptions = [
  { value: 'customer', label: 'Customer' },
  { value: 'manager', label: 'Manager' },
  { value: 'admin', label: 'Admin' },
];

export function CreateUserModal({ onClose, onSuccess }: CreateUserModalProps) {
  const [formData, setFormData] = useState<UserCreate>({
    username: '',
    email: '',
    password: '',
    full_name: '',
    phone: '',
    bio: '',
    role: 'customer',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const queryClient = useQueryClient();

  const createUserMutation = useMutation({
    mutationFn: (data: UserCreate) => userApi.updateUser(0, data), // Using updateUser as placeholder
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
        setErrors({ general: 'Failed to create user' });
      }
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validation
    const newErrors: Record<string, string> = {};
    if (!formData.username.trim()) newErrors.username = 'Username is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!formData.password.trim()) newErrors.password = 'Password is required';
    if (formData.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
    if (!formData.full_name?.trim()) newErrors.full_name = 'Full name is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    createUserMutation.mutate(formData);
  };

  const handleChange = (field: keyof UserCreate, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <Modal onClose={onClose} title="Create New User" size="lg">
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
              value={formData.username}
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
              value={formData.email}
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

          {/* Password */}
          <div>
            <Input
              label="Password *"
              type="password"
              value={formData.password}
              onChange={(e) => handleChange('password', e.target.value)}
              placeholder="Enter password"
              error={errors.password}
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

        {/* Actions */}
        <div className="flex justify-end space-x-3 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={createUserMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={createUserMutation.isPending}
          >
            {createUserMutation.isPending ? 'Creating...' : 'Create User'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
