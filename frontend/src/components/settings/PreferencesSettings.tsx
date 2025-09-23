'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { User } from '@/types/user';

interface PreferencesSettingsProps {
  user: User;
}

export function PreferencesSettings({ user }: PreferencesSettingsProps) {
  const [preferences, setPreferences] = useState({
    theme: 'light',
    language: 'en',
    timezone: 'UTC',
    date_format: 'MM/DD/YYYY',
    currency: 'USD',
    items_per_page: '10',
    default_view: 'table',
    email_digest: 'daily',
  });

  const queryClient = useQueryClient();

  const updatePreferencesMutation = useMutation({
    mutationFn: (data: any) => userApi.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user', 'profile'] });
    },
  });

  const handleChange = (field: string, value: string) => {
    setPreferences(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    updatePreferencesMutation.mutate({ preferences });
  };

  const themeOptions = [
    { value: 'light', label: 'Light' },
    { value: 'dark', label: 'Dark' },
    { value: 'auto', label: 'Auto (System)' },
  ];

  const languageOptions = [
    { value: 'en', label: 'English' },
    { value: 'es', label: 'Spanish' },
    { value: 'fr', label: 'French' },
    { value: 'de', label: 'German' },
  ];

  const timezoneOptions = [
    { value: 'UTC', label: 'UTC' },
    { value: 'America/New_York', label: 'Eastern Time' },
    { value: 'America/Chicago', label: 'Central Time' },
    { value: 'America/Denver', label: 'Mountain Time' },
    { value: 'America/Los_Angeles', label: 'Pacific Time' },
    { value: 'Europe/London', label: 'London' },
    { value: 'Europe/Paris', label: 'Paris' },
    { value: 'Asia/Tokyo', label: 'Tokyo' },
  ];

  const dateFormatOptions = [
    { value: 'MM/DD/YYYY', label: 'MM/DD/YYYY' },
    { value: 'DD/MM/YYYY', label: 'DD/MM/YYYY' },
    { value: 'YYYY-MM-DD', label: 'YYYY-MM-DD' },
  ];

  const currencyOptions = [
    { value: 'USD', label: 'US Dollar ($)' },
    { value: 'EUR', label: 'Euro (€)' },
    { value: 'GBP', label: 'British Pound (£)' },
    { value: 'JPY', label: 'Japanese Yen (¥)' },
  ];

  const itemsPerPageOptions = [
    { value: '5', label: '5 items' },
    { value: '10', label: '10 items' },
    { value: '25', label: '25 items' },
    { value: '50', label: '50 items' },
    { value: '100', label: '100 items' },
  ];

  const defaultViewOptions = [
    { value: 'table', label: 'Table View' },
    { value: 'grid', label: 'Grid View' },
    { value: 'list', label: 'List View' },
  ];

  const emailDigestOptions = [
    { value: 'immediate', label: 'Immediate' },
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
    { value: 'never', label: 'Never' },
  ];

  return (
    <div className="space-y-6">
      {/* Appearance */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Appearance
          </h3>
          
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <Select
                label="Theme"
                value={preferences.theme}
                onChange={(e) => handleChange('theme', e.target.value)}
                options={themeOptions}
              />
            </div>
            <div>
              <Select
                label="Language"
                value={preferences.language}
                onChange={(e) => handleChange('language', e.target.value)}
                options={languageOptions}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Date & Time */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Date & Time
          </h3>
          
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <Select
                label="Timezone"
                value={preferences.timezone}
                onChange={(e) => handleChange('timezone', e.target.value)}
                options={timezoneOptions}
              />
            </div>
            <div>
              <Select
                label="Date Format"
                value={preferences.date_format}
                onChange={(e) => handleChange('date_format', e.target.value)}
                options={dateFormatOptions}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Currency & Display */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Currency & Display
          </h3>
          
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <Select
                label="Currency"
                value={preferences.currency}
                onChange={(e) => handleChange('currency', e.target.value)}
                options={currencyOptions}
              />
            </div>
            <div>
              <Select
                label="Items Per Page"
                value={preferences.items_per_page}
                onChange={(e) => handleChange('items_per_page', e.target.value)}
                options={itemsPerPageOptions}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Interface */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Interface
          </h3>
          
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <Select
                label="Default View"
                value={preferences.default_view}
                onChange={(e) => handleChange('default_view', e.target.value)}
                options={defaultViewOptions}
              />
            </div>
            <div>
              <Select
                label="Email Digest"
                value={preferences.email_digest}
                onChange={(e) => handleChange('email_digest', e.target.value)}
                options={emailDigestOptions}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button
          onClick={handleSave}
          disabled={updatePreferencesMutation.isPending}
        >
          {updatePreferencesMutation.isPending ? 'Saving...' : 'Save Preferences'}
        </Button>
      </div>
    </div>
  );
}
