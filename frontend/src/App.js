import React, { useState } from 'react';
import LoadingSpinner from './components/LoadingSpinner';
import ResultsDisplay from './components/ResultsDisplay';
import ErrorMessage from './components/ErrorMessage';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const analyzeArticle = async () => {
    if (!url.trim()) {
      setError('Please enter a valid URL');
      return;
    }

    // Basic URL validation
    try {
      new URL(url);
    } catch {
      setError('Please enter a valid URL (include http:// or https://)');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP ${response.status}: Request failed`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error('Analysis error:', err);
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        setError('Unable to connect to NewsCheckr API. Please ensure the backend is running on http://localhost:5001');
      } else {
        setError(err.message || 'An unexpected error occurred while analyzing the article');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    analyzeArticle();
  };

  const clearResults = () => {
    setResults(null);
    setError(null);
    setUrl('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            NewsCheckr
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered news analysis tool that evaluates credibility and political bias of news articles
          </p>
        </header>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {/* Input Form */}
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                  News Article URL
                </label>
                <input
                  id="url"
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com/news-article"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors"
                  disabled={loading}
                />
              </div>
              
              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={loading || !url.trim()}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center"
                >
                  {loading ? (
                    <>
                      <LoadingSpinner size="sm" className="mr-2" />
                      Analyzing...
                    </>
                  ) : (
                    'Analyze'
                  )}
                </button>
                
                {(results || error) && (
                  <button
                    type="button"
                    onClick={clearResults}
                    className="px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors duration-200"
                  >
                    Clear
                  </button>
                )}
              </div>
            </form>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex flex-col items-center justify-center text-center">
                <LoadingSpinner size="lg" className="mb-4" />
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                  Analyzing Article
                </h3>
                <p className="text-gray-500">
                  Scraping content, analyzing credibility, detecting bias, and generating summary...
                </p>
              </div>
            </div>
          )}

          {/* Error State */}
          {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

          {/* Results */}
          {results && <ResultsDisplay results={results} />}

          {/* Sample URLs for Testing */}
          {!loading && !results && !error && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-4">
                Try these sample URLs:
              </h3>
              <div className="space-y-2">
                {[
                  'https://www.reuters.com/business/',
                  'https://www.bbc.com/news',
                  'https://apnews.com/',
                ].map((sampleUrl, index) => (
                  <button
                    key={index}
                    onClick={() => setUrl(sampleUrl)}
                    className="block w-full text-left px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200"
                  >
                    {sampleUrl}
                  </button>
                ))}
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Note: Make sure the NewsCheckr API is running on localhost:5001
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="text-center mt-16 text-gray-500">
          <p>&copy; 2023 NewsCheckr. Built with React and Tailwind CSS.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;