import React from 'react';
import { Database, Search, Brain, FileOutput } from 'lucide-react';
import { translations } from '../utils/translations';

export default function PipelineTimeline({ lang }) {
  const t = translations[lang];

  const steps = [
    {
      id: 1,
      title: "Query Expansion",
      description: "LLM expands user query with technical synonyms and context.",
      icon: <Brain className="w-5 h-5 text-tertiary" />,
      time: "12ms"
    },
    {
      id: 2,
      title: "Vector Search",
      description: "Retrieval from Pinecone index using multi-modal embeddings.",
      icon: <Database className="w-5 h-5 text-primary" />,
      time: "45ms"
    },
    {
      id: 3,
      title: "Reranking & Filtering",
      description: "Cross-encoder model ranks results by semantic relevance.",
      icon: <Search className="w-5 h-5 text-secondary" />,
      time: "8ms"
    },
    {
      id: 4,
      title: "Rationale Generation",
      description: "Gemini 1.5 Pro generates explanation for top matches.",
      icon: <FileOutput className="w-5 h-5 text-primary" />,
      time: "115ms"
    }
  ];

  return (
    <div className="card mb-xl">
      <h3 className="text-xl font-semibold text-on-surface mb-lg font-mono uppercase tracking-widest text-sm border-b border-surface-container-highest pb-sm">
        {t.pipeline} Trace
      </h3>
      
      <div className="relative">
        <div className="absolute left-[27px] top-0 bottom-0 w-[2px] bg-surface-container-highest"></div>
        
        <div className="space-y-lg">
          {steps.map((step, index) => (
            <div key={step.id} className="relative flex items-start gap-md group">
              <div className="w-[56px] h-[56px] rounded-full bg-surface-container-lowest border-2 border-surface-container-highest flex items-center justify-center flex-shrink-0 relative z-10 group-hover:border-primary transition-colors">
                {step.icon}
              </div>
              <div className="flex-1 pt-sm">
                <div className="flex justify-between items-baseline mb-xs">
                  <h4 className="text-on-surface font-semibold">{step.title}</h4>
                  <span className="font-mono text-xs text-outline-variant bg-surface-container px-2 py-1 rounded">{step.time}</span>
                </div>
                <p className="text-sm text-on-surface-variant">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
