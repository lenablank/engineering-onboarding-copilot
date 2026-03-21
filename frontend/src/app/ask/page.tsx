'use client';

import { useState } from 'react';

interface AskResponse {
  answer: string;
  confidence: number;
  sources: string[];
  chunks_used: number;
}

interface ErrorState {
  message: string;
  type: 'error' | 'warning';
}

export default function AskPage() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ErrorState | null>(null);
  const [showSources, setShowSources] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!question.trim()) {
      setError({ message: 'Please enter a question', type: 'warning' });
      return;
    }

    if (question.length > 500) {
      setError({ message: 'Question must be 500 characters or less', type: 'warning' });
      return;
    }

    // Reset states
    setError(null);
    setResponse(null);
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP ${res.status}: ${res.statusText}`);
      }

      const data: AskResponse = await res.json();
      setResponse(data);
      
      // Auto-expand sources if confidence is low
      if (data.confidence < 0.6) {
        setShowSources(true);
      }
    } catch (err) {
      console.error('Error asking question:', err);
      setError({
        message: err instanceof Error ? err.message : 'Failed to get answer. Please check if the backend is running.',
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestion('');
    setResponse(null);
    setError(null);
    setShowSources(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-2">
            Engineering Onboarding Copilot
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            Ask questions about engineering processes, tools, and practices
          </p>
        </div>

        {/* Question Input */}
        <form onSubmit={handleSubmit} className="mb-6">
          <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6">
            <label htmlFor="question" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
              Your Question
            </label>
            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="How do I set up my development environment?"
              className="w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-slate-700 dark:text-white resize-none"
              rows={3}
              disabled={loading}
              maxLength={500}
            />
            <div className="flex items-center justify-between mt-3">
              <span className="text-sm text-slate-500 dark:text-slate-400">
                {question.length}/500 characters
              </span>
              <div className="flex gap-2">
                {(question || response) && (
                  <button
                    type="button"
                    onClick={handleClear}
                    disabled={loading}
                    className="px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 bg-slate-200 dark:bg-slate-700 rounded-lg hover:bg-slate-300 dark:hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Clear
                  </button>
                )}
                <button
                  type="submit"
                  disabled={loading || !question.trim()}
                  className="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'Thinking...' : 'Ask'}
                </button>
              </div>
            </div>
          </div>
        </form>

        {/* Loading State */}
        {loading && (
          <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 mb-6">
            <div className="flex items-center gap-3">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
              <p className="text-slate-600 dark:text-slate-400">
                Searching documentation and generating answer...
              </p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className={`rounded-lg shadow-lg p-6 mb-6 ${
            error.type === 'error' 
              ? 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800' 
              : 'bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800'
          }`}>
            <div className="flex items-start gap-3">
              <span className="text-2xl">
                {error.type === 'error' ? '❌' : '⚠️'}
              </span>
              <div>
                <h3 className={`font-semibold mb-1 ${
                  error.type === 'error' 
                    ? 'text-red-800 dark:text-red-400' 
                    : 'text-yellow-800 dark:text-yellow-400'
                }`}>
                  {error.type === 'error' ? 'Error' : 'Warning'}
                </h3>
                <p className={error.type === 'error' 
                  ? 'text-red-700 dark:text-red-300' 
                  : 'text-yellow-700 dark:text-yellow-300'
                }>
                  {error.message}
                </p>
                {error.type === 'error' && (
                  <p className="text-sm text-red-600 dark:text-red-400 mt-2">
                    💡 Tip: Make sure the backend server is running on {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Answer Display */}
        {response && !loading && (
          <div className="space-y-4">
            {/* Main Answer Card */}
            <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6">
              {/* Confidence Badge */}
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white">
                  Answer
                </h2>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    Confidence:
                  </span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    response.confidence >= 0.7 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                      : response.confidence >= 0.5
                      ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                      : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                  }`}>
                    {(response.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              {/* Answer Text */}
              <div className="prose dark:prose-invert max-w-none">
                <p className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
                  {response.answer}
                </p>
              </div>

              {/* Metadata */}
              <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
                <div className="flex items-center gap-4 text-sm text-slate-600 dark:text-slate-400">
                  <span>📚 {response.chunks_used} chunks retrieved</span>
                  <span>📄 {response.sources.length} source files</span>
                </div>
              </div>
            </div>

            {/* Sources Section */}
            <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg overflow-hidden">
              <button
                onClick={() => setShowSources(!showSources)}
                className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
              >
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                  Source Documents
                </h3>
                <span className="text-slate-600 dark:text-slate-400">
                  {showSources ? '▼' : '▶'}
                </span>
              </button>
              
              {showSources && (
                <div className="px-6 pb-4">
                  <div className="space-y-2">
                    {response.sources.map((source, index) => {
                      const filename = source.split('/').pop() || source;
                      return (
                        <div
                          key={index}
                          className="px-4 py-3 bg-slate-50 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600"
                        >
                          <div className="flex items-center gap-2">
                            <span className="text-blue-600 dark:text-blue-400 font-mono text-sm">
                              #{index + 1}
                            </span>
                            <code className="text-sm text-slate-700 dark:text-slate-300 break-all">
                              {filename}
                            </code>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  {response.confidence < 0.6 && (
                    <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                      <p className="text-sm text-yellow-800 dark:text-yellow-400">
                        ℹ️ Low confidence score. The answer may not be fully accurate. Consider rephrasing your question or checking the source documents.
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Help Text */}
        {!response && !loading && !error && (
          <div className="text-center text-slate-500 dark:text-slate-400 mt-12">
            <p className="text-lg mb-4">👋 Welcome!</p>
            <p className="text-sm">
              Ask any question about engineering processes, tools, or practices.
              <br />
              The system will search through documentation and provide answers with sources.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
