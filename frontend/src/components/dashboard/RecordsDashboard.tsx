'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { recordsApi } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';

interface Record {
  id: number;
  name: string;
  description?: string;
  sku: string;
  price: number;
  quantity: number;
  category?: string;
  brand?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

interface RecordsDashboardProps {
  className?: string;
}

export function RecordsDashboard({ className }: RecordsDashboardProps) {
  const [searchId, setSearchId] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'done' | 'not_done'>('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(10);

  // Fetch records with filters
  const { data: recordsData, isLoading, error, refetch } = useQuery({
    queryKey: ['records', searchId, statusFilter, currentPage, pageSize],
    queryFn: () => recordsApi.getRecords({
      id: searchId || undefined,
      status: statusFilter === 'all' ? undefined : statusFilter,
      page: currentPage,
      size: pageSize,
    }),
    enabled: true,
  });

  const records = recordsData?.data?.items || [];
  const totalRecords = recordsData?.data?.total || 0;
  const totalPages = Math.ceil(totalRecords / pageSize);

  // Reset page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchId, statusFilter]);

  const handleSearch = () => {
    refetch();
  };

  const handleClearFilters = () => {
    setSearchId('');
    setStatusFilter('all');
    setCurrentPage(1);
  };

  const getStatusBadge = (record: Record) => {
    // For this demo, we'll consider a record "done" if it's active and has quantity > 0
    const isDone = record.is_active && record.quantity > 0;
    return (
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          isDone
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        }`}
      >
        {isDone ? 'Done' : 'Not Done'}
      </span>
    );
  };

  if (error) {
    return (
      <div className="p-6">
        <div className="text-center">
          <p className="text-red-600">Error loading records: {error.message}</p>
          <Button onClick={() => refetch()} className="mt-4">
            Retry
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Records Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          View and filter your records by ID and processing status
        </p>
      </div>

      {/* Filters */}
      <Card>
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Filters</h3>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label htmlFor="search-id" className="block text-sm font-medium text-gray-700">
                Search by Record ID
              </label>
              <Input
                id="search-id"
                type="text"
                placeholder="Enter record ID"
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
                className="mt-1"
              />
            </div>
            <div>
              <label htmlFor="status-filter" className="block text-sm font-medium text-gray-700">
                Filter by Status
              </label>
              <Select
                id="status-filter"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as 'all' | 'done' | 'not_done')}
                className="mt-1"
              >
                <option value="all">All Records</option>
                <option value="done">Done</option>
                <option value="not_done">Not Done</option>
              </Select>
            </div>
            <div className="flex items-end space-x-2">
              <Button onClick={handleSearch} className="btn-primary">
                Search
              </Button>
              <Button onClick={handleClearFilters} variant="outline">
                Clear
              </Button>
            </div>
          </div>
        </div>
      </Card>

      {/* Results Summary */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-700">
          Showing {records.length} of {totalRecords} records
        </p>
        {isLoading && (
          <div className="flex items-center text-sm text-gray-500">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600 mr-2"></div>
            Loading...
          </div>
        )}
      </div>

      {/* Records Table */}
      <Card>
        <div className="card-content p-0">
          {records.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No records found matching your criteria</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      SKU
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Price
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Quantity
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {records.map((record: Record) => (
                    <tr key={record.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {record.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {record.sku}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${record.price.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {record.quantity}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {getStatusBadge(record)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(record.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </Card>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              variant="outline"
            >
              Previous
            </Button>
            <span className="text-sm text-gray-700">
              Page {currentPage} of {totalPages}
            </span>
            <Button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              variant="outline"
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}