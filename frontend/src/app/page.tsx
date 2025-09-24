import { redirect } from 'next/navigation';

export default function HomePage() {
  // Always redirect to login for simplicity
  redirect('/login');
}