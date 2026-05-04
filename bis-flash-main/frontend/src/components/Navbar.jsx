import React from 'react';
import { Shield, Settings, Activity, Languages } from 'lucide-react';

export default function Navbar({ lang, setLang }) {
  const languages = [
    { code: 'en', label: 'EN' },
    { code: 'te', label: 'తె' },
    { code: 'hi', label: 'हि' }
  ];

  return (
    <nav className="border-b border-surface-container-highest bg-surface-dim sticky top-0 z-50">
      <div className="max-w-[1280px] mx-auto px-lg py-md flex items-center justify-between">
        <div className="flex items-center gap-sm">
          <Shield className="w-6 h-6 text-primary" />
          <span className="font-mono text-lg font-bold tracking-tight text-on-surface">BIS_STANDARD_AI</span>
        </div>
        
        <div className="flex items-center gap-md">
          <div className="flex items-center bg-surface-container rounded-full px-xs py-1 border border-outline-variant mr-md">
            <Languages className="w-4 h-4 text-outline-variant mx-sm" />
            {languages.map((l) => (
              <button
                key={l.code}
                onClick={() => setLang(l.code)}
                className={`px-sm py-0.5 rounded-full text-xs font-bold transition-all ${
                  lang === l.code 
                    ? 'bg-primary text-on-primary shadow-sm' 
                    : 'text-on-surface-variant hover:text-on-surface'
                }`}
              >
                {l.label}
              </button>
            ))}
          </div>

          <button className="text-on-surface-variant hover:text-primary transition-colors flex items-center gap-xs text-sm font-mono uppercase tracking-wider">
            <Activity className="w-4 h-4" />
            Metrics
          </button>
          <button className="text-on-surface-variant hover:text-primary transition-colors flex items-center gap-xs text-sm font-mono uppercase tracking-wider">
            <Settings className="w-4 h-4" />
            Config
          </button>
          <button className="btn-primary ml-sm text-sm py-xs px-md">
            Deploy
          </button>
        </div>
      </div>
    </nav>
  );
}
