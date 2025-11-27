/**
 * ENDOCHAIN-VIDUYA-2025 Tailwind Configuration
 * Viduya Family Legacy Glyph © 2025 – All Rights Reserved
 */

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ENDOCHAIN brand colors
        'endo-primary': '#6366f1',
        'endo-secondary': '#8b5cf6',
        'endo-healthy': '#22c55e',
        'endo-warning': '#f59e0b',
        'endo-danger': '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};

