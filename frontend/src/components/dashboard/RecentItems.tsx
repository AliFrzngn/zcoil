'use client';

import { useQuery } from '@tanstack/react-query';
import { crmApi } from '@/lib/api';

export function RecentItems() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['recent-items'],
    queryFn: () => crmApi.getMyItems(),
  });

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[...Array(3)].map((_, i) => (
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
        <p className="text-sm text-gray-500">Failed to load recent items</p>
      </div>
    );
  }

  const items = data?.data?.items?.slice(0, 5) || [];

  if (items.length === 0) {
    return (
      <div className="text-center py-4">
        <p className="text-sm text-gray-500">No items found</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item: any) => (
        <div key={item.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-900">{item.name}</p>
            <p className="text-xs text-gray-500">SKU: {item.sku}</p>
          </div>
          <div className="text-right">
            <p className="text-sm font-medium text-gray-900">${item.price}</p>
            <p className="text-xs text-gray-500">Qty: {item.quantity}</p>
          </div>
        </div>
      ))}
    </div>
  );
}