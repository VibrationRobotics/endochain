/**
 * ENDOCHAIN Dashboard Layout
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

import { Outlet, Link, useLocation } from 'react-router-dom';
import { 
  Home, FileSearch, Users, Hexagon, Shield, Settings 
} from 'lucide-react';
import clsx from 'clsx';

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'New Assessment', href: '/assessment', icon: FileSearch },
  { name: 'Patients', href: '/patients', icon: Users },
  { name: 'Glyph Viewer', href: '/glyph', icon: Hexagon },
  { name: 'Audit Log', href: '/audit', icon: Shield },
];

export function Layout() {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <Hexagon className="h-8 w-8 text-white" />
              <div>
                <h1 className="text-xl font-bold text-white">
                  ENDOCHAIN-VIDUYA-2025
                </h1>
                <p className="text-xs text-indigo-200">
                  Viduya Family Legacy Glyph © 2025
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-indigo-200">
                LEI-V Diagnostic System
              </span>
              <button className="p-2 rounded-full hover:bg-indigo-500 transition">
                <Settings className="h-5 w-5 text-white" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={clsx(
                    'flex items-center space-x-2 py-4 border-b-2 text-sm font-medium transition',
                    isActive
                      ? 'border-indigo-600 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  )}
                >
                  <item.icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-400 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm">
                © 2025 IAMVC Holdings LLC. All rights reserved.
              </p>
              <p className="text-xs text-gray-500">
                Viduya Family Legacy Glyph © 2025 – FDA 510(k) De Novo | EU MDR Class IIa
              </p>
            </div>
            <div className="flex space-x-4 text-xs">
              <span>HIPAA Compliant</span>
              <span>|</span>
              <span>FHIR R5</span>
              <span>|</span>
              <span>HL7v2</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

