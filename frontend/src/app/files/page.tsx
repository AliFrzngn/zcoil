'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fileApi } from '@/lib/api';
import { FileUpload } from '@/types/api';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Modal } from '@/components/ui/Modal';
import { UploadIcon, TrashIcon, EyeIcon, DownloadIcon } from '@heroicons/react/24/outline';

export default function FilesPage() {
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadOptions, setUploadOptions] = useState({
    resource_type: '',
    resource_id: '',
    is_public: false,
  });
  const [filters, setFilters] = useState({
    resource_type: '',
    page: 1,
    size: 10,
  });

  const queryClient = useQueryClient();

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['files', filters],
    queryFn: () => fileApi.getUserFiles(filters),
  });

  const uploadFileMutation = useMutation({
    mutationFn: (file: File) => fileApi.uploadFile(file, uploadOptions),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['files'] });
      setShowUploadModal(false);
      setSelectedFile(null);
      setUploadOptions({ resource_type: '', resource_id: '', is_public: false });
    },
  });

  const deleteFileMutation = useMutation({
    mutationFn: (id: number) => fileApi.deleteFile(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['files'] });
    },
  });

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      uploadFileMutation.mutate(selectedFile);
    }
  };

  const handleDelete = (id: number) => {
    if (confirm('Are you sure you want to delete this file?')) {
      deleteFileMutation.mutate(id);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const files = data?.data || [];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">File Management</h1>
            <p className="mt-1 text-sm text-gray-500">
              Upload and manage your files
            </p>
          </div>
          <Button
            onClick={() => setShowUploadModal(true)}
            className="btn btn-primary btn-md"
          >
            <UploadIcon className="h-5 w-5 mr-2" />
            Upload File
          </Button>
        </div>

        {/* Filters */}
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center space-x-4">
            <div className="flex-1">
              <Select
                label="Resource Type"
                value={filters.resource_type}
                onChange={(e) => setFilters(prev => ({ ...prev, resource_type: e.target.value, page: 1 }))}
                options={[
                  { value: '', label: 'All Types' },
                  { value: 'product', label: 'Product' },
                  { value: 'user', label: 'User' },
                  { value: 'other', label: 'Other' },
                ]}
              />
            </div>
          </div>
        </div>

        {/* Files List */}
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-16 bg-gray-200 rounded"></div>
              </div>
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <div className="text-red-600 text-2xl mb-4">⚠️</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Failed to load files</h3>
            <p className="text-gray-500 mb-4">There was an error loading your files.</p>
            <Button onClick={() => refetch()} className="btn btn-outline">
              Try Again
            </Button>
          </div>
        ) : files.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-4xl mb-4">📁</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No files found</h3>
            <p className="text-gray-500">Upload your first file to get started.</p>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      File
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Size
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Resource
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Uploaded
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {files.map((file: FileUpload) => (
                    <tr key={file.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-10 w-10">
                            <div className="h-10 w-10 rounded-md bg-gray-200 flex items-center justify-center">
                              <span className="text-sm font-medium text-gray-500">
                                {file.original_filename.charAt(0).toUpperCase()}
                              </span>
                            </div>
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-medium text-gray-900">
                              {file.original_filename}
                            </div>
                            <div className="text-sm text-gray-500">
                              {file.filename}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {formatFileSize(file.file_size)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {file.content_type}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {file.resource_type || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(file.created_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex items-center justify-end space-x-2">
                          <Button
                            onClick={() => window.open(`/api/v1/files/${file.id}/download`, '_blank')}
                            variant="outline"
                            size="sm"
                          >
                            <DownloadIcon className="h-4 w-4" />
                          </Button>
                          <Button
                            onClick={() => handleDelete(file.id)}
                            variant="outline"
                            size="sm"
                            className="text-red-600 hover:text-red-700"
                          >
                            <TrashIcon className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Upload Modal */}
        {showUploadModal && (
          <Modal onClose={() => setShowUploadModal(false)} title="Upload File" size="lg">
            <div className="space-y-4">
              {/* File Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Select File
                </label>
                <input
                  type="file"
                  id="file_upload"
                  onChange={handleFileSelect}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  aria-label="Select file to upload"
                />
                {selectedFile && (
                  <p className="mt-1 text-sm text-gray-500">
                    Selected: {selectedFile.name} ({formatFileSize(selectedFile.size)})
                  </p>
                )}
              </div>

              {/* Upload Options */}
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <Input
                    label="Resource Type"
                    value={uploadOptions.resource_type}
                    onChange={(e) => setUploadOptions(prev => ({ ...prev, resource_type: e.target.value }))}
                    placeholder="e.g., product, user"
                  />
                </div>
                <div>
                  <Input
                    label="Resource ID"
                    value={uploadOptions.resource_id}
                    onChange={(e) => setUploadOptions(prev => ({ ...prev, resource_id: e.target.value }))}
                    placeholder="e.g., 123"
                  />
                </div>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="is_public"
                  checked={uploadOptions.is_public}
                  onChange={(e) => setUploadOptions(prev => ({ ...prev, is_public: e.target.checked }))}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="is_public" className="ml-2 block text-sm text-gray-900">
                  Make file public
                </label>
              </div>

              {/* Actions */}
              <div className="flex justify-end space-x-3 pt-4">
                <Button
                  variant="outline"
                  onClick={() => setShowUploadModal(false)}
                  disabled={uploadFileMutation.isPending}
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleUpload}
                  disabled={!selectedFile || uploadFileMutation.isPending}
                >
                  {uploadFileMutation.isPending ? 'Uploading...' : 'Upload File'}
                </Button>
              </div>
            </div>
          </Modal>
        )}
      </div>
    </DashboardLayout>
  );
}
