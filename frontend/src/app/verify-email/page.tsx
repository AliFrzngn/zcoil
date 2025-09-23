'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

export default function VerifyEmailPage() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get('token');

  const verifyEmailMutation = useMutation({
    mutationFn: (token: string) => authApi.verifyEmail(token),
    onSuccess: (response) => {
      setStatus('success');
      setMessage('Your email has been successfully verified! You can now access all features of the application.');
    },
    onError: (error: any) => {
      setStatus('error');
      setMessage(error.message || 'Failed to verify email. The token may be invalid or expired.');
    },
  });

  useEffect(() => {
    if (token) {
      verifyEmailMutation.mutate(token);
    } else {
      setStatus('error');
      setMessage('No verification token provided.');
    }
  }, [token]);

  const handleContinue = () => {
    router.push('/dashboard');
  };

  const handleResend = () => {
    // This would trigger resend verification email
    router.push('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 flex items-center justify-center">
            {status === 'loading' && (
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            )}
            {status === 'success' && (
              <CheckCircleIcon className="h-12 w-12 text-green-600" />
            )}
            {status === 'error' && (
              <XCircleIcon className="h-12 w-12 text-red-600" />
            )}
          </div>
          
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            {status === 'loading' && 'Verifying Email...'}
            {status === 'success' && 'Email Verified!'}
            {status === 'error' && 'Verification Failed'}
          </h2>
          
          <p className="mt-2 text-sm text-gray-600">
            {message}
          </p>
        </div>

        <div className="mt-8 space-y-4">
          {status === 'success' && (
            <Button
              onClick={handleContinue}
              className="w-full"
            >
              Continue to Dashboard
            </Button>
          )}
          
          {status === 'error' && (
            <div className="space-y-3">
              <Button
                onClick={handleResend}
                variant="outline"
                className="w-full"
              >
                Request New Verification Email
              </Button>
              <Button
                onClick={() => router.push('/login')}
                className="w-full"
              >
                Back to Login
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
