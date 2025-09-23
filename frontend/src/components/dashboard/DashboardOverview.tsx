'use client';

import { useQuery } from '@tanstack/react-query';
import { inventoryApi, crmApi } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { StatsCard } from '@/components/ui/StatsCard';
import { RecentItems } from '@/components/dashboard/RecentItems';
import { LowStockAlert } from '@/components/dashboard/LowStockAlert';

export function DashboardOverview() {
  const { data: inventoryStats } = useQuery({
    queryKey: ['inventory-stats'],
    queryFn: () => inventoryApi.getItems({ size: 1 }),
  });

  const { data: myItems } = useQuery({
    queryKey: ['my-items'],
    queryFn: () => crmApi.getMyItems(),
  });

  const { data: lowStockItems } = useQuery({
    queryKey: ['low-stock-items'],
    queryFn: () => inventoryApi.getLowStockItems(),
  });

  const totalProducts = inventoryStats?.data?.total || 0;
  const myProductsCount = myItems?.data?.items?.length || 0;
  const lowStockCount = lowStockItems?.data?.length || 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome back! Here's what's happening with your business.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Products"
          value={totalProducts}
          icon="📦"
          description="Products in inventory"
        />
        <StatsCard
          title="My Products"
          value={myProductsCount}
          icon="👤"
          description="Products assigned to you"
        />
        <StatsCard
          title="Low Stock Items"
          value={lowStockCount}
          icon="⚠️"
          description="Items needing restock"
          alert={lowStockCount > 0}
        />
        <StatsCard
          title="Active Users"
          value="1,234"
          icon="👥"
          description="Total active users"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Items */}
        <Card>
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Recent Items</h3>
            <p className="text-sm text-gray-500">Latest products in your inventory</p>
          </div>
          <div className="card-content">
            <RecentItems />
          </div>
        </Card>

        {/* Low Stock Alert */}
        <Card>
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Low Stock Alert</h3>
            <p className="text-sm text-gray-500">Items that need immediate attention</p>
          </div>
          <div className="card-content">
            <LowStockAlert />
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
          <p className="text-sm text-gray-500">Common tasks and shortcuts</p>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <button className="btn btn-outline btn-md">
              Add New Product
            </button>
            <button className="btn btn-outline btn-md">
              View All Products
            </button>
            <button className="btn btn-outline btn-md">
              Manage Users
            </button>
            <button className="btn btn-outline btn-md">
              Send Notification
            </button>
          </div>
        </div>
      </Card>
    </div>
  );
}