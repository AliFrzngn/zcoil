'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { userApi } from '@/lib/api';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { UserList } from '@/components/admin/UserList';
import { UserFilters } from '@/components/admin/UserFilters';
import { CreateUserModal } from '@/components/admin/CreateUserModal';
import { Button } from '@/components/ui/Button';
import { PlusIcon } from '@heroicons/react/24/outline';

export default function UsersPage() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filters, setFilters] = useState({
    username: '',
    email: '',
    role: '',
    is_verified: undefined as boolean | undefined,
    page: 1,
    size: 10
  });

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['admin', 'users', filters],
    queryFn: () => userApi.getUsers(filters),
  });

  const handleFiltersChange = (newFilters: any) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">User Management</h1>
            <p className="mt-1 text-sm text-gray-500">
              Manage user accounts and permissions
            </p>
          </div>
          <Button
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary btn-md"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add User
          </Button>
        </div>

        {/* Filters */}
        <UserFilters
          filters={filters}
          onFiltersChange={handleFiltersChange}
        />

        {/* User List */}
        <UserList
          data={data?.data}
          isLoading={isLoading}
          error={error}
          onPageChange={handlePageChange}
          onRefresh={refetch}
        />

        {/* Create User Modal */}
        {showCreateModal && (
          <CreateUserModal
            onClose={() => setShowCreateModal(false)}
            onSuccess={() => {
              setShowCreateModal(false);
              refetch();
            }}
          />
        )}
      </div>
    </AdminLayout>
  );
}
