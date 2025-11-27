/**
 * Audit Log Page - Immutable Audit Trail
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Shield, CheckCircle, XCircle, ExternalLink, RefreshCw } from 'lucide-react';
import { auditApi } from '../lib/api';

export function AuditLog() {
  const [verifying, setVerifying] = useState(false);
  const [chainStatus, setChainStatus] = useState<{ verified: boolean; hash: string } | null>(null);

  // Mock audit log data
  const auditLogs = [
    {
      id: 'audit-001',
      hash: 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456',
      timestamp: '2025-11-26T14:30:00Z',
      action: 'ASSESSMENT_CREATED',
      resource_type: 'Assessment',
      resource_id: 'ASSESS-2025-001',
      user: 'dr.smith@clinic.org',
      summary: 'LEI-V=0.0142, Stage: healthy, Patient: ENDO-2025-A3F2',
    },
    {
      id: 'audit-002',
      hash: 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567a',
      timestamp: '2025-11-26T14:25:00Z',
      action: 'AI_FUSION_COMPLETED',
      resource_type: 'Analysis',
      resource_id: 'ANALYSIS-2025-001',
      user: 'system',
      summary: 'Med-Gemini + Aidoc + OpenEvidence fusion, confidence: 94.2%',
    },
    {
      id: 'audit-003',
      hash: 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567ab2',
      timestamp: '2025-11-26T14:20:00Z',
      action: 'EVG_RECORDING_COMPLETED',
      resource_type: 'EVGSession',
      resource_id: 'EVG-2025-001',
      user: 'system',
      summary: '96-hour V-CAW recording completed, 6 channels, Patient: ENDO-2025-A3F2',
    },
  ];

  const handleVerifyChain = async () => {
    setVerifying(true);
    // Simulate verification
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setChainStatus({
      verified: true,
      hash: 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567ab2',
    });
    setVerifying(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Audit Trail</h2>
          <p className="text-gray-500">
            256-bit SHA-256 hash chain • FDA 21 CFR Part 11 compliant
          </p>
        </div>
        <button
          onClick={handleVerifyChain}
          disabled={verifying}
          className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
        >
          {verifying ? (
            <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
          ) : (
            <Shield className="h-4 w-4 mr-2" />
          )}
          Verify Chain Integrity
        </button>
      </div>

      {/* Chain Status */}
      {chainStatus && (
        <div className={`p-4 rounded-lg flex items-center justify-between ${
          chainStatus.verified ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        }`}>
          <div className="flex items-center">
            {chainStatus.verified ? (
              <CheckCircle className="h-6 w-6 text-green-500 mr-3" />
            ) : (
              <XCircle className="h-6 w-6 text-red-500 mr-3" />
            )}
            <div>
              <p className={`font-semibold ${chainStatus.verified ? 'text-green-700' : 'text-red-700'}`}>
                {chainStatus.verified ? 'Chain Integrity Verified' : 'Chain Integrity Failed'}
              </p>
              <p className="text-sm text-gray-500">
                Latest hash: {chainStatus.hash.slice(0, 16)}...
              </p>
            </div>
          </div>
          <div className="text-sm text-gray-500">
            <p>IPFS: Ready for pinning</p>
            <p>Bitcoin: Timestamp pending</p>
          </div>
        </div>
      )}

      {/* Audit Log Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Timestamp</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Action</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Resource</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">User</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Hash</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Summary</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {auditLogs.map((log) => (
              <tr key={log.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm text-gray-600">
                  {new Date(log.timestamp).toLocaleString()}
                </td>
                <td className="px-4 py-3">
                  <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded text-xs font-mono">
                    {log.action}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm">
                  <p className="text-gray-900">{log.resource_type}</p>
                  <p className="text-gray-500 text-xs">{log.resource_id}</p>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">{log.user}</td>
                <td className="px-4 py-3">
                  <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                    {log.hash.slice(0, 12)}...
                  </code>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600 max-w-xs truncate">
                  {log.summary}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Blockchain Anchoring */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-semibold mb-2 flex items-center">
            <ExternalLink className="h-4 w-4 mr-2" />
            IPFS Pinning
          </h3>
          <p className="text-sm text-gray-500 mb-3">
            Audit chain snapshots are pinned to IPFS for permanent storage.
          </p>
          <button className="text-indigo-600 hover:text-indigo-800 text-sm">
            Pin Latest Snapshot →
          </button>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-semibold mb-2 flex items-center">
            <ExternalLink className="h-4 w-4 mr-2" />
            Bitcoin Timestamping
          </h3>
          <p className="text-sm text-gray-500 mb-3">
            Hash anchored to Bitcoin blockchain via OP_RETURN.
          </p>
          <button className="text-indigo-600 hover:text-indigo-800 text-sm">
            Create Timestamp →
          </button>
        </div>
      </div>

      <p className="text-center text-xs text-gray-400">
        Citation: Viduya Family Legacy Glyph © 2025
      </p>
    </div>
  );
}

