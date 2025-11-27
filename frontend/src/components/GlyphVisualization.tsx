/**
 * 3D Viduya Legacy Glyph Visualization - KILLER VERSION
 * Viduya Family Legacy Glyph (C) 2025 - All Rights Reserved
 *
 * Real-time EVG signal overlay on rotating 3D pelvic glyph
 * - Color intensity = signal amplitude
 * - Opacity = drift from symmetry
 * - Pulse animation = active electrode
 */

import { useRef, useMemo, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Line, Sphere, Ring } from '@react-three/drei';
import * as THREE from 'three';

// EXACT glyph coordinates from viduya_constants.py
const SQRT3_4 = 0.4330127018922193;
const SQRT3_8 = 0.21650635094610966;

const GLYPH_POINTS = {
  triangleHexagon: [
    { x: SQRT3_4, y: 0, z: 0 },
    { x: SQRT3_8, y: 0.375, z: 0 },
    { x: -SQRT3_8, y: 0.375, z: 0 },
    { x: -SQRT3_4, y: 0, z: 0 },
    { x: -SQRT3_8, y: -0.375, z: 0 },
    { x: SQRT3_8, y: -0.375, z: 0 },
  ],
  rslElectrodes: [
    { x: SQRT3_4, y: 0, z: 0, label: 'E1' },
    { x: SQRT3_8, y: 0.375, z: 0, label: 'E2' },
    { x: -SQRT3_8, y: 0.375, z: 0, label: 'E3' },
    { x: -SQRT3_4, y: 0, z: 0, label: 'E4' },
    { x: -SQRT3_8, y: -0.375, z: 0, label: 'E5' },
    { x: SQRT3_8, y: -0.375, z: 0, label: 'E6' },
  ],
};

interface LiveEVGData {
  amplitudes: number[];      // 6 electrode amplitudes (μV)
  radialDistances: number[]; // 6 radial distances
  leiV: number;              // Current LEI-V value
  meanRadial: number;        // Mean radial distance
  isStreaming: boolean;
}

interface ElectrodeProps {
  position: [number, number, number];
  index: number;
  amplitude: number;         // Signal amplitude for color
  radialDistance: number;    // Distance for opacity/position
  meanRadial: number;        // For drift calculation
  isActive?: boolean;
  label: string;
}

function LiveElectrode({ position, index, amplitude, radialDistance, meanRadial, isActive = false, label }: ElectrodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const waveRef = useRef<THREE.Mesh>(null);

  // Calculate drift from symmetry (opacity indicator)
  const drift = Math.abs(radialDistance - meanRadial);
  const driftOpacity = Math.min(1, 0.3 + drift * 10);

  // Color based on amplitude (blue = low, green = medium, red = high)
  const color = useMemo(() => {
    const normalized = Math.min(1, Math.max(0, (amplitude - 20) / 60));
    const r = Math.floor(normalized * 255);
    const g = Math.floor((1 - Math.abs(normalized - 0.5) * 2) * 255);
    const b = Math.floor((1 - normalized) * 255);
    return `rgb(${r},${g},${b})`;
  }, [amplitude]);

  // Electrode size based on amplitude
  const size = useMemo(() => {
    return 0.025 + (amplitude / 100) * 0.02;
  }, [amplitude]);

  useFrame((state) => {
    if (meshRef.current) {
      // Pulse animation for active electrode
      const pulse = isActive ? 1 + Math.sin(state.clock.elapsedTime * 4) * 0.2 : 1;
      meshRef.current.scale.setScalar(pulse);
    }
    if (glowRef.current) {
      // Glow pulse
      glowRef.current.material.opacity = 0.3 + Math.sin(state.clock.elapsedTime * 2) * 0.2;
    }
    if (waveRef.current && isActive) {
      // Ripple effect
      const scale = 1 + ((state.clock.elapsedTime * 2) % 1) * 0.5;
      waveRef.current.scale.setScalar(scale);
      waveRef.current.material.opacity = 1 - ((state.clock.elapsedTime * 2) % 1);
    }
  });

  return (
    <group position={position}>
      {/* Outer glow ring */}
      <mesh ref={glowRef}>
        <ringGeometry args={[size * 1.5, size * 2, 32]} />
        <meshBasicMaterial color={color} transparent opacity={driftOpacity * 0.5} />
      </mesh>

      {/* Main electrode sphere */}
      <mesh ref={meshRef}>
        <sphereGeometry args={[size, 32, 32]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.5 + amplitude / 100}
          metalness={0.3}
          roughness={0.4}
        />
      </mesh>

      {/* Active ripple effect */}
      {isActive && (
        <mesh ref={waveRef}>
          <ringGeometry args={[size * 2, size * 2.2, 32]} />
          <meshBasicMaterial color={color} transparent opacity={0.5} />
        </mesh>
      )}

      {/* Amplitude value display */}
      <Text
        position={[0, size + 0.04, 0]}
        fontSize={0.025}
        color="#ffffff"
        anchorX="center"
        anchorY="bottom"
        outlineWidth={0.002}
        outlineColor="#000000"
      >
        {label}: {amplitude.toFixed(1)}μV
      </Text>

      {/* Drift indicator line */}
      {drift > 0.01 && (
        <Line
          points={[[0, 0, 0], [0, 0, drift * 2]]}
          color="#ff6b6b"
          lineWidth={2}
        />
      )}
    </group>
  );
}

