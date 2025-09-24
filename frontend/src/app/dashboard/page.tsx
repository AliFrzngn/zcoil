'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getClientSession } from '@/lib/auth';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { RecordsDashboard } from '@/components/dashboard/RecordsDashboard';

export default function DashboardPage() {
  const router = useRouter();
  const [session, setSession] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const userSession = getClientSession();
    if (!userSession) {
      router.push('/login');
      return;
    }
    setSession(userSession);
    setIsLoading(false);
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <DashboardLayout user={session.user}>
      <RecordsDashboard />
    </DashboardLayout>
  );
}