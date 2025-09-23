'use client';

import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { XMarkIcon, FunnelIcon } from '@heroicons/react/24/outline';

interface UserFiltersProps {
  filters: any;
  onFiltersChange: (filters: any) => void;
}

const roleOptions = [
  { value: '', label: 'All Roles' },
  { value: 'admin', label: 'Admin' },
  { value: 'manager', label: 'Manager' },
  { value: 'customer', label: 'Customer' },
];

const statusOptions = [
  { value: '', label: 'All Status' },
  { value: 'true', label: 'Verified' },
  { value: 'false', label: 'Unverified' },
];

const activeOptions = [
  { value: '', label: 'All Users' },
  { value: 'true', label: 'Active' },
  { value: 'false', label: 'Inactive' },
];

export function UserFilters({ filters, onFiltersChange }: UserFiltersProps) {
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleFilterChange = (key: string, value: any) => {
    onFiltersChange({ [key]: value });
  };

  const clearFilters = () => {
    onFiltersChange({
      username: '',
      email: '',
      role: '',
      is_verified: undefined,
      is_active: undefined,
    });
  };

  const hasActiveFilters = 
    filters.username || 
    filters.email || 
    filters.role || 
    filters.is_verified !== undefined ||
    filters.is_active !== undefined;

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Filters</h3>
        <div className="flex items-center space-x-2">
          {hasActiveFilters && (
            <Button
              onClick={clearFilters}
              variant="outline"
              size="sm"
            >
              <XMarkIcon className="h-4 w-4 mr-1" />
              Clear
            </Button>
          )}
          <Button
            onClick={() => setShowAdvanced(!showAdvanced)}
            variant="outline"
            size="sm"
          >
            <FunnelIcon className="h-4 w-4 mr-1" />
            {showAdvanced ? 'Hide' : 'Show'} Advanced
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {/* Search Username */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Username
          </label>
          <Input
            type="text"
            placeholder="Search by username..."
            value={filters.username || ''}
            onChange={(e) => handleFilterChange('username', e.target.value)}
          />
        </div>

        {/* Search Email */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <Input
            type="text"
            placeholder="Search by email..."
            value={filters.email || ''}
            onChange={(e) => handleFilterChange('email', e.target.value)}
          />
        </div>

        {/* Role */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Role
          </label>
          <Select
            value={filters.role || ''}
            onChange={(e) => handleFilterChange('role', e.target.value)}
            options={roleOptions}
          />
        </div>

        {/* Verification Status */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Verification
          </label>
          <Select
            value={filters.is_verified?.toString() || ''}
            onChange={(e) => handleFilterChange('is_verified', e.target.value === '' ? undefined : e.target.value === 'true')}
            options={statusOptions}
          />
        </div>
      </div>

      {/* Advanced Filters */}
      {showAdvanced && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {/* Active Status */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Account Status
              </label>
              <Select
                value={filters.is_active?.toString() || ''}
                onChange={(e) => handleFilterChange('is_active', e.target.value === '' ? undefined : e.target.value === 'true')}
                options={activeOptions}
              />
            </div>

            {/* Date Range */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Created After
              </label>
              <Input
                type="date"
                value={filters.created_after || ''}
                onChange={(e) => handleFilterChange('created_after', e.target.value)}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}