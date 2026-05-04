import React, { useState } from 'react';
import { Search, Loader2, Sparkles } from 'lucide-react';
import { translations } from '../utils/translations';

export default function SearchPanel({ onSearch, isSearching, lang }) {
  const [query, setQuery] = useState('');
  const t = translations[lang];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query) return;
    onSearch(query);
  };

  return (
    <div className="card p-xl relative overflow-hidden group">
      {/* Subtle background glow */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-primary rounded-full opacity-5 blur-[100px] pointer-events-none group-hover:opacity-10 transition-opacity"></div>
      
      <div className="relative z-10">
        <h2 className="text-on-surface mb-sm flex items-center gap-sm">
          <Sparkles className="w-6 h-6 text-tertiary" />
          {t.searchTitle || "Semantic Standard Search"}
        </h2>
        <p className="text-on-surface-variant mb-lg max-w-2xl">
          {t.searchDescription || "Enter a product description, use case, or technical query. The AI will traverse the vector space to identify the most relevant BIS standards."}
        </p>

        <form onSubmit={handleSubmit} className="flex gap-md">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-md flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-outline" />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="input-field pl-[3rem] py-md text-lg bg-surface-container border-surface-container-highest focus:border-primary focus:ring-1 focus:ring-primary focus:bg-surface-container-lowest"
              placeholder={t.searchPlaceholder}
            />
          </div>
          <button 
            type="submit" 
            disabled={isSearching}
            className="btn-primary flex items-center gap-sm whitespace-nowrap min-w-[140px] justify-center"
          >
            {isSearching ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                {t.analyzing || "Analyzing"}
              </>
            ) : (
              <>
                {t.search}
              </>
            )}
          </button>
        </form>
        
        <div className="mt-md flex gap-sm items-center">
          <span className="font-mono text-xs text-outline-variant uppercase tracking-wider">{t.exampleQueries || "Example queries:"}</span>
          <button onClick={() => setQuery('Water purifiers for domestic use')} className="chip-status bg-surface-bright text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest transition-colors cursor-pointer border border-surface-container-highest">Water Purifiers</button>
          <button onClick={() => setQuery('Concrete testing methods')} className="chip-status bg-surface-bright text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest transition-colors cursor-pointer border border-surface-container-highest">Concrete Testing</button>
        </div>
      </div>
    </div>
  );
}
