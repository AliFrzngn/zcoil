'use client';

import { useQuery } from '@tanstack/react-query';
import { userApi, inventoryApi, crmApi } from '@/lib/api';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { StatsCard } from '@/components/ui/StatsCard';
import { Card } from '@/components/ui/Card';

export default function AdminDashboardPage() {
  const { data: usersData } = useQuery({
    queryKey: ['admin', 'users', 'stats'],
    queryFn: () => userApi.getUsers({ size: 1 }),
  });

  const { data: inventoryData } = useQuery({
    queryKey: ['inventory', 'stats'],
    queryFn: () => inventoryApi.getItems({ size: 1 }),
  });

  const { data: crmData } = useQuery({
    queryKey: ['crm', 'stats'],
    queryFn: () => crmApi.getMyItems({ size: 1 }),
  });

  const stats = {
    totalUsers: usersData?.data?.total || 0,
    totalProducts: inventoryData?.data?.total || 0,
    totalCustomerProducts: crmData?.data?.total || 0,
    activeUsers: usersData?.data?.items?.filter((user: any) => user.is_active)?.length || 0,
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Overview of system statistics and recent activity
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <StatsCard
            title="Total Users"
            value={stats.totalUsers}
            icon="👥"
            description="Registered users"
          />
          <StatsCard
            title="Active Users"
            value={stats.activeUsers}
            icon="✅"
            description="Currently active"
          />
          <StatsCard
            title="Total Products"
            value={stats.totalProducts}
            icon="📦"
            description="In inventory"
          />
          <StatsCard
            title="Customer Products"
            value={stats.totalCustomerProducts}
            icon="🛒"
            description="Customer associations"
          />
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <Card>
            <div className="card-content">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <a
                  href="/admin/users"
                  className="block p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <div className="text-2xl mr-3">👥</div>
                    <div>
                      <p className="font-medium text-gray-900">Manage Users</p>
                      <p className="text-sm text-gray-500">View and manage user accounts</p>
                    </div>
                  </div>
                </a>
                <a
                  href="/admin/inventory"
                  className="block p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <div className="text-2xl mr-3">📦</div>
                    <div>
                      <p className="font-medium text-gray-900">Manage Inventory</p>
                      <p className="text-sm text-gray-500">View and manage products</p>
                    </div>
                  </div>
                </a>
                <a
                  href="/admin/settings"
                  className="block p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <div className="text-2xl mr-3">⚙️</div>
                    <div>
                      <p className="font-medium text-gray-900">System Settings</p>
                      <p className="text-sm text-gray-500">Configure system preferences</p>
                    </div>
                  </div>
                </a>
              </div>
            </div>
          </Card>

          <Card>
            <div className="card-content">
              <h3 className="text-lg font-medium text-gray-900 mb-4">System Status</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Database</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Online
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">API Services</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Online
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Email Service</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                    Configured
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">File Storage</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Available
                  </span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </AdminLayout>
  );
}