function AnimatedHexagon({ leiV }: { leiV: number }) {
  const lineRef = useRef<any>(null);

  const points = useMemo(() => {
    const pts = GLYPH_POINTS.rslElectrodes.map(p => new THREE.Vector3(p.x, p.y, p.z));
    return [...pts, pts[0]];
  }, []);

  // Color based on LEI-V (healthy=green, stage0=yellow, advanced=red)
  const color = useMemo(() => {
    if (leiV < 0.018) return '#22c55e';
    if (leiV < 0.08) return '#f59e0b';
    return '#ef4444';
  }, [leiV]);

  useFrame((state) => {
    if (lineRef.current) {
      // Subtle breathing animation
      const scale = 1 + Math.sin(state.clock.elapsedTime * 0.5) * 0.02;
      lineRef.current.scale.setScalar(scale);
    }
  });

  return (
    <group ref={lineRef}>
      <Line points={points} color={color} lineWidth={3} />
      {/* Inner hexagon */}
      <Line
        points={points.map(p => new THREE.Vector3(p.x * 0.8, p.y * 0.8, p.z))}
        color={color}
        lineWidth={1}
        opacity={0.3}
        transparent
      />
    </group>
  );
}

function GlyphTriangle({ rotating }: { rotating: boolean }) {
  const groupRef = useRef<THREE.Group>(null);

  const points = useMemo(() => {
    const s = 0.65;
    return [
      new THREE.Vector3(0, s * 0.5, 0),
      new THREE.Vector3(-s * SQRT3_4, -s * 0.25, 0),
      new THREE.Vector3(s * SQRT3_4, -s * 0.25, 0),
      new THREE.Vector3(0, s * 0.5, 0),
    ];
  }, []);

  useFrame((state) => {
    if (groupRef.current && rotating) {
      groupRef.current.rotation.z = state.clock.elapsedTime * 0.1;
    }
  });

  return (
    <group ref={groupRef}>
      <Line points={points} color="#8b5cf6" lineWidth={2} dashed />
      {/* Inverted triangle */}
      <Line
        points={points.map(p => new THREE.Vector3(p.x, -p.y, p.z))}
        color="#8b5cf6"
        lineWidth={1}
        opacity={0.4}
        transparent
      />
    </group>
  );
}

function PelvicOutline() {
  const curve = useMemo(() => {
    const points = [];
    for (let i = 0; i <= 100; i++) {
      const t = (i / 100) * Math.PI * 2;
      const r = 0.55 + 0.1 * Math.cos(t * 2) + 0.05 * Math.sin(t * 4);
      points.push(new THREE.Vector3(r * Math.cos(t), r * Math.sin(t) * 0.75, 0));
    }
    return points;
  }, []);

  return (
    <Line points={curve} color="#4b5563" lineWidth={1} dashed />
  );
}

function LEIVDisplay({ leiV, stage }: { leiV: number; stage: string }) {
  const color = leiV < 0.018 ? '#22c55e' : leiV < 0.08 ? '#f59e0b' : '#ef4444';

  return (
    <group position={[0, -0.55, 0]}>
      <Text
        fontSize={0.06}
        color={color}
        anchorX="center"
        outlineWidth={0.003}
        outlineColor="#000000"
      >
        LEI-V: {leiV.toFixed(5)}
      </Text>
      <Text
        position={[0, -0.08, 0]}
        fontSize={0.04}
        color="#9ca3af"
        anchorX="center"
      >
        {stage.toUpperCase().replace('_', ' ')}
      </Text>
    </group>
  );
}

function SignalWaveform({ amplitudes, position }: { amplitudes: number[]; position: [number, number, number] }) {
  const points = useMemo(() => {
    return amplitudes.map((a, i) =>
      new THREE.Vector3(position[0] + i * 0.05 - 0.125, position[1] + (a - 45) * 0.002, position[2])
    );
  }, [amplitudes, position]);

  return <Line points={points} color="#60a5fa" lineWidth={2} />;
}

interface GlyphVisualizationProps {
  electrodeValues?: number[];      // Amplitudes for color
  radialDistances?: number[];      // Distances for position/opacity
  leiV?: number;
  stage?: string;
  activeElectrode?: number;
  isStreaming?: boolean;
}

