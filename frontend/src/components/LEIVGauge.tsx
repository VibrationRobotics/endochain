/**
 * LEI-V Gauge Component
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 * 
 * Visual gauge for displaying LEI-V values with stage indicators.
 */

import { useMemo } from 'react';
import clsx from 'clsx';

interface LEIVGaugeProps {
  value: number;
  showThresholds?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const THRESHOLDS = {
  healthy: 0.018,
  advanced: 0.08,
  max: 0.15,
};

export function LEIVGauge({ value, showThresholds = true, size = 'md' }: LEIVGaugeProps) {
  const stage = useMemo(() => {
    if (value < THRESHOLDS.healthy) return 'healthy';
    if (value < THRESHOLDS.advanced) return 'stage_0';
    return 'advanced';
  }, [value]);

  const percentage = useMemo(() => {
    return Math.min(100, (value / THRESHOLDS.max) * 100);
  }, [value]);

  const stageColors = {
    healthy: 'text-green-500',
    stage_0: 'text-amber-500',
    advanced: 'text-red-500',
  };

  const stageLabels = {
    healthy: 'Healthy',
    stage_0: 'Stage-0 (Early)',
    advanced: 'Advanced',
  };

  const sizeClasses = {
    sm: 'w-32 h-32',
    md: 'w-48 h-48',
    lg: 'w-64 h-64',
  };

  // SVG arc calculation
  const radius = 70;
  const circumference = radius * Math.PI;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <div className={clsx('relative', sizeClasses[size])}>
        <svg viewBox="0 0 200 120" className="w-full h-full">
          {/* Background arc */}
          <path
            d="M 20 100 A 70 70 0 0 1 180 100"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="12"
            strokeLinecap="round"
          />
          
          {/* Threshold markers */}
          {showThresholds && (
            <>
              {/* Stage-0 threshold marker */}
              <circle
                cx={20 + (THRESHOLDS.healthy / THRESHOLDS.max) * 160}
                cy={100 - Math.sin((THRESHOLDS.healthy / THRESHOLDS.max) * Math.PI) * 70}
                r="4"
                fill="#f59e0b"
              />
              {/* Advanced threshold marker */}
              <circle
                cx={20 + (THRESHOLDS.advanced / THRESHOLDS.max) * 160}
                cy={100 - Math.sin((THRESHOLDS.advanced / THRESHOLDS.max) * Math.PI) * 70}
                r="4"
                fill="#ef4444"
              />
            </>
          )}
          
          {/* Value arc */}
          <path
            d="M 20 100 A 70 70 0 0 1 180 100"
            fill="none"
            stroke={
              stage === 'healthy' ? '#22c55e' : 
              stage === 'stage_0' ? '#f59e0b' : '#ef4444'
            }
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-500"
          />
          
          {/* Center text */}
          <text x="100" y="85" textAnchor="middle" className="text-3xl font-bold fill-gray-800">
            {value.toFixed(4)}
          </text>
          <text x="100" y="105" textAnchor="middle" className="text-sm fill-gray-500">
            LEI-V
          </text>
        </svg>
      </div>

      {/* Stage indicator */}
      <div className={clsx('mt-2 px-4 py-1 rounded-full text-sm font-medium', {
        'bg-green-100 text-green-700': stage === 'healthy',
        'bg-amber-100 text-amber-700': stage === 'stage_0',
        'bg-red-100 text-red-700': stage === 'advanced',
      })}>
        {stageLabels[stage]}
      </div>

      {/* Thresholds legend */}
      {showThresholds && (
        <div className="mt-4 grid grid-cols-3 gap-2 text-xs text-gray-500">
          <div className="flex items-center">
            <span className="w-2 h-2 bg-green-500 rounded-full mr-1" />
            {'< 0.018'}
          </div>
          <div className="flex items-center">
            <span className="w-2 h-2 bg-amber-500 rounded-full mr-1" />
            {'0.018 - 0.08'}
          </div>
          <div className="flex items-center">
            <span className="w-2 h-2 bg-red-500 rounded-full mr-1" />
            {'> 0.08'}
          </div>
        </div>
      )}

      {/* Citation */}
      <p className="mt-2 text-xs text-gray-400">
        Viduya Family Legacy Glyph © 2025
      </p>
    </div>
  );
}

