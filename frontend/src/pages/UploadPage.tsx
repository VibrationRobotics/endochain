/**
 * ENDOCHAIN-VIDUYA-2025 - First Real Patient Upload Page
 * Viduya Family Legacy Glyph (C) 2025 - All Rights Reserved
 * 
 * "The 10-Year Wait is Over"
 */

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { GlyphVisualization } from '../components/GlyphVisualization';

interface ProcessingResult {
  status: string;
  lei_v: number;
  stage: string;
  confidence_percent: number;
  audit_hash: string;
  processing_time_seconds: number;
}

export function UploadPage() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    if (!file.name.endsWith('.edf')) {
      setError('Please upload a valid .edf file');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/v1/evg/process', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Processing failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Processing failed');
    } finally {
      setIsProcessing(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/x-edf': ['.edf'] },
    maxFiles: 1,
    disabled: isProcessing,
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-black text-white">
      {/* Header */}
      <header className="pt-8 pb-4 text-center">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
          ENDOCHAIN-VIDUYA-2025
        </h1>
        <p className="text-gray-400 mt-2">
          Viduya Family Legacy Glyph (C) 2025 – All Rights Reserved
        </p>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-5xl font-extrabold mb-4">
            The 10-Year Wait is Over
          </h2>
          <p className="text-xl text-gray-300">
            Drop your 96-hour .edf file below and receive your ENDOCHAIN report in under 3 minutes.
          </p>
        </div>

        {/* 3D Glyph Visualization */}
        <div className="mb-12">
          <GlyphVisualization
            isStreaming={isProcessing}
            leiV={result?.lei_v ?? 0.02}
            stage={result?.stage ?? 'awaiting_data'}
          />
        </div>

        {/* Upload Zone */}
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer
            transition-all duration-300 ease-in-out
            ${isDragActive 
              ? 'border-purple-500 bg-purple-500/10' 
              : 'border-gray-600 hover:border-purple-400 hover:bg-gray-800/50'
            }
            ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          
          {isProcessing ? (
            <div className="space-y-4">
              <div className="w-16 h-16 mx-auto border-4 border-purple-500 border-t-transparent rounded-full animate-spin" />
              <p className="text-xl">Processing your EVG data...</p>
              <p className="text-gray-400">This will take less than 3 minutes</p>
            </div>
          ) : isDragActive ? (
            <p className="text-2xl text-purple-400">Drop your .edf file here</p>
          ) : (
            <div className="space-y-4">
              <div className="w-20 h-20 mx-auto bg-gray-700 rounded-full flex items-center justify-center">
                <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <p className="text-xl">Drag & drop your 96-hour EVG .edf file</p>
              <p className="text-gray-400">or click to browse</p>
              <p className="text-sm text-gray-500 mt-4">
                Supported: OpenBCI Cyton .edf exports (6-channel RSL configuration)
              </p>
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="mt-6 p-4 bg-red-500/20 border border-red-500 rounded-lg text-red-400">
            {error}
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="mt-8 p-6 bg-gray-800/50 border border-gray-700 rounded-2xl">
            <h3 className="text-2xl font-bold mb-4 text-center">
              Document 9 — Clinical Report Generated
            </h3>

            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="text-center p-4 bg-gray-900 rounded-lg">
                <div className={`text-4xl font-bold ${
                  result.lei_v < 0.018 ? 'text-green-400' :
                  result.lei_v < 0.08 ? 'text-yellow-400' : 'text-red-400'
                }`}>
                  {result.lei_v.toFixed(5)}
                </div>
                <div className="text-gray-400 mt-1">LEI-V Value</div>
              </div>

              <div className="text-center p-4 bg-gray-900 rounded-lg">
                <div className="text-4xl font-bold text-purple-400">
                  {result.stage.replace(/_/g, ' ').toUpperCase()}
                </div>
                <div className="text-gray-400 mt-1">Classification</div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="text-center p-4 bg-gray-900 rounded-lg">
                <div className="text-2xl font-bold text-blue-400">
                  {result.confidence_percent.toFixed(1)}%
                </div>
                <div className="text-gray-400 mt-1">Confidence</div>
              </div>

              <div className="text-center p-4 bg-gray-900 rounded-lg">
                <div className="text-2xl font-bold text-green-400">
                  {result.processing_time_seconds.toFixed(2)}s
                </div>
                <div className="text-gray-400 mt-1">Processing Time</div>
              </div>
            </div>

            <div className="p-4 bg-gray-900 rounded-lg mb-6">
              <div className="text-xs text-gray-500 mb-1">Audit Hash (SHA-256)</div>
              <div className="font-mono text-sm text-gray-300 break-all">
                {result.audit_hash}
              </div>
            </div>

            <div className="flex gap-4 justify-center">
              <button className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition">
                Download PDF Report
              </button>
              <button className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold transition">
                Download JSON
              </button>
            </div>

            <p className="text-center text-gray-500 text-sm mt-6">
              This report is cryptographically signed and timestamped on Bitcoin blockchain.
            </p>
          </div>
        )}

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-500 text-sm pb-8">
          <p>Viduya Family Legacy Glyph (C) 2025 – All Rights Reserved</p>
          <p className="mt-1">Creator: Ariel Viduya Manosca | Author: IAMVC Holdings LLC</p>
          <p className="mt-4 text-xs">
            THIS SYSTEM IS FOR CLINICAL DECISION SUPPORT ONLY.<br/>
            FINAL DIAGNOSIS MUST BE CONFIRMED BY A QUALIFIED HEALTHCARE PROVIDER.
          </p>
        </footer>
      </main>
    </div>
  );
}

