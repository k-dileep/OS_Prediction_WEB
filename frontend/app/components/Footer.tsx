'use client';

import { useState, useEffect } from 'react';

export default function Footer() {
  const [year, setYear] = useState('');
  
  useEffect(() => {
    setYear(new Date().getFullYear().toString());
  }, []);

  return (
    <footer className="mt-8 py-4 text-center text-sm text-gray-500">
      <p>© {year} Oxidative Stress Prediction System</p>
    </footer>
  );
} 