'use client';

import { StatsCard } from '@/components/ui/StatsCard';

interface CustomerStatsProps {
  data?: any;
}

export function CustomerStats({ data }: CustomerStatsProps) {
  const products = data?.items || [];
  
  const stats = {
    totalProducts: products.length,
    totalValue: products.reduce((sum: number, product: any) => sum + (product.price * product.quantity), 0),
    lowStockItems: products.filter((product: any) => product.quantity <= product.min_quantity).length,
    categories: [...new Set(products.map((product: any) => product.category).filter(Boolean))].length,
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <StatsCard
        title="Total Products"
        value={stats.totalProducts}
        icon="📦"
        description="Products in your inventory"
      />
      <StatsCard
        title="Total Value"
        value={formatCurrency(stats.totalValue)}
        icon="💰"
        description="Total inventory value"
      />
      <StatsCard
        title="Low Stock Items"
        value={stats.lowStockItems}
        icon="⚠️"
        description="Items needing restock"
        variant={stats.lowStockItems > 0 ? 'warning' : 'default'}
      />
      <StatsCard
        title="Categories"
        value={stats.categories}
        icon="🏷️"
        description="Product categories"
      />
    </div>
  );
}