'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { crmApi } from '@/lib/api';
import { CRMLayout } from '@/components/crm/CRMLayout';
import { CustomerProductList } from '@/components/crm/CustomerProductList';
import { CustomerStats } from '@/components/crm/CustomerStats';

export default function CRMPage() {
  const [filters, setFilters] = useState({
    name: '',
    category: '',
    brand: '',
    page: 1,
    size: 10
  });

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['crm', 'my-items', filters],
    queryFn: () => crmApi.getMyItems(filters),
  });

  const handleFiltersChange = (newFilters: any) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  return (
    <CRMLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Products</h1>
          <p className="mt-1 text-sm text-gray-500">
            View and manage products associated with your account
          </p>
        </div>

        {/* Stats */}
        <CustomerStats data={data?.data} />

        {/* Product List */}
        <CustomerProductList
          data={data?.data}
          isLoading={isLoading}
          error={error}
          filters={filters}
          onFiltersChange={handleFiltersChange}
          onPageChange={handlePageChange}
          onRefresh={refetch}
        />
      </div>
    </CRMLayout>
  );
}