export function GlyphVisualization({
  electrodeValues = [45, 42, 48, 44, 46, 43],
  radialDistances = [0.44, 0.43, 0.45, 0.42, 0.44, 0.43],
  leiV = 0.0358,
  stage = 'stage_0_early',
  activeElectrode,
  isStreaming = false,
}: GlyphVisualizationProps) {
  const [time, setTime] = useState(0);
  const meanRadial = useMemo(() =>
    radialDistances.reduce((a, b) => a + b, 0) / radialDistances.length,
    [radialDistances]
  );

  // Simulate streaming data
  useEffect(() => {
    if (isStreaming) {
      const interval = setInterval(() => setTime(t => t + 1), 100);
      return () => clearInterval(interval);
    }
  }, [isStreaming]);

  // Animated values when streaming
  const animatedAmplitudes = useMemo(() => {
    if (!isStreaming) return electrodeValues;
    return electrodeValues.map((v, i) =>
      v + Math.sin(time * 0.1 + i) * 5 + Math.random() * 2
    );
  }, [electrodeValues, isStreaming, time]);

  return (
    <div className="relative w-full h-[500px] bg-gradient-to-b from-gray-900 to-black rounded-xl overflow-hidden border border-gray-800">
      {/* Streaming indicator */}
      {isStreaming && (
        <div className="absolute top-4 left-4 flex items-center space-x-2 z-10">
          <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
          <span className="text-red-400 text-sm font-medium">LIVE EVG</span>
        </div>
      )}

      {/* LEI-V Badge */}
      <div className="absolute top-4 right-4 bg-black/60 rounded-lg px-4 py-2 z-10">
        <div className={`text-2xl font-bold ${
          leiV < 0.018 ? 'text-green-400' : leiV < 0.08 ? 'text-yellow-400' : 'text-red-400'
        }`}>
          {leiV.toFixed(5)}
        </div>
        <div className="text-xs text-gray-400 uppercase">{stage.replace(/_/g, ' ')}</div>
      </div>

      <Canvas camera={{ position: [0, 0, 1.8], fov: 45 }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[5, 5, 5]} intensity={0.8} />
        <pointLight position={[-5, -5, 5]} intensity={0.4} color="#8b5cf6" />

        {/* Background grid */}
        <gridHelper args={[2, 20, '#1f2937', '#1f2937']} rotation={[Math.PI / 2, 0, 0]} position={[0, 0, -0.1]} />

        {/* Pelvic outline */}
        <PelvicOutline />

        {/* Animated hexagon */}
        <AnimatedHexagon leiV={leiV} />

        {/* Rotating triangle */}
        <GlyphTriangle rotating={isStreaming} />

        {/* Live electrodes with signal overlay */}
        {GLYPH_POINTS.rslElectrodes.map((pos, i) => (
          <LiveElectrode
            key={i}
            position={[pos.x, pos.y, pos.z]}
            index={i}
            amplitude={animatedAmplitudes[i]}
            radialDistance={radialDistances[i]}
            meanRadial={meanRadial}
            isActive={activeElectrode === i || (isStreaming && i === time % 6)}
            label={pos.label}
          />
        ))}

        {/* Center symmetry indicator */}
        <group position={[0, 0, 0]}>
          <Ring args={[0.015, 0.025, 32]}>
            <meshBasicMaterial color="#6366f1" />
          </Ring>
          <Sphere args={[0.008, 16, 16]}>
            <meshStandardMaterial color="#ffffff" emissive="#6366f1" emissiveIntensity={0.5} />
          </Sphere>
        </group>

        {/* LEI-V display in 3D */}
        <LEIVDisplay leiV={leiV} stage={stage} />

        {/* Controls */}
        <OrbitControls
          enablePan={false}
          minDistance={1}
          maxDistance={4}
          enableDamping
          autoRotate={isStreaming}
          autoRotateSpeed={0.5}
        />
      </Canvas>

      {/* Bottom legend */}
      <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end z-10">
        <div className="bg-black/60 rounded-lg px-3 py-2 text-xs">
          <div className="flex items-center space-x-4 text-white">
            <span className="flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-1" />
              Healthy (&lt;0.018)
            </span>
            <span className="flex items-center">
              <span className="w-2 h-2 bg-yellow-500 rounded-full mr-1" />
              Stage-0 (0.018-0.08)
            </span>
            <span className="flex items-center">
              <span className="w-2 h-2 bg-red-500 rounded-full mr-1" />
              Advanced (&gt;0.08)
            </span>
          </div>
          <p className="mt-2 text-gray-500 text-center">
            Viduya Family Legacy Glyph (C) 2025 | C₃ × D₆ Symmetry
          </p>
        </div>

        {/* Waveform preview */}
        {isStreaming && (
          <div className="bg-black/60 rounded-lg px-3 py-2">
            <div className="text-xs text-gray-400 mb-1">Signal Preview</div>
            <div className="w-32 h-8 bg-gray-900 rounded overflow-hidden">
              {/* Mini waveform would render here */}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

