'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { inventoryApi } from '@/lib/api';
import { InventoryLayout } from '@/components/inventory/InventoryLayout';
import { ProductList } from '@/components/inventory/ProductList';
import { ProductFilters } from '@/components/inventory/ProductFilters';
import { CreateProductModal } from '@/components/inventory/CreateProductModal';
import { Button } from '@/components/ui/Button';
import { PlusIcon } from '@heroicons/react/24/outline';

export default function InventoryPage() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filters, setFilters] = useState({
    name: '',
    category: '',
    brand: '',
    is_active: undefined as boolean | undefined,
    min_price: undefined as number | undefined,
    max_price: undefined as number | undefined,
    page: 1,
    size: 10
  });

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['inventory', filters],
    queryFn: () => inventoryApi.getItems(filters),
  });

  const handleFiltersChange = (newFilters: any) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  return (
    <InventoryLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Inventory Management</h1>
            <p className="mt-1 text-sm text-gray-500">
              Manage your product inventory and stock levels
            </p>
          </div>
          <Button
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary btn-md"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Product
          </Button>
        </div>

        {/* Filters */}
        <ProductFilters
          filters={filters}
          onFiltersChange={handleFiltersChange}
        />

        {/* Product List */}
        <ProductList
          data={data?.data}
          isLoading={isLoading}
          error={error}
          onPageChange={handlePageChange}
          onRefresh={refetch}
        />

        {/* Create Product Modal */}
        {showCreateModal && (
          <CreateProductModal
            onClose={() => setShowCreateModal(false)}
            onSuccess={() => {
              setShowCreateModal(false);
              refetch();
            }}
          />
        )}
      </div>
    </InventoryLayout>
  );
}
