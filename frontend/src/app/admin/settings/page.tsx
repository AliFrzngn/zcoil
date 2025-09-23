'use client';

import { useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';

export default function AdminSettingsPage() {
  const [settings, setSettings] = useState({
    site_name: 'AliFrzngn Development',
    site_description: 'Microservices-based inventory management system',
    admin_email: 'admin@alifrzngn.dev',
    support_email: 'support@alifrzngn.dev',
    max_file_size: '10',
    allowed_file_types: 'jpg,jpeg,png,pdf,doc,docx,txt',
    email_verification_required: true,
    user_registration_enabled: true,
    maintenance_mode: false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (field: string, value: any) => {
    setSettings(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handleSave = () => {
    // This would save settings to the backend
    console.log('Saving settings:', settings);
  };

  const fileTypeOptions = [
    { value: 'jpg,jpeg,png,pdf,doc,docx,txt', label: 'Images & Documents' },
    { value: 'jpg,jpeg,png,gif,webp', label: 'Images Only' },
    { value: 'pdf,doc,docx,txt,rtf', label: 'Documents Only' },
    { value: 'jpg,jpeg,png,pdf,doc,docx,txt,zip,rar', label: 'All Supported' },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">System Settings</h1>
          <p className="mt-1 text-sm text-gray-500">
            Configure system-wide settings and preferences
          </p>
        </div>

        {/* General Settings */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              General Settings
            </h3>
            
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <Input
                  label="Site Name"
                  value={settings.site_name}
                  onChange={(e) => handleChange('site_name', e.target.value)}
                  placeholder="Enter site name"
                />
              </div>
              <div>
                <Input
                  label="Admin Email"
                  type="email"
                  value={settings.admin_email}
                  onChange={(e) => handleChange('admin_email', e.target.value)}
                  placeholder="admin@example.com"
                />
              </div>
            </div>

            <div className="mt-4">
              <Textarea
                label="Site Description"
                value={settings.site_description}
                onChange={(e) => handleChange('site_description', e.target.value)}
                placeholder="Enter site description"
                rows={3}
              />
            </div>

            <div className="mt-4">
              <Input
                label="Support Email"
                type="email"
                value={settings.support_email}
                onChange={(e) => handleChange('support_email', e.target.value)}
                placeholder="support@example.com"
              />
            </div>
          </div>
        </div>

        {/* File Upload Settings */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              File Upload Settings
            </h3>
            
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <Input
                  label="Max File Size (MB)"
                  type="number"
                  value={settings.max_file_size}
                  onChange={(e) => handleChange('max_file_size', e.target.value)}
                  placeholder="10"
                />
              </div>
              <div>
                <Select
                  label="Allowed File Types"
                  value={settings.allowed_file_types}
                  onChange={(e) => handleChange('allowed_file_types', e.target.value)}
                  options={fileTypeOptions}
                />
              </div>
            </div>
          </div>
        </div>

        {/* User Settings */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              User Settings
            </h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-900">Email Verification Required</p>
                  <p className="text-sm text-gray-500">
                    Require users to verify their email before accessing the system
                  </p>
                </div>
                <input
                  type="checkbox"
                  id="email_verification_required"
                  checked={settings.email_verification_required}
                  onChange={(e) => handleChange('email_verification_required', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  aria-label="Email verification required"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-900">User Registration Enabled</p>
                  <p className="text-sm text-gray-500">
                    Allow new users to register accounts
                  </p>
                </div>
                <input
                  type="checkbox"
                  id="user_registration_enabled"
                  checked={settings.user_registration_enabled}
                  onChange={(e) => handleChange('user_registration_enabled', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  aria-label="User registration enabled"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-900">Maintenance Mode</p>
                  <p className="text-sm text-gray-500">
                    Put the system in maintenance mode (admin access only)
                  </p>
                </div>
                <input
                  type="checkbox"
                  id="maintenance_mode"
                  checked={settings.maintenance_mode}
                  onChange={(e) => handleChange('maintenance_mode', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  aria-label="Maintenance mode"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <Button onClick={handleSave}>
            Save Settings
          </Button>
        </div>
      </div>
    </AdminLayout>
  );
}
