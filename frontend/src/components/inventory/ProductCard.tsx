'use client';

import { useState } from 'react';
import { Product } from '@/types/product';
import { EditProductModal } from './EditProductModal';
import { DeleteProductModal } from './DeleteProductModal';
import { Button } from '@/components/ui/Button';
import { PencilIcon, TrashIcon, EyeIcon } from '@heroicons/react/24/outline';

interface ProductCardProps {
  product: Product;
  onRefresh: () => void;
}

export function ProductCard({ product, onRefresh }: ProductCardProps) {
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [deletingProduct, setDeletingProduct] = useState<Product | null>(null);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const getStatusBadge = (isActive: boolean) => {
    return isActive ? (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Active
      </span>
    ) : (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
        Inactive
      </span>
    );
  };

  const getStockBadge = (quantity: number, minQuantity: number) => {
    if (quantity <= 0) {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
          Out of Stock
        </span>
      );
    } else if (quantity <= minQuantity) {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
          Low Stock
        </span>
      );
    } else {
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          In Stock
        </span>
      );
    }
  };

  return (
    <>
      <div className="card hover:shadow-md transition-shadow">
        <div className="card-content">
          {/* Product Image/Icon */}
          <div className="flex items-center justify-center h-32 bg-gray-100 rounded-lg mb-4">
            <div className="text-4xl text-gray-400">
              {product.name.charAt(0).toUpperCase()}
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium text-gray-900 truncate">
              {product.name}
            </h3>
            <p className="text-sm text-gray-500">SKU: {product.sku}</p>
            <p className="text-sm text-gray-500">
              {product.brand || 'No brand'} • {product.category || 'Uncategorized'}
            </p>
            
            {/* Price */}
            <div className="text-xl font-bold text-gray-900">
              {formatPrice(product.price)}
            </div>

            {/* Stock and Status */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Stock: {product.quantity}</span>
                {getStockBadge(product.quantity, product.min_quantity)}
              </div>
              {getStatusBadge(product.is_active)}
            </div>

            {/* Description */}
            {product.description && (
              <p className="text-sm text-gray-600 line-clamp-2">
                {product.description}
              </p>
            )}
          </div>

          {/* Actions */}
          <div className="mt-4 flex items-center justify-between">
            <div className="flex space-x-2">
              <Button
                onClick={() => setEditingProduct(product)}
                variant="outline"
                size="sm"
              >
                <PencilIcon className="h-4 w-4 mr-1" />
                Edit
              </Button>
              <Button
                onClick={() => setDeletingProduct(product)}
                variant="outline"
                size="sm"
                className="text-red-600 hover:text-red-700"
              >
                <TrashIcon className="h-4 w-4 mr-1" />
                Delete
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Edit Product Modal */}
      {editingProduct && (
        <EditProductModal
          product={editingProduct}
          onClose={() => setEditingProduct(null)}
          onSuccess={() => {
            setEditingProduct(null);
            onRefresh();
          }}
        />
      )}

      {/* Delete Product Modal */}
      {deletingProduct && (
        <DeleteProductModal
          product={deletingProduct}
          onClose={() => setDeletingProduct(null)}
          onSuccess={() => {
            setDeletingProduct(null);
            onRefresh();
          }}
        />
      )}
    </>
  );
}