import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Check, Loader2 } from 'lucide-react';

export default function SetupProgress({ onComplete }) {
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState('initializing'); // initializing, running, complete
  const hasRun = useRef(false);

  const steps = [
    { msg: "Initializing system environment...", delay: 800 },
    { msg: "Loading BIS Standard vector embeddings...", delay: 1500 },
    { msg: "Connecting to Pinecone index 'bis-standards-v2'...", delay: 1200 },
    { msg: "Index connected. Dimension: 768, Metric: Cosine", delay: 800 },
    { msg: "Initializing Gemini 1.5 Pro inference engine...", delay: 2000 },
    { msg: "Loading cross-encoder re-ranking models...", delay: 1500 },
    { msg: "System ready. Awaiting semantic queries.", delay: 1000 },
  ];

  useEffect(() => {
    let currentStep = 0;
    let timeoutId;
    let mounted = true;

    setStatus('running');
    setLogs([]); // Reset logs on mount to avoid duplicates in strict mode
    
    const runStep = () => {
      if (!mounted) return;
      
      if (currentStep < steps.length) {
        setLogs(prev => {
          // Prevent duplicates by checking if we already have this step
          if (prev.some(log => log.id === currentStep)) return prev;
          return [...prev, { id: currentStep, ...steps[currentStep] }];
        });
        
        timeoutId = setTimeout(() => {
          currentStep++;
          runStep();
        }, steps[currentStep].delay);
      } else {
        setStatus('complete');
        timeoutId = setTimeout(() => {
          if (mounted) onComplete();
        }, 1500);
      }
    };

    runStep();
    
    return () => {
      mounted = false;
      clearTimeout(timeoutId);
    };
  }, []);

  return (
    <div className="bg-surface-container-lowest border border-surface-container-highest rounded-lg p-lg font-mono text-sm shadow-2xl mx-auto max-w-3xl w-full">
      <div className="flex items-center gap-sm mb-md border-b border-surface-container-highest pb-sm">
        <Terminal className="w-5 h-5 text-outline" />
        <span className="text-outline-variant tracking-widest uppercase text-xs">Setup Sequence</span>
        <div className="ml-auto flex gap-2">
          <div className="w-3 h-3 rounded-full bg-error/50"></div>
          <div className="w-3 h-3 rounded-full bg-tertiary/50"></div>
          <div className="w-3 h-3 rounded-full bg-secondary/50"></div>
        </div>
      </div>
      
      <div className="space-y-sm min-h-[300px]">
        {logs.map((log, index) => (
          <div key={log.id} className="flex items-start gap-sm animate-in fade-in duration-300">
            <span className="text-primary mt-0.5">➜</span>
            <span className={index === logs.length - 1 && status !== 'complete' ? 'text-on-surface' : 'text-on-surface-variant'}>
              {log.msg}
            </span>
            {index < logs.length - 1 && (
              <Check className="w-4 h-4 text-secondary ml-auto" />
            )}
            {index === logs.length - 1 && status !== 'complete' && (
              <Loader2 className="w-4 h-4 text-primary animate-spin ml-auto" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
