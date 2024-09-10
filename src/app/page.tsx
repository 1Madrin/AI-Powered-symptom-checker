"use client"
import React, { useState, FormEvent } from 'react';
import axios from 'axios';

interface Prediction {
  disease: string;
  probability: string;
}

interface ApiResponse {
  top_prediction: string;
  top_5_predictions: Prediction[];
}

export default function Home() {
  const [symptoms, setSymptoms] = useState<string>('');
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post<ApiResponse>('http://localhost:5000/api/check-symptoms', { symptoms });
      setResult(response.data);
    } catch (error) {
      setError('An error occurred while checking symptoms.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-5 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">AI Symptom Checker</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          placeholder="Enter your symptoms here..."
          rows={5}
          className="w-full p-2 border border-gray-300 rounded mb-2"
        />
        <button
          type="submit"
          disabled={loading}
          className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300"
        >
          {loading ? 'Checking...' : 'Check Symptoms'}
        </button>
      </form>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {result && (
        <div className="result">
          <h2 className="text-2xl font-semibold mb-2">Results:</h2>
          <h3 className="text-xl font-semibold mb-1">Top Prediction:</h3>
          <p className="mb-2">{result.top_prediction}</p>
          <h3 className="text-xl font-semibold mb-1">Top 5 Predictions:</h3>
          <ul className="list-disc pl-5">
            {result.top_5_predictions.map((prediction, index) => (
              <li key={index} className="mb-1">
                {prediction.disease}: {prediction.probability}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
