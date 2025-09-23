export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T = any> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  errors?: Record<string, string[]>;
  status_code: number;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: number;
    username: string;
    email: string;
    full_name?: string;
    role: string;
    is_verified: boolean;
  };
}

export interface FileUpload {
  id: number;
  filename: string;
  original_filename: string;
  file_path: string;
  file_size: number;
  content_type: string;
  user_id?: string;
  resource_type?: string;
  resource_id?: string;
  is_public: string;
  created_at: string;
}

export interface AuditLog {
  id: number;
  user_id?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  details?: string;
  metadata?: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  is_read: boolean;
  created_at: string;
  read_at?: string;
}