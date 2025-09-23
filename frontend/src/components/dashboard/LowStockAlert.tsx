'use client';

import { useQuery } from '@tanstack/react-query';
import { inventoryApi } from '@/lib/api';

export function LowStockAlert() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['low-stock-alert'],
    queryFn: () => inventoryApi.getLowStockItems(),
  });

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[...Array(2)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-3 bg-gray-200 rounded w-1/2 mt-1"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-4">
        <p className="text-sm text-gray-500">Failed to load low stock items</p>
      </div>
    );
  }

  const items = data?.data || [];

  if (items.length === 0) {
    return (
      <div className="text-center py-4">
        <div className="text-green-600 text-2xl mb-2">✅</div>
        <p className="text-sm text-gray-500">All items are well stocked</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {items.slice(0, 5).map((item: any) => (
        <div key={item.id} className="flex items-center justify-between py-2 border-b border-red-100 last:border-b-0">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-900">{item.name}</p>
            <p className="text-xs text-gray-500">SKU: {item.sku}</p>
          </div>
          <div className="text-right">
            <p className="text-sm font-medium text-red-600">{item.quantity} left</p>
            <p className="text-xs text-gray-500">Min: {item.min_quantity}</p>
          </div>
        </div>
      ))}
      {items.length > 5 && (
        <div className="text-center pt-2">
          <p className="text-xs text-gray-500">+{items.length - 5} more items</p>
        </div>
      )}
    </div>
  );
}