/**
 * ENDOCHAIN Dashboard Page
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

import { useQuery } from '@tanstack/react-query';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  AreaChart, Area
} from 'recharts';
import { Activity, Users, FileCheck, AlertTriangle } from 'lucide-react';
import { LEIVGauge } from '../components/LEIVGauge';
import { api } from '../lib/api';

export function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => api.get('/api/v1/stats'),
  });

  // Mock data for demonstration
  const recentAssessments = [
    { date: '2025-11-20', lei_v: 0.015, stage: 'healthy' },
    { date: '2025-11-21', lei_v: 0.019, stage: 'stage_0' },
    { date: '2025-11-22', lei_v: 0.022, stage: 'stage_0' },
    { date: '2025-11-23', lei_v: 0.018, stage: 'stage_0' },
    { date: '2025-11-24', lei_v: 0.016, stage: 'healthy' },
    { date: '2025-11-25', lei_v: 0.014, stage: 'healthy' },
    { date: '2025-11-26', lei_v: 0.012, stage: 'healthy' },
  ];

  const statCards = [
    { name: 'Active V-CAW Sessions', value: '3', icon: Activity, color: 'bg-blue-500' },
    { name: 'Patients Enrolled', value: '47', icon: Users, color: 'bg-green-500' },
    { name: 'Assessments Today', value: '12', icon: FileCheck, color: 'bg-purple-500' },
    { name: 'Pending Review', value: '5', icon: AlertTriangle, color: 'bg-amber-500' },
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          LEI-V Diagnostic Dashboard
        </h2>
        <p className="text-gray-500">
          Real-time monitoring powered by Viduya Family Legacy Glyph © 2025
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat) => (
          <div
            key={stat.name}
            className="bg-white rounded-lg shadow p-6 flex items-center space-x-4"
          >
            <div className={`${stat.color} p-3 rounded-lg`}>
              <stat.icon className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-sm text-gray-500">{stat.name}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEI-V Trend Chart */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">LEI-V Population Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={recentAssessments}>
              <defs>
                <linearGradient id="leivGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis domain={[0, 0.05]} />
              <Tooltip 
                formatter={(value: number) => [value.toFixed(4), 'LEI-V']}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Area
                type="monotone"
                dataKey="lei_v"
                stroke="#6366f1"
                fillOpacity={1}
                fill="url(#leivGradient)"
              />
              {/* Stage-0 threshold line */}
              <Line
                type="monotone"
                dataKey={() => 0.018}
                stroke="#ef4444"
                strokeDasharray="5 5"
                dot={false}
              />
            </AreaChart>
          </ResponsiveContainer>
          <div className="flex justify-center space-x-6 mt-4 text-sm">
            <span className="flex items-center">
              <span className="w-3 h-3 bg-indigo-500 rounded-full mr-2" />
              LEI-V Value
            </span>
            <span className="flex items-center">
              <span className="w-3 h-0.5 bg-red-500 mr-2" style={{ borderTop: '2px dashed' }} />
              Stage-0 Threshold (0.018)
            </span>
          </div>
        </div>

        {/* Current LEI-V Gauge */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Latest Assessment</h3>
          <LEIVGauge value={0.014} />
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-500">Patient: ENDO-2025-A3F2</p>
            <p className="text-sm text-gray-500">V-CAW Hour: 72/96</p>
          </div>
        </div>
      </div>

      {/* Citation Footer */}
      <div className="text-center text-xs text-gray-400 mt-8">
        All computations use exact symbolic mathematics.
        Citation: Viduya Family Legacy Glyph © 2025
      </div>
    </div>
  );
}

