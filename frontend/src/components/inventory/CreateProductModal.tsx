'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { inventoryApi } from '@/lib/api';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';

interface CreateProductModalProps {
  onClose: () => void;
  onSuccess: () => void;
}

const categories = [
  { value: 'electronics', label: 'Electronics' },
  { value: 'clothing', label: 'Clothing' },
  { value: 'books', label: 'Books' },
  { value: 'home', label: 'Home & Garden' },
  { value: 'sports', label: 'Sports' },
  { value: 'toys', label: 'Toys' },
  { value: 'other', label: 'Other' },
];

export function CreateProductModal({ onClose, onSuccess }: CreateProductModalProps) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    sku: '',
    price: '',
    quantity: '',
    min_quantity: '',
    category: '',
    brand: '',
    is_active: true,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const queryClient = useQueryClient();

  const createProductMutation = useMutation({
    mutationFn: (data: any) => inventoryApi.createItem(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      onSuccess();
    },
    onError: (error: any) => {
      if (error.response?.data?.detail) {
        setErrors({ general: error.response.data.detail });
      } else if (error.response?.data?.errors) {
        setErrors(error.response.data.errors);
      } else {
        setErrors({ general: 'Failed to create product' });
      }
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validation
    const newErrors: Record<string, string> = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.sku.trim()) newErrors.sku = 'SKU is required';
    if (!formData.price || parseFloat(formData.price) <= 0) newErrors.price = 'Valid price is required';
    if (!formData.quantity || parseInt(formData.quantity) < 0) newErrors.quantity = 'Valid quantity is required';
    if (!formData.min_quantity || parseInt(formData.min_quantity) < 0) newErrors.min_quantity = 'Valid minimum quantity is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const submitData = {
      ...formData,
      price: parseFloat(formData.price),
      quantity: parseInt(formData.quantity),
      min_quantity: parseInt(formData.min_quantity),
    };

    createProductMutation.mutate(submitData);
  };

  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <Modal onClose={onClose} title="Create New Product">
      <form onSubmit={handleSubmit} className="space-y-4">
        {errors.general && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {errors.general}
          </div>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {/* Name */}
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Product Name *
            </label>
            <Input
              type="text"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              placeholder="Enter product name"
              error={errors.name}
            />
          </div>

          {/* SKU */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              SKU *
            </label>
            <Input
              type="text"
              value={formData.sku}
              onChange={(e) => handleChange('sku', e.target.value)}
              placeholder="Enter SKU"
              error={errors.sku}
            />
          </div>

          {/* Brand */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Brand
            </label>
            <Input
              type="text"
              value={formData.brand}
              onChange={(e) => handleChange('brand', e.target.value)}
              placeholder="Enter brand"
            />
          </div>

          {/* Price */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Price *
            </label>
            <Input
              type="number"
              value={formData.price}
              onChange={(e) => handleChange('price', e.target.value)}
              placeholder="0.00"
              step="0.01"
              min="0"
              error={errors.price}
            />
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <Select
              value={formData.category}
              onChange={(e) => handleChange('category', e.target.value)}
              options={[{ value: '', label: 'Select category' }, ...categories]}
            />
          </div>

          {/* Quantity */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Quantity *
            </label>
            <Input
              type="number"
              value={formData.quantity}
              onChange={(e) => handleChange('quantity', e.target.value)}
              placeholder="0"
              min="0"
              error={errors.quantity}
            />
          </div>

          {/* Min Quantity */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Min Quantity *
            </label>
            <Input
              type="number"
              value={formData.min_quantity}
              onChange={(e) => handleChange('min_quantity', e.target.value)}
              placeholder="0"
              min="0"
              error={errors.min_quantity}
            />
          </div>

          {/* Status */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <Select
              value={formData.is_active.toString()}
              onChange={(e) => handleChange('is_active', e.target.value === 'true')}
              options={[
                { value: 'true', label: 'Active' },
                { value: 'false', label: 'Inactive' },
              ]}
            />
          </div>
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <Textarea
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            placeholder="Enter product description"
            rows={3}
          />
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-3 pt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={createProductMutation.isPending}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={createProductMutation.isPending}
          >
            {createProductMutation.isPending ? 'Creating...' : 'Create Product'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}