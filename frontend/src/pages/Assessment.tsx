/**
 * Assessment Page - Create and View LEI-V Assessments
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Loader2, Send, Download, FileJson } from 'lucide-react';
import { LEIVGauge } from '../components/LEIVGauge';
import { GlyphVisualization } from '../components/GlyphVisualization';
import { assessmentApi, AssessmentRequest, Assessment as AssessmentType } from '../lib/api';

const assessmentSchema = z.object({
  patient_id: z.string().min(1, 'Patient ID is required'),
  cycle_day: z.number().min(1).max(35).optional(),
  v_caw_hour: z.number().min(0).max(96).optional(),
  clinical_notes: z.string().optional(),
  request_ai_fusion: z.boolean().default(true),
  // EVG readings would be from hardware in production
});

type AssessmentFormData = z.infer<typeof assessmentSchema>;

export function Assessment() {
  const { id } = useParams<{ id: string }>();
  const [result, setResult] = useState<AssessmentType | null>(null);

  const { data: existingAssessment, isLoading: loadingExisting } = useQuery({
    queryKey: ['assessment', id],
    queryFn: () => assessmentApi.get(id!),
    enabled: !!id,
  });

  const mutation = useMutation({
    mutationFn: assessmentApi.create,
    onSuccess: (data) => setResult(data),
  });

  const { register, handleSubmit, formState: { errors } } = useForm<AssessmentFormData>({
    resolver: zodResolver(assessmentSchema),
    defaultValues: {
      request_ai_fusion: true,
    },
  });

  // Simulated EVG readings for demo
  const simulatedEVGReadings = Array.from({ length: 6 }, (_, i) => ({
    electrode_index: i + 1,
    radial_distance: 0.43 + (Math.random() - 0.5) * 0.02,
    impedance: 1150 + Math.random() * 100,
    timestamp: new Date().toISOString(),
  }));

  const onSubmit = (data: AssessmentFormData) => {
    const request: AssessmentRequest = {
      ...data,
      evg_readings: simulatedEVGReadings,
    };
    mutation.mutate(request);
  };

  const displayAssessment = result || existingAssessment;

  if (id && loadingExisting) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">
        {id ? 'Assessment Details' : 'New LEI-V Assessment'}
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        {!id && !result && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">Patient Information</h3>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Patient ID
                </label>
                <input
                  {...register('patient_id')}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder="ENDO-2025-XXXX"
                />
                {errors.patient_id && (
                  <p className="text-red-500 text-sm">{errors.patient_id.message}</p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Cycle Day
                  </label>
                  <input
                    type="number"
                    {...register('cycle_day', { valueAsNumber: true })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    V-CAW Hour
                  </label>
                  <input
                    type="number"
                    {...register('v_caw_hour', { valueAsNumber: true })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Clinical Notes
                </label>
                <textarea
                  {...register('clinical_notes')}
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                />
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  {...register('request_ai_fusion')}
                  className="h-4 w-4 text-indigo-600 rounded"
                />
                <label className="ml-2 text-sm text-gray-700">
                  Request AI Platform Fusion Analysis
                </label>
              </div>

              <button
                type="submit"
                disabled={mutation.isPending}
                className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
              >
                {mutation.isPending ? (
                  <Loader2 className="h-5 w-5 animate-spin mr-2" />
                ) : (
                  <Send className="h-5 w-5 mr-2" />
                )}
                Compute LEI-V
              </button>
            </form>
          </div>
        )}

        {/* Glyph Visualization */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Regenerative Spark Lattice</h3>
          <GlyphVisualization
            electrodeValues={simulatedEVGReadings.map((r) => r.radial_distance - 0.43 + 0.018)}
          />
        </div>

        {/* Results */}
        {displayAssessment && (
          <>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">LEI-V Result</h3>
              <LEIVGauge value={displayAssessment.lei_v} />
              <div className="mt-4 space-y-2 text-sm">
                <p><strong>Stage:</strong> {displayAssessment.stage}</p>
                <p><strong>Confidence:</strong> {displayAssessment.confidence_percent.toFixed(1)}%</p>
                <p><strong>Symbolic:</strong> <code>{displayAssessment.lei_v_symbolic}</code></p>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-4">Export Options</h3>
              <div className="space-y-3">
                <button className="w-full flex items-center justify-center py-2 px-4 border border-gray-300 rounded-md text-sm hover:bg-gray-50">
                  <Download className="h-4 w-4 mr-2" />
                  Download PDF Report
                </button>
                <button className="w-full flex items-center justify-center py-2 px-4 border border-gray-300 rounded-md text-sm hover:bg-gray-50">
                  <FileJson className="h-4 w-4 mr-2" />
                  Export FHIR Bundle
                </button>
              </div>
              <p className="mt-4 text-xs text-gray-400 text-center">
                Audit Hash: {displayAssessment.audit_hash?.slice(0, 16)}...
              </p>
            </div>
          </>
        )}
      </div>

      <p className="text-center text-xs text-gray-400">
        Citation: Viduya Family Legacy Glyph © 2025
      </p>
    </div>
  );
}

