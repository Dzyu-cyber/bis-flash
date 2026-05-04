import React from 'react';
import { Activity, Clock, Database, Zap } from 'lucide-react';
import { translations } from '../utils/translations';

export default function MetricsDashboard({ latency, lang }) {
  const t = translations[lang];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-md mb-xl">
      <MetricCard 
        title="Vector Index Size" 
        value="12.4M" 
        unit="embeddings"
        icon={<Database className="w-5 h-5 text-primary" />}
        trend="+14% this week"
      />
      <MetricCard 
        title={t.latency} 
        value={latency || "0.0"} 
        unit="s"
        icon={<Clock className="w-5 h-5 text-secondary" />}
        trend={latency > 0 ? "Real-time query" : "Waiting for query..."}
        trendPositive={latency > 0}
      />
      <MetricCard 
        title={t.relevance} 
        value="96.8" 
        unit="%"
        icon={<Zap className="w-5 h-5 text-tertiary" />}
        trend="Peak performance"
      />
      <MetricCard 
        title={t.coverage} 
        value="Optimal" 
        unit=""
        icon={<Activity className="w-5 h-5 text-secondary" />}
        trend="All nodes active"
        trendPositive
      />
    </div>
  );
}

function MetricCard({ title, value, unit, icon, trend, trendPositive }) {
  return (
    <div className="bg-surface-container border border-surface-container-highest rounded-lg p-md">
      <div className="flex justify-between items-start mb-sm">
        <h4 className="font-mono text-xs text-outline-variant uppercase tracking-wider">{title}</h4>
        {icon}
      </div>
      <div className="flex items-baseline gap-xs mb-xs">
        <span className="text-3xl font-semibold text-on-surface tracking-tight">{value}</span>
        <span className="text-on-surface-variant text-sm font-medium">{unit}</span>
      </div>
      <div className={`text-xs font-mono tracking-wide ${trendPositive ? 'text-secondary' : 'text-outline'}`}>
        {trend}
      </div>
    </div>
  );
}
