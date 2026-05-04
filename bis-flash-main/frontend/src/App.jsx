import React, { useState, useEffect, useMemo } from 'react';
import Navbar from './components/Navbar';
import SearchPanel from './components/SearchPanel';
import ResultCard from './components/ResultCard';
import MetricsDashboard from './components/MetricsDashboard';
import PipelineTimeline from './components/PipelineTimeline';
import SetupProgress from './components/SetupProgress';
import { translations } from './utils/translations';

const mockResults = [
  {
    id: "IS 16221 (Part 1) : 2015",
    title: "Electric Vehicle Conductive Charging System Part 1 General Requirements",
    category: "Automotive",
    confidenceScore: 94,
    summary: "Specifies the general requirements for conductive charging of electric vehicles. It covers the characteristics and operating conditions of the supply device and the connection to the EV.",
    rationale: "The user query specifically mentions 'charging stations' and 'safety'. This standard directly addresses the general requirements for EV charging, which fundamentally encompasses safety protocols and operational conditions for the supply device. The vector similarity is exceptionally high due to exact multi-word matches in the embeddings.",
    entities: ["Electric Vehicle", "Conductive Charging", "Supply Device", "Safety Requirements"],
    stats: [
      { name: 'Jan', value: 400 },
      { name: 'Feb', value: 300 },
      { name: 'Mar', value: 600 },
      { name: 'Apr', value: 800 },
    ]
  },
  {
    id: "IS 17017 (Part 2) : 2018",
    title: "Electric Vehicle Conductive AC Charging System",
    category: "Electrical",
    confidenceScore: 88,
    summary: "Applies to equipment for the AC charging of electric vehicles with a rated supply voltage up to 1 000 V AC and a rated output voltage up to 1 000 V AC.",
    rationale: "While the query doesn't specify AC or DC, AC charging is the most common form of domestic and commercial EV charging infrastructure. This standard provides crucial specifications for AC systems, making it highly relevant to a general search for EV charging station standards.",
    entities: ["AC Charging", "Voltage Specifications", "Equipment Requirements"],
    stats: [
      { name: 'Jan', value: 200 },
      { name: 'Feb', value: 500 },
      { name: 'Mar', value: 400 },
      { name: 'Apr', value: 700 },
    ]
  },
  {
    id: "IS 16221 (Part 2) : 2015",
    title: "Electric Vehicle Conductive Charging System Part 2 Plugs, Socket-Outlets, Vehicle Connectors",
    category: "Component",
    confidenceScore: 72,
    summary: "Applies to plugs, socket-outlets, vehicle connectors and vehicle inlets with pins and contact tubes of standardized configurations.",
    rationale: "Safety is highly dependent on the physical connection points. This standard details the requirements for plugs and sockets, which are critical safety components of any charging station, though it's less comprehensive than Part 1.",
    entities: ["Plugs", "Socket-Outlets", "Connectors"],
    stats: [
      { name: 'Jan', value: 100 },
      { name: 'Feb', value: 200 },
      { name: 'Mar', value: 300 },
      { name: 'Apr', value: 400 },
    ]
  }
];

export default function App() {
  const [setupComplete, setSetupComplete] = useState(false);
  const [results, setResults] = useState(null);
  const [lang, setLang] = useState('en');
  const [latency, setLatency] = useState(0);
  const [isSearching, setIsSearching] = useState(false);

  const t = translations[lang];

  // Derived results to ensure they translate immediately when lang changes if possible
  const localizedResults = useMemo(() => {
    if (!results) return null;
    
    return results.map(res => {
      // Check if we have a hardcoded translation for this standard
      const standardBaseId = res.id.split('(')[0].trim().toUpperCase();
      const translation = t.results.find(tr => tr.id.toUpperCase().includes(standardBaseId));
      
      if (translation) {
        return {
          ...res,
          title: translation.title,
          category: translation.category,
          summary: translation.summary,
          rationale: translation.rationale,
          entities: translation.entities || []
        };
      }
      
      // Otherwise, return the result as is (which might already be translated by the API)
      return res;
    });
  }, [results, lang, t]);

  const handleSearch = async (query) => {
    setIsSearching(true);
    setResults(null); // Clear previous results
    const startTime = performance.now();
    
    try {
      const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}&lang=${lang}`);
      if (!response.ok) throw new Error('API request failed');
      
      const data = await response.json();
      
      const endTime = performance.now();
      setLatency(data.latency || ((endTime - startTime) / 1000).toFixed(1));
      
      setResults(data.results);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
      setLatency(0);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-surface">
      <Navbar lang={lang} setLang={setLang} />
      
      <main className="flex-1 max-w-[1280px] w-full mx-auto px-lg py-xl">
        {!setupComplete ? (
          <div className="flex items-center justify-center min-h-[60vh]">
            <SetupProgress onComplete={() => setSetupComplete(true)} />
          </div>
        ) : (
          <div className="space-y-xl animate-in fade-in duration-500">
            <header className="mb-xl">
              <h1 className="text-on-surface mb-sm tracking-tight">{t.title}</h1>
              <p className="text-on-surface-variant text-lg max-w-3xl">
                {t.subtitle}
              </p>
            </header>

            <MetricsDashboard latency={latency} lang={lang} />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-xl">
              <div className="lg:col-span-2 space-y-lg">
                <SearchPanel onSearch={handleSearch} isSearching={isSearching} lang={lang} />
                
                {localizedResults && (
                  <div className="space-y-md mt-xl animate-in slide-in-from-bottom-4 duration-500">
                    <h3 className="text-on-surface font-semibold flex items-center gap-sm">
                      {t.identifiedStandards}
                      <span className="chip-status bg-primary/10 text-primary border border-primary/20">
                        {localizedResults.length} {t.found}
                      </span>
                    </h3>
                    {localizedResults.map((result, i) => (
                      <ResultCard key={i} result={result} lang={lang} />
                    ))}
                  </div>
                )}
              </div>
              
              <div className="lg:col-span-1">
                <PipelineTimeline lang={lang} />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
