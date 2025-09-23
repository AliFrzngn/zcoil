'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { notificationApi } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { User } from '@/types/user';

interface NotificationSettingsProps {
  user: User;
}

export function NotificationSettings({ user }: NotificationSettingsProps) {
  const [emailSettings, setEmailSettings] = useState({
    product_updates: true,
    low_stock_alerts: true,
    system_notifications: true,
    marketing_emails: false,
  });

  const [pushSettings, setPushSettings] = useState({
    product_updates: true,
    low_stock_alerts: true,
    system_notifications: true,
  });

  const [frequency, setFrequency] = useState('immediate');

  const queryClient = useQueryClient();

  const updateNotificationSettingsMutation = useMutation({
    mutationFn: (data: any) => {
      // This would be implemented when notification API is ready
      return Promise.resolve();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user', 'profile'] });
    },
  });

  const handleEmailSettingChange = (setting: string, value: boolean) => {
    setEmailSettings(prev => ({ ...prev, [setting]: value }));
  };

  const handlePushSettingChange = (setting: string, value: boolean) => {
    setPushSettings(prev => ({ ...prev, [setting]: value }));
  };

  const handleSave = () => {
    updateNotificationSettingsMutation.mutate({
      email: emailSettings,
      push: pushSettings,
      frequency,
    });
  };

  const frequencyOptions = [
    { value: 'immediate', label: 'Immediate' },
    { value: 'daily', label: 'Daily Digest' },
    { value: 'weekly', label: 'Weekly Summary' },
    { value: 'never', label: 'Never' },
  ];

  return (
    <div className="space-y-6">
      {/* Email Notifications */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Email Notifications
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Product Updates</p>
                <p className="text-sm text-gray-500">
                  Get notified about new products and inventory changes
                </p>
              </div>
              <input
                type="checkbox"
                checked={emailSettings.product_updates}
                onChange={(e) => handleEmailSettingChange('product_updates', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Low Stock Alerts</p>
                <p className="text-sm text-gray-500">
                  Receive alerts when inventory is running low
                </p>
              </div>
              <input
                type="checkbox"
                checked={emailSettings.low_stock_alerts}
                onChange={(e) => handleEmailSettingChange('low_stock_alerts', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">System Notifications</p>
                <p className="text-sm text-gray-500">
                  Important system updates and maintenance notifications
                </p>
              </div>
              <input
                type="checkbox"
                checked={emailSettings.system_notifications}
                onChange={(e) => handleEmailSettingChange('system_notifications', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Marketing Emails</p>
                <p className="text-sm text-gray-500">
                  Promotional content and feature announcements
                </p>
              </div>
              <input
                type="checkbox"
                checked={emailSettings.marketing_emails}
                onChange={(e) => handleEmailSettingChange('marketing_emails', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Push Notifications */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Push Notifications
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Product Updates</p>
                <p className="text-sm text-gray-500">
                  Real-time notifications for product changes
                </p>
              </div>
              <input
                type="checkbox"
                checked={pushSettings.product_updates}
                onChange={(e) => handlePushSettingChange('product_updates', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">Low Stock Alerts</p>
                <p className="text-sm text-gray-500">
                  Immediate alerts for low inventory
                </p>
              </div>
              <input
                type="checkbox"
                checked={pushSettings.low_stock_alerts}
                onChange={(e) => handlePushSettingChange('low_stock_alerts', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-900">System Notifications</p>
                <p className="text-sm text-gray-500">
                  Critical system updates and alerts
                </p>
              </div>
              <input
                type="checkbox"
                checked={pushSettings.system_notifications}
                onChange={(e) => handlePushSettingChange('system_notifications', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Notification Frequency */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Notification Frequency
          </h3>
          
          <div>
            <Select
              label="Email Frequency"
              value={frequency}
              onChange={(e) => setFrequency(e.target.value)}
              options={frequencyOptions}
            />
            <p className="mt-1 text-sm text-gray-500">
              Choose how often you want to receive email notifications
            </p>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button
          onClick={handleSave}
          disabled={updateNotificationSettingsMutation.isPending}
        >
          {updateNotificationSettingsMutation.isPending ? 'Saving...' : 'Save Settings'}
        </Button>
      </div>
    </div>
  );
}
