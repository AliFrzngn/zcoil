export interface Product {
  id: number;
  name: string;
  description?: string;
  sku: string;
  price: number;
  quantity: number;
  min_quantity: number;
  category?: string;
  brand?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ProductCreate {
  name: string;
  description?: string;
  sku: string;
  price: number;
  quantity: number;
  min_quantity: number;
  category?: string;
  brand?: string;
  is_active?: boolean;
}

export interface ProductUpdate {
  name?: string;
  description?: string;
  sku?: string;
  price?: number;
  quantity?: number;
  min_quantity?: number;
  category?: string;
  brand?: string;
  is_active?: boolean;
}

export interface ProductResponse {
  id: number;
  name: string;
  description?: string;
  sku: string;
  price: number;
  quantity: number;
  min_quantity: number;
  category?: string;
  brand?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ProductListResponse {
  items: ProductResponse[];
  total: int;
  page: int;
  size: int;
  pages: int;
}

export interface ProductFilters {
  name?: string;
  category?: string;
  brand?: string;
  is_active?: boolean;
  min_price?: number;
  max_price?: number;
  page?: number;
  size?: number;
}

export interface LowStockItem {
  id: number;
  name: string;
  sku: string;
  quantity: number;
  min_quantity: number;
  category?: string;
  brand?: string;
}