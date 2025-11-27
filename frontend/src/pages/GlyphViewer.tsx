/**
 * Glyph Viewer Page - Interactive 3D Viduya Legacy Glyph
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

import { useState } from 'react';
import { GlyphVisualization } from '../components/GlyphVisualization';
import { Info, Hexagon, Triangle, Circle } from 'lucide-react';

// Exact symbolic coordinates from Viduya Legacy Glyph
const GLYPH_COORDINATES = {
  triangleHexagon: [
    { name: 'TH_axial_pos', x: '√3/4', y: '0', approx: '(0.433, 0)' },
    { name: 'TH_axial_neg', x: '-√3/4', y: '0', approx: '(-0.433, 0)' },
    { name: 'TH_offaxis_1', x: '√3/8', y: '3/8', approx: '(0.217, 0.375)' },
    { name: 'TH_offaxis_2', x: '-√3/8', y: '3/8', approx: '(-0.217, 0.375)' },
    { name: 'TH_offaxis_3', x: '√3/8', y: '-3/8', approx: '(0.217, -0.375)' },
    { name: 'TH_offaxis_4', x: '-√3/8', y: '-3/8', approx: '(-0.217, -0.375)' },
  ],
  vesicaHexagon: [
    { name: 'VH_pos', x: '√3(3/80 + √229/80)', y: '-37/80 + √229/80', approx: '(0.361, -0.273)' },
    { name: 'VH_neg', x: '√3(3/80 - √229/80)', y: '-37/80 + √229/80', approx: '(-0.296, -0.273)' },
  ],
  hiddenStarTriangle: [
    { name: 'HST_pos', x: '7/40 - √2/4', y: '-3/8', approx: '(-0.179, -0.375)' },
    { name: 'HST_neg', x: '-(7/40 - √2/4)', y: '-3/8', approx: '(0.179, -0.375)' },
  ],
};

export function GlyphViewer() {
  const [activeLayer, setActiveLayer] = useState<string | null>(null);
  const [showCoordinates, setShowCoordinates] = useState(true);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Viduya Legacy Glyph Viewer
          </h2>
          <p className="text-gray-500">
            Interactive visualization of the geometric foundation
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowCoordinates(!showCoordinates)}
            className={`px-3 py-1 rounded text-sm ${
              showCoordinates ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-700'
            }`}
          >
            {showCoordinates ? 'Hide' : 'Show'} Coordinates
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 3D Visualization */}
        <div className="lg:col-span-2">
          <GlyphVisualization />
        </div>

        {/* Layer Controls */}
        <div className="space-y-4">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-3 flex items-center">
              <Info className="h-4 w-4 mr-2" />
              Glyph Layers
            </h3>
            <div className="space-y-2">
              <button
                onClick={() => setActiveLayer('triangleHexagon')}
                className={`w-full flex items-center p-2 rounded ${
                  activeLayer === 'triangleHexagon' ? 'bg-indigo-50 border-indigo-500' : 'hover:bg-gray-50'
                } border`}
              >
                <Hexagon className="h-4 w-4 mr-2 text-indigo-600" />
                <span className="text-sm">Triangle-Hexagon (6 points)</span>
              </button>
              <button
                onClick={() => setActiveLayer('vesicaHexagon')}
                className={`w-full flex items-center p-2 rounded ${
                  activeLayer === 'vesicaHexagon' ? 'bg-purple-50 border-purple-500' : 'hover:bg-gray-50'
                } border`}
              >
                <Circle className="h-4 w-4 mr-2 text-purple-600" />
                <span className="text-sm">Vesica-Hexagon (4 points)</span>
              </button>
              <button
                onClick={() => setActiveLayer('hiddenStarTriangle')}
                className={`w-full flex items-center p-2 rounded ${
                  activeLayer === 'hiddenStarTriangle' ? 'bg-amber-50 border-amber-500' : 'hover:bg-gray-50'
                } border`}
              >
                <Triangle className="h-4 w-4 mr-2 text-amber-600" />
                <span className="text-sm">Hidden Star-Triangle (2 points)</span>
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-3">Symmetry Properties</h3>
            <div className="text-sm space-y-2">
              <p><strong>Group:</strong> C₃ × D₆</p>
              <p><strong>Rotational:</strong> 120° (3-fold)</p>
              <p><strong>Dihedral:</strong> 6-fold reflection</p>
              <p><strong>RSL Radius:</strong> √3/4 ≈ 0.433</p>
            </div>
          </div>
        </div>
      </div>

      {/* Coordinate Table */}
      {showCoordinates && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-4 py-3 border-b bg-gray-50">
            <h3 className="font-semibold">Exact Symbolic Coordinates</h3>
            <p className="text-xs text-gray-500">
              All coordinates are exact algebraic expressions (no floating-point approximations in computation)
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Layer</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Point</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">x (symbolic)</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">y (symbolic)</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">≈ (float)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {Object.entries(GLYPH_COORDINATES).flatMap(([layer, points]) =>
                  points.map((point, i) => (
                    <tr key={`${layer}-${i}`} className="hover:bg-gray-50">
                      <td className="px-4 py-2 text-sm">{layer}</td>
                      <td className="px-4 py-2 text-sm font-mono">{point.name}</td>
                      <td className="px-4 py-2 text-sm font-mono">{point.x}</td>
                      <td className="px-4 py-2 text-sm font-mono">{point.y}</td>
                      <td className="px-4 py-2 text-sm text-gray-500">{point.approx}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="text-center text-sm text-gray-500">
        <p className="font-medium">Viduya Family Legacy Glyph © 2025</p>
        <p className="text-xs">
          All geometry computations use symbolic mathematics for exact precision.
          No floating-point approximations in diagnostic calculations.
        </p>
      </div>
    </div>
  );
}

