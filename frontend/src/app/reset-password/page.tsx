'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

export default function ResetPasswordPage() {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [status, setStatus] = useState<'form' | 'success' | 'error'>('form');
  const [message, setMessage] = useState('');
  
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get('token');

  const resetPasswordMutation = useMutation({
    mutationFn: (data: { token: string; new_password: string }) => 
      authApi.resetPassword(data),
    onSuccess: () => {
      setStatus('success');
      setMessage('Your password has been successfully reset! You can now log in with your new password.');
    },
    onError: (error: any) => {
      setStatus('error');
      setMessage(error.message || 'Failed to reset password. The token may be invalid or expired.');
    },
  });

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('No reset token provided.');
    }
  }, [token]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validation
    const newErrors: Record<string, string> = {};
    if (!password) newErrors.password = 'Password is required';
    if (password.length < 8) newErrors.password = 'Password must be at least 8 characters';
    if (!confirmPassword) newErrors.confirmPassword = 'Please confirm your password';
    if (password !== confirmPassword) newErrors.confirmPassword = 'Passwords do not match';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    if (token) {
      resetPasswordMutation.mutate({ token, new_password: password });
    }
  };

  const handleContinue = () => {
    router.push('/login');
  };

  const handleBackToLogin = () => {
    router.push('/login');
  };

  if (status === 'success') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <CheckCircleIcon className="mx-auto h-12 w-12 text-green-600" />
            <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
              Password Reset Successfully!
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              {message}
            </p>
          </div>
          <Button onClick={handleContinue} className="w-full">
            Continue to Login
          </Button>
        </div>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <XCircleIcon className="mx-auto h-12 w-12 text-red-600" />
            <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
              Reset Failed
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              {message}
            </p>
          </div>
          <Button onClick={handleBackToLogin} className="w-full">
            Back to Login
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Reset Your Password
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Enter your new password below
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Input
              label="New Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter new password"
              error={errors.password}
            />
            
            <Input
              label="Confirm Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password"
              error={errors.confirmPassword}
            />
          </div>

          <div>
            <Button
              type="submit"
              className="w-full"
              disabled={resetPasswordMutation.isPending}
            >
              {resetPasswordMutation.isPending ? 'Resetting...' : 'Reset Password'}
            </Button>
          </div>

          <div className="text-center">
            <Button
              type="button"
              variant="outline"
              onClick={handleBackToLogin}
            >
              Back to Login
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
