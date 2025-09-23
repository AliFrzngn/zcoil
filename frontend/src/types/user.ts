export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  phone?: string;
  bio?: string;
  role: 'admin' | 'manager' | 'customer';
  is_verified: boolean;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  last_login?: string;
  email_verified_at?: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  full_name?: string;
  phone?: string;
  bio?: string;
  role?: 'admin' | 'manager' | 'customer';
}

export interface UserUpdate {
  username?: string;
  email?: string;
  full_name?: string;
  phone?: string;
  bio?: string;
  role?: 'admin' | 'manager' | 'customer';
  is_verified?: boolean;
  is_active?: boolean;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserRegister {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
  full_name?: string;
  phone?: string;
}

export interface UserResponse {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  phone?: string;
  bio?: string;
  role: string;
  is_verified: boolean;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  last_login?: string;
  email_verified_at?: string;
}

export interface UserListResponse {
  items: UserResponse[];
  total: int;
  page: int;
  size: int;
  pages: int;
}

export interface PasswordChange {
  current_password: string;
  new_password: string;
}

export interface PasswordResetRequest {
  email: string;
}

export interface PasswordReset {
  token: string;
  new_password: string;
}
