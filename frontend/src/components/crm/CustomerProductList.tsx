'use client';

import { useState } from 'react';
import { CustomerProductCard } from './CustomerProductCard';
import { CustomerProductTable } from './CustomerProductTable';
import { Pagination } from '@/components/ui/Pagination';
import { Button } from '@/components/ui/Button';
import { ViewColumnsIcon, Squares2X2Icon, FunnelIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';

interface CustomerProductListProps {
  data?: any;
  isLoading: boolean;
  error: any;
  filters: any;
  onFiltersChange: (filters: any) => void;
  onPageChange: (page: number) => void;
  onRefresh: () => void;
}

const categories = [
  { value: '', label: 'All Categories' },
  { value: 'electronics', label: 'Electronics' },
  { value: 'clothing', label: 'Clothing' },
  { value: 'books', label: 'Books' },
  { value: 'home', label: 'Home & Garden' },
  { value: 'sports', label: 'Sports' },
  { value: 'toys', label: 'Toys' },
  { value: 'other', label: 'Other' },
];

export function CustomerProductList({ 
  data, 
  isLoading, 
  error, 
  filters, 
  onFiltersChange, 
  onPageChange, 
  onRefresh 
}: CustomerProductListProps) {
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [showFilters, setShowFilters] = useState(false);

  const handleFilterChange = (key: string, value: any) => {
    onFiltersChange({ [key]: value });
  };

  const clearFilters = () => {
    onFiltersChange({
      name: '',
      category: '',
      brand: '',
    });
  };

  const hasActiveFilters = filters.name || filters.category || filters.brand;

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-32 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-2xl mb-4">⚠️</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">Failed to load products</h3>
        <p className="text-gray-500 mb-4">There was an error loading your products.</p>
        <Button onClick={onRefresh} className="btn btn-outline">
          Try Again
        </Button>
      </div>
    );
  }

  const products = data?.items || [];
  const total = data?.total || 0;
  const page = data?.page || 1;
  const pages = data?.pages || 1;

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-500">
          Showing {products.length} of {total} products
        </div>
        <div className="flex items-center space-x-2">
          <Button
            onClick={() => setShowFilters(!showFilters)}
            variant="outline"
            size="sm"
          >
            <FunnelIcon className="h-4 w-4 mr-1" />
            Filters
          </Button>
          <div className="flex space-x-1">
            <Button
              onClick={() => setViewMode('grid')}
              variant={viewMode === 'grid' ? 'primary' : 'outline'}
              size="sm"
            >
              <Squares2X2Icon className="h-4 w-4" />
            </Button>
            <Button
              onClick={() => setViewMode('table')}
              variant={viewMode === 'table' ? 'primary' : 'outline'}
              size="sm"
            >
              <ViewColumnsIcon className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">Filters</h3>
            <div className="flex items-center space-x-2">
              {hasActiveFilters && (
                <Button
                  onClick={clearFilters}
                  variant="outline"
                  size="sm"
                >
                  <XMarkIcon className="h-4 w-4 mr-1" />
                  Clear
                </Button>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Search
              </label>
              <Input
                type="text"
                placeholder="Search products..."
                value={filters.name || ''}
                onChange={(e) => handleFilterChange('name', e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <Select
                value={filters.category || ''}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                options={categories}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Brand
              </label>
              <Input
                type="text"
                placeholder="Brand name"
                value={filters.brand || ''}
                onChange={(e) => handleFilterChange('brand', e.target.value)}
              />
            </div>
          </div>
        </div>
      )}

      {/* Products */}
      {products.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 text-4xl mb-4">📦</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No products found</h3>
          <p className="text-gray-500">No products are currently associated with your account.</p>
        </div>
      ) : (
        <>
          {viewMode === 'table' ? (
            <CustomerProductTable products={products} />
          ) : (
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {products.map((product: any) => (
                <CustomerProductCard
                  key={product.id}
                  product={product}
                />
              ))}
            </div>
          )}

          {/* Pagination */}
          {pages > 1 && (
            <Pagination
              currentPage={page}
              totalPages={pages}
              onPageChange={onPageChange}
            />
          )}
        </>
      )}
    </div>
  );
}