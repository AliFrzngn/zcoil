import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RecordsDashboard } from '@/components/dashboard/RecordsDashboard';
import { recordsApi } from '@/lib/api';

// Mock dependencies
jest.mock('@/lib/api', () => ({
  recordsApi: {
    getRecords: jest.fn(),
  },
}));

const mockRecordsApi = recordsApi as jest.Mocked<typeof recordsApi>;

// Test wrapper with QueryClient
const TestWrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

const mockRecords = [
  {
    id: 1,
    name: 'Test Product 1',
    sku: 'SKU001',
    price: 29.99,
    quantity: 10,
    is_active: true,
    created_at: '2023-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: 'Test Product 2',
    sku: 'SKU002',
    price: 49.99,
    quantity: 0,
    is_active: false,
    created_at: '2023-01-02T00:00:00Z',
  },
];

describe('RecordsDashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders dashboard with filters and table', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: mockRecords,
        total: 2,
        page: 1,
        size: 10,
        pages: 1,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    expect(screen.getByText('Records Dashboard')).toBeInTheDocument();
    expect(screen.getByLabelText(/search by record id/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/filter by status/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /clear/i })).toBeInTheDocument();
  });

  it('displays records in table format', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: mockRecords,
        total: 2,
        page: 1,
        size: 10,
        pages: 1,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
      expect(screen.getByText('Test Product 2')).toBeInTheDocument();
      expect(screen.getByText('SKU001')).toBeInTheDocument();
      expect(screen.getByText('SKU002')).toBeInTheDocument();
    });
  });

  it('shows correct status badges', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: mockRecords,
        total: 2,
        page: 1,
        size: 10,
        pages: 1,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Done')).toBeInTheDocument();
      expect(screen.getByText('Not Done')).toBeInTheDocument();
    });
  });

  it('filters records by ID when search is performed', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: [mockRecords[0]],
        total: 1,
        page: 1,
        size: 10,
        pages: 1,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    const searchInput = screen.getByLabelText(/search by record id/i);
    const searchButton = screen.getByRole('button', { name: /search/i });

    fireEvent.change(searchInput, { target: { value: '1' } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(mockRecordsApi.getRecords).toHaveBeenCalledWith({
        id: '1',
        status: undefined,
        page: 1,
        size: 10,
      });
    });
  });

  it('filters records by status', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: [mockRecords[0]],
        total: 1,
        page: 1,
        size: 10,
        pages: 1,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    const statusSelect = screen.getByLabelText(/filter by status/i);
    const searchButton = screen.getByRole('button', { name: /search/i });

    fireEvent.change(statusSelect, { target: { value: 'done' } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(mockRecordsApi.getRecords).toHaveBeenCalledWith({
        id: undefined,
        status: 'done',
        page: 1,
        size: 10,
      });
    });
  });

  it('clears filters when clear button is clicked', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: mockRecords,
        total: 2,
        page: 1,
        size: 10,
        pages: 1,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    const searchInput = screen.getByLabelText(/search by record id/i);
    const statusSelect = screen.getByLabelText(/filter by status/i);
    const clearButton = screen.getByRole('button', { name: /clear/i });

    fireEvent.change(searchInput, { target: { value: '1' } });
    fireEvent.change(statusSelect, { target: { value: 'done' } });
    fireEvent.click(clearButton);

    expect(searchInput).toHaveValue('');
    expect(statusSelect).toHaveValue('all');
  });

  it('shows loading state', () => {
    mockRecordsApi.getRecords.mockImplementationOnce(
      () => new Promise(resolve => setTimeout(resolve, 100))
    );

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('shows error state when API fails', async () => {
    const mockError = new Error('API Error');
    mockRecordsApi.getRecords.mockRejectedValueOnce(mockError);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText(/error loading records/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
    });
  });

  it('shows no records message when no data', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: [],
        total: 0,
        page: 1,
        size: 10,
        pages: 0,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText(/no records found matching your criteria/i)).toBeInTheDocument();
    });
  });

  it('handles pagination correctly', async () => {
    mockRecordsApi.getRecords.mockResolvedValueOnce({
      data: {
        items: mockRecords,
        total: 25,
        page: 1,
        size: 10,
        pages: 3,
      },
    } as any);

    render(
      <TestWrapper>
        <RecordsDashboard />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText(/page 1 of 3/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /next/i })).toBeInTheDocument();
    });
  });
});