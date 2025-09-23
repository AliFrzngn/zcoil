'use client';

import { Product } from '@/types/product';

interface CustomerProductCardProps {
  product: Product;
}

export function CustomerProductCard({ product }: CustomerProductCardProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
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

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="card-content">
        {/* Product Image/Icon */}
        <div className="flex items-center justify-center h-32 bg-gray-100 rounded-lg mb-4">
          <div className="text-4xl text-gray-400">
            {product.name.charAt(0).toUpperCase()}
          </div>
        </div>

        {/* Product Info */}
        <div className="space-y-3">
          <div>
            <h3 className="text-lg font-medium text-gray-900 truncate">
              {product.name}
            </h3>
            <p className="text-sm text-gray-500">SKU: {product.sku}</p>
          </div>

          <div className="flex items-center justify-between">
            <div className="text-xl font-bold text-gray-900">
              {formatPrice(product.price)}
            </div>
            {getStatusBadge(product.is_active)}
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Stock Level:</span>
              <span className="font-medium">{product.quantity} units</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Min Quantity:</span>
              <span className="font-medium">{product.min_quantity} units</span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500">
              {product.brand || 'No brand'} • {product.category || 'Uncategorized'}
            </div>
            {getStockBadge(product.quantity, product.min_quantity)}
          </div>

          {/* Description */}
          {product.description && (
            <p className="text-sm text-gray-600 line-clamp-3">
              {product.description}
            </p>
          )}

          {/* Stock Alert */}
          {product.quantity <= product.min_quantity && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <div className="flex items-center">
                <div className="text-yellow-600 mr-2">⚠️</div>
                <div className="text-sm text-yellow-800">
                  <strong>Low Stock Alert:</strong> This item is running low on inventory.
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}