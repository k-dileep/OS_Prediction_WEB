'use client';

import { useState, useEffect } from 'react';

export default function PredictionForm() {
    const [radiation, setRadiation] = useState('');
    const [fibrinogen, setFibrinogen] = useState('');
    const [result, setResult] = useState<{
        predicted_sod: number;
        status: string;
        threshold: number;
    } | null>(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [apiUrl, setApiUrl] = useState('');

    useEffect(() => {
        // Set the API URL based on environment or default to localhost for development
        setApiUrl(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000');
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch(`${apiUrl}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    radiation: parseFloat(radiation),
                    fibrinogen: parseFloat(fibrinogen),
                }),
            });

            const data = await response.json();
            if (data.success) {
                setResult(data);
            } else {
                setError(data.error || 'Prediction failed');
            }
        } catch (err) {
            setError('Failed to get prediction. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-md mx-auto p-4 sm:p-6 bg-white rounded-lg shadow-lg">
            <h2 className="text-xl sm:text-2xl text-blue-600 font-bold mb-4 sm:mb-6 text-center">Oxidative Stress Prediction</h2>
            
            <form onSubmit={handleSubmit} className="space-y-3 sm:space-y-4">
                <div>
                    <label htmlFor="radiation" className="block text-sm font-medium text-gray-900">
                        Radiation Level
                    </label>
                    <input
                        type="number"
                        id="radiation"
                        value={radiation}
                        onChange={(e) => setRadiation(e.target.value)}
                        className="mt-1 pl-1 text-gray-900 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        required
                        step="any"
                        placeholder="Enter radiation level"
                        suppressHydrationWarning
                    />
                </div>

                <div>
                    <label htmlFor="fibrinogen" className="block text-sm font-medium text-gray-700">
                        Fibrinogen Level
                    </label>
                    <input
                        type="number"
                        id="fibrinogen"
                        value={fibrinogen}
                        onChange={(e) => setFibrinogen(e.target.value)}
                        className="mt-1 pl-1 text-gray-900 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        required
                        step="any"
                        placeholder="Enter fibrinogen level"
                        suppressHydrationWarning
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors duration-200"
                    suppressHydrationWarning
                >
                    {loading ? 'Predicting...' : 'Predict'}
                </button>
            </form>

            {error && (
                <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md text-sm">
                    {error}
                </div>
            )}

            {result && (
                <div className="mt-4 sm:mt-6 p-3 sm:p-4 bg-gray-50 rounded-md">
                    <h3 className="text-base sm:text-lg text-gray-900 font-semibold mb-2">Results:</h3>
                    <div className="space-y-2">
                        <p className="text-sm sm:text-base">
                            <span className="font-medium text-gray-900">SOD Activity:</span>{' '}
                            <span className="text-black">{result.predicted_sod.toFixed(2)}</span>
                        </p>
                        <p className="text-sm sm:text-base">
                            <span className="font-medium text-gray-900">Status:</span>{' '}
                            <span className={result.status.includes('Exposed') ? 'text-red-600' : 'text-green-600'}>
                                {result.status}
                            </span>
                        </p>
                        <p className="text-xs sm:text-sm text-gray-600">
                            Threshold: {result.threshold}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
} 