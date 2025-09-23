'use client';

import Link from 'next/link';
import { ArrowRightIcon, CheckIcon } from '@heroicons/react/24/outline';

const features = [
  {
    name: 'Inventory Management',
    description: 'Complete product and inventory management with real-time tracking.',
    icon: '📦',
  },
  {
    name: 'Customer Relationship',
    description: 'Manage customer relationships and product associations.',
    icon: '👥',
  },
  {
    name: 'User Authentication',
    description: 'Secure user management with role-based access control.',
    icon: '🔐',
  },
  {
    name: 'Real-time Updates',
    description: 'Get instant notifications and updates across all services.',
    icon: '⚡',
  },
];

export function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">
                AliFrzngn Development
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/login"
                className="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="btn btn-primary btn-md"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Microservices-Based
              <span className="text-primary-600"> Web Application</span>
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
              A production-ready microservices architecture with inventory management,
              customer relationship management, and user authentication.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/register"
                className="btn btn-primary btn-lg"
              >
                Get started
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
              <Link
                href="/login"
                className="btn btn-outline btn-lg"
              >
                Sign in
              </Link>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="bg-gray-50 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900">
                Everything you need to manage your business
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Built with modern technologies and best practices for scalability and reliability.
              </p>
            </div>
            <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {features.map((feature) => (
                <div key={feature.name} className="card">
                  <div className="card-content">
                    <div className="text-4xl mb-4">{feature.icon}</div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {feature.name}
                    </h3>
                    <p className="mt-2 text-gray-600">{feature.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-primary-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight text-white">
                Ready to get started?
              </h2>
              <p className="mt-4 text-lg text-primary-100">
                Join thousands of businesses already using our platform.
              </p>
              <div className="mt-8">
                <Link
                  href="/register"
                  className="btn bg-white text-primary-600 hover:bg-gray-50 btn-lg"
                >
                  Create your account
                  <ArrowRightIcon className="ml-2 h-5 w-5" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <p className="text-gray-500">
              © 2024 AliFrzngn Development. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
