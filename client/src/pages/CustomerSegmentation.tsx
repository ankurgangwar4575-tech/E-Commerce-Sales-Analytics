import React, { useState } from 'react';
import { Users, AlertCircle, Sparkles } from 'lucide-react';
import { API_URL } from '../config';

export const CustomerSegmentation = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ cluster_id: number; profile: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    total_orders: '5',
    total_spend: '1500.00',
    return_rate: '0.1',
    customer_age: '35',
    customer_acquisition_cost: '20.00'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      total_orders: parseInt(formData.total_orders),
      total_spend: parseFloat(formData.total_spend),
      return_rate: parseFloat(formData.return_rate),
      customer_age: parseInt(formData.customer_age),
      customer_acquisition_cost: parseFloat(formData.customer_acquisition_cost)
    };

    try {
      const response = await fetch(`${API_URL}/segment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('Failed to fetch segmentation');
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Customer Segmentation</h1>
        <p className="text-zinc-400">Classify customers using our K-Means clustering model.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="text-xl font-semibold mb-6 text-indigo-400">Customer Features</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            
            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Total Orders</label>
              <input 
                type="number" 
                name="total_orders"
                value={formData.total_orders}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Total Lifetime Spend ($)</label>
              <input 
                type="number" 
                name="total_spend"
                value={formData.total_spend}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Return Rate (0-1)</label>
              <input 
                type="number" 
                step="0.01"
                name="return_rate"
                value={formData.return_rate}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Customer Age</label>
              <input 
                type="number" 
                name="customer_age"
                value={formData.customer_age}
                onChange={handleChange}
                className="input-field"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Acquisition Cost ($)</label>
              <input 
                type="number" 
                name="customer_acquisition_cost"
                value={formData.customer_acquisition_cost}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full mt-6 btn-primary py-3"
            >
              {loading ? 'Clustering...' : 'Segment Customer'}
            </button>
          </form>
        </div>

        <div className="card flex flex-col justify-center items-center text-center">
          {!result && !error && !loading && (
             <div className="text-zinc-500">
               <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
               <p>Enter features to determine customer segment</p>
             </div>
          )}

          {loading && (
            <div className="animate-pulse flex flex-col items-center">
              <div className="w-12 h-12 border-4 border-accent-teal border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-zinc-300">Running K-Means Model...</p>
            </div>
          )}

          {error && (
            <div className="text-red-400 flex flex-col items-center">
              <AlertCircle className="w-12 h-12 mb-2" />
              <p>{error}</p>
            </div>
          )}

          {result && !loading && (
            <div className="w-full">
              <div className="p-6 rounded-xl border bg-accent-teal/10 border-accent-teal/50">
                <Sparkles className="w-12 h-12 text-indigo-400 mx-auto mb-4" />
                <h3 className="text-2xl font-bold mb-1 text-indigo-400">
                  Cluster {result.cluster_id}
                </h3>
                <p className="text-zinc-300 mb-6">Profile Assigned</p>
                
                <div className="bg-zinc-950/50 rounded-lg p-4">
                  <p className="text-sm text-zinc-400 mb-1">Customer Profile</p>
                  <p className="text-xl font-bold text-white">
                    {result.profile}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
