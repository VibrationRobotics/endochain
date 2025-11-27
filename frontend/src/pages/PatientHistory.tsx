/**
 * Patient History Page - Longitudinal LEI-V Tracking
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, ReferenceLine 
} from 'recharts';
import { Calendar, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { patientApi } from '../lib/api';

export function PatientHistory() {
  const { id } = useParams<{ id: string }>();

  // Mock data for demonstration
  const historyData = [
    { date: '2025-10-01', lei_v: 0.021, cycle_day: 14, stage: 'stage_0' },
    { date: '2025-10-15', lei_v: 0.019, cycle_day: 14, stage: 'stage_0' },
    { date: '2025-10-29', lei_v: 0.018, cycle_day: 14, stage: 'stage_0' },
    { date: '2025-11-12', lei_v: 0.016, cycle_day: 14, stage: 'healthy' },
    { date: '2025-11-26', lei_v: 0.014, cycle_day: 14, stage: 'healthy' },
  ];

  const patient = {
    patient_id: id || 'ENDO-2025-A3F2',
    date_of_birth: '1990-05-15',
    cycle_length_days: 28,
    total_assessments: 5,
    mean_lei_v: 0.0176,
    trend: 'improving' as const,
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving':
        return <TrendingDown className="h-5 w-5 text-green-500" />;
      case 'worsening':
        return <TrendingUp className="h-5 w-5 text-red-500" />;
      default:
        return <Minus className="h-5 w-5 text-gray-500" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Patient History</h2>
          <p className="text-gray-500">{patient.patient_id}</p>
        </div>
        <div className="flex items-center space-x-2 px-3 py-1 bg-green-100 text-green-700 rounded-full">
          {getTrendIcon(patient.trend)}
          <span className="text-sm font-medium capitalize">{patient.trend}</span>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-sm text-gray-500">Total Assessments</p>
          <p className="text-2xl font-bold">{patient.total_assessments}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-sm text-gray-500">Mean LEI-V</p>
          <p className="text-2xl font-bold">{patient.mean_lei_v.toFixed(4)}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-sm text-gray-500">Cycle Length</p>
          <p className="text-2xl font-bold">{patient.cycle_length_days} days</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-sm text-gray-500">Latest Stage</p>
          <p className="text-2xl font-bold text-green-600">Healthy</p>
        </div>
      </div>

      {/* LEI-V Trend Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">LEI-V Longitudinal Trend</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={historyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              domain={[0, 0.04]}
              tick={{ fontSize: 12 }}
              tickFormatter={(v) => v.toFixed(3)}
            />
            <Tooltip
              formatter={(value: number) => [value.toFixed(4), 'LEI-V']}
              labelFormatter={(label) => `Date: ${label}`}
            />
            {/* Stage-0 threshold */}
            <ReferenceLine 
              y={0.018} 
              stroke="#f59e0b" 
              strokeDasharray="5 5"
              label={{ value: 'Stage-0 Threshold', position: 'right', fontSize: 10 }}
            />
            {/* Advanced threshold */}
            <ReferenceLine 
              y={0.08} 
              stroke="#ef4444" 
              strokeDasharray="5 5"
            />
            <Line
              type="monotone"
              dataKey="lei_v"
              stroke="#6366f1"
              strokeWidth={2}
              dot={{ fill: '#6366f1', strokeWidth: 2 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Assessment History Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-4 py-3 border-b bg-gray-50">
          <h3 className="font-semibold">Assessment History</h3>
        </div>
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Date</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">LEI-V</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Stage</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Cycle Day</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {historyData.map((row, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm flex items-center">
                  <Calendar className="h-4 w-4 mr-2 text-gray-400" />
                  {row.date}
                </td>
                <td className="px-4 py-3 text-sm font-mono">{row.lei_v.toFixed(4)}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    row.stage === 'healthy' 
                      ? 'bg-green-100 text-green-700'
                      : 'bg-amber-100 text-amber-700'
                  }`}>
                    {row.stage}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm">{row.cycle_day}</td>
                <td className="px-4 py-3">
                  <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-center text-xs text-gray-400">
        Citation: Viduya Family Legacy Glyph © 2025
      </p>
    </div>
  );
}

