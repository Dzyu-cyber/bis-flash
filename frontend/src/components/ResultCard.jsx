import React, { useState } from 'react';
import { ChevronDown, ChevronUp, FileText, CheckCircle2, AlertTriangle, ExternalLink, BarChart3 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { translations } from '../utils/translations';

export default function ResultCard({ result, lang }) {
  const [expanded, setExpanded] = useState(false);
  const t = translations[lang];

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-secondary bg-secondary/10 border-secondary/20';
    if (score >= 75) return 'text-tertiary bg-tertiary/10 border-tertiary/20';
    return 'text-error bg-error/10 border-error/20';
  };

  return (
    <div className="card card-hover transition-all duration-300">
      <div className="flex flex-col md:flex-row gap-md justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center gap-sm mb-sm">
            <span className="font-mono font-bold text-primary tracking-wide">{result.id}</span>
            <span className="chip-status bg-surface-bright border border-outline-variant text-on-surface-variant">
              {result.category}
            </span>
            <span className={`chip-status border ${getScoreColor(result.confidenceScore)}`}>
              {result.confidenceScore}% {t.match || "Match"}
            </span>
          </div>
          <h3 className="text-xl font-semibold text-on-surface mb-xs">{result.title}</h3>
          <p className="text-on-surface-variant line-clamp-2">{result.summary}</p>
        </div>
        
        <div className="flex flex-col items-end gap-sm w-full md:w-auto">
          <button className="btn-secondary flex items-center justify-center gap-xs w-full md:w-auto text-sm py-xs">
            <FileText className="w-4 h-4" />
            {t.viewDocument}
          </button>
        </div>
      </div>

      {/* Statistics Section - Data Related Graph */}
      <div className="mt-lg p-md bg-surface-container-low border border-surface-container-highest rounded-lg">
        <div className="flex items-center gap-sm mb-md">
          <BarChart3 className="w-4 h-4 text-primary" />
          <h4 className="font-mono text-xs text-outline-variant uppercase tracking-wider">{t.distribution || "Semantic Similarity Distribution"}</h4>
        </div>
        <div className="h-[120px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={result.stats}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
              <XAxis dataKey="name" hide />
              <YAxis hide domain={[0, 1000]} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1C1B1F', border: '1px solid #49454F', borderRadius: '8px', fontSize: '12px' }}
                itemStyle={{ color: '#D0BCFF' }}
              />
              <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                {result.stats.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 3 ? '#D0BCFF' : '#49454F'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-md pt-md border-t border-surface-container-highest">
        <button 
          onClick={() => setExpanded(!expanded)}
          className="flex items-center gap-xs text-sm font-mono uppercase tracking-wider text-primary hover:text-primary-container transition-colors w-full justify-between"
        >
          <span>{t.aiRationale}</span>
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
        
        {expanded && (
          <div className="mt-md bg-surface-container-lowest border border-surface-container-highest rounded p-md animate-in slide-in-from-top-2 duration-200">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-lg">
              <div>
                <h4 className="font-mono text-xs text-outline-variant uppercase tracking-wider mb-sm flex items-center gap-xs">
                  <SparkleIcon className="w-4 h-4 text-primary" />
                  {t.reasoningTrace || "Reasoning Trace"}
                </h4>
                <p className="text-sm text-on-surface-variant leading-relaxed">
                  {result.rationale}
                </p>
              </div>
              <div>
                <h4 className="font-mono text-xs text-outline-variant uppercase tracking-wider mb-sm flex items-center gap-xs">
                  <CheckCircle2 className="w-4 h-4 text-secondary" />
                  {t.keyEntities || "Key Entities Extracted"}
                </h4>
                <ul className="space-y-sm">
                  {result.entities.map((entity, i) => (
                    <li key={i} className="flex items-start gap-sm text-sm">
                      <span className="w-1.5 h-1.5 rounded-full bg-secondary mt-1.5 flex-shrink-0"></span>
                      <span className="text-on-surface">{entity}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function SparkleIcon(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
    </svg>
  );
}
