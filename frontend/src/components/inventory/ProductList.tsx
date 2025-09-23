'use client';

import { useState } from 'react';
import { ProductCard } from './ProductCard';
import { ProductTable } from './ProductTable';
import { Pagination } from '@/components/ui/Pagination';
import { Button } from '@/components/ui/Button';
import { ViewColumnsIcon, Squares2X2Icon } from '@heroicons/react/24/outline';

interface ProductListProps {
  data?: any;
  isLoading: boolean;
  error: any;
  onPageChange: (page: number) => void;
  onRefresh: () => void;
}

export function ProductList({ data, isLoading, error, onPageChange, onRefresh }: ProductListProps) {
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('table');

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-16 bg-gray-200 rounded"></div>
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
        <p className="text-gray-500 mb-4">There was an error loading the product list.</p>
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
      {/* View Controls */}
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-500">
          Showing {products.length} of {total} products
        </div>
        <div className="flex space-x-2">
          <Button
            onClick={() => setViewMode('table')}
            variant={viewMode === 'table' ? 'primary' : 'outline'}
            size="sm"
          >
            <ViewColumnsIcon className="h-4 w-4" />
          </Button>
          <Button
            onClick={() => setViewMode('grid')}
            variant={viewMode === 'grid' ? 'primary' : 'outline'}
            size="sm"
          >
            <Squares2X2Icon className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Products */}
      {products.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 text-4xl mb-4">📦</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No products found</h3>
          <p className="text-gray-500">Get started by adding your first product.</p>
        </div>
      ) : (
        <>
          {viewMode === 'table' ? (
            <ProductTable products={products} onRefresh={onRefresh} />
          ) : (
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {products.map((product: any) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onRefresh={onRefresh}
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
