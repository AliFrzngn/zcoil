'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { inventoryApi } from '@/lib/api';
import { Product } from '@/types/product';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface DeleteProductModalProps {
  product: Product;
  onClose: () => void;
  onSuccess: () => void;
}

export function DeleteProductModal({ product, onClose, onSuccess }: DeleteProductModalProps) {
  const queryClient = useQueryClient();

  const deleteProductMutation = useMutation({
    mutationFn: () => inventoryApi.deleteItem(product.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      onSuccess();
    },
    onError: (error: any) => {
      console.error('Failed to delete product:', error);
    },
  });

  const handleDelete = () => {
    deleteProductMutation.mutate();
  };

  return (
    <Modal onClose={onClose} title="Delete Product">
      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              Delete Product
            </h3>
            <p className="text-sm text-gray-500">
              This action cannot be undone.
            </p>
          </div>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-2">Product Details:</h4>
          <div className="space-y-1 text-sm text-gray-600">
            <p><strong>Name:</strong> {product.name}</p>
            <p><strong>SKU:</strong> {product.sku}</p>
            <p><strong>Price:</strong> ${product.price}</p>
            <p><strong>Stock:</strong> {product.quantity} units</p>
          </div>
        </div>

        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-700">
            <strong>Warning:</strong> Deleting this product will permanently remove it from your inventory. 
            All associated data will be lost.
          </p>
        </div>

        <div className="flex justify-end space-x-3">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={deleteProductMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            variant="danger"
            onClick={handleDelete}
            disabled={deleteProductMutation.isPending}
          >
            {deleteProductMutation.isPending ? 'Deleting...' : 'Delete Product'}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
