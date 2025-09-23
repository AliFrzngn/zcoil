import { clsx } from 'clsx';

interface StatsCardProps {
  title: string;
  value: number | string;
  icon: string;
  description: string;
  alert?: boolean;
}

export function StatsCard({ title, value, icon, description, alert = false }: StatsCardProps) {
  return (
    <div className={clsx(
      'card',
      alert && 'border-red-200 bg-red-50'
    )}>
      <div className="card-content">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <span className="text-2xl">{icon}</span>
          </div>
          <div className="ml-4 flex-1">
            <p className="text-sm font-medium text-gray-500">{title}</p>
            <p className={clsx(
              'text-2xl font-semibold',
              alert ? 'text-red-600' : 'text-gray-900'
            )}>
              {value}
            </p>
            <p className="text-xs text-gray-500">{description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}