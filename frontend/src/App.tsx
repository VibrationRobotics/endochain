/**
 * ENDOCHAIN-VIDUYA-2025 Medical Dashboard
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 * 
 * Main application component with routing and layout.
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Assessment } from './pages/Assessment';
import { PatientHistory } from './pages/PatientHistory';
import { GlyphViewer } from './pages/GlyphViewer';
import { AuditLog } from './pages/AuditLog';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 3,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="assessment" element={<Assessment />} />
            <Route path="assessment/:id" element={<Assessment />} />
            <Route path="patient/:id" element={<PatientHistory />} />
            <Route path="glyph" element={<GlyphViewer />} />
            <Route path="audit" element={<AuditLog />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

