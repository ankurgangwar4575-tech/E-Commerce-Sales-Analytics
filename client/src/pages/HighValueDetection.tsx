import React, { useState } from 'react';
import { Gem, AlertCircle, Trophy } from 'lucide-react';
import { API_URL } from '../config';

export const HighValueDetection = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ high_value_probability: number; is_high_value: boolean } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    customer_age: '28',
    customer_acquisition_cost: '15.00',
    first_order_value: '120.00',
    first_order_discount: '10.00',
    first_order_quantity: '2',
    gender: 'F',
    first_order_channel: 'Online'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      customer_age: parseInt(formData.customer_age),
      customer_acquisition_cost: parseFloat(formData.customer_acquisition_cost),
      first_order_value: parseFloat(formData.first_order_value),
      first_order_discount: parseFloat(formData.first_order_discount),
      first_order_quantity: parseInt(formData.first_order_quantity),
      gender: formData.gender,
      first_order_channel: formData.first_order_channel
    };

    try {
      const response = await fetch(`${API_URL}/high-value`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('Failed to fetch prediction');
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
        <h1 className="text-3xl font-bold mb-2">High-Value Customer Detection</h1>
        <p className="text-zinc-400">Predict if a customer will become a top-tier spender based on their first order.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="text-xl font-semibold mb-6 text-indigo-400">New Customer Data</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-1">Age</label>
                <input 
                  type="number" 
                  name="customer_age"
                  value={formData.customer_age}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-300 mb-1">Gender</label>
                <select 
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Acquisition Cost ($)</label>
              <input 
                type="number" 
                step="0.01"
                name="customer_acquisition_cost"
                value={formData.customer_acquisition_cost}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div className="pt-4 border-t border-zinc-800">
              <h3 className="text-sm font-bold text-zinc-400 mb-4 uppercase">First Order Details</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-1">Order Value ($)</label>
                  <input 
                    type="number" 
                    step="0.01"
                    name="first_order_value"
                    value={formData.first_order_value}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-1">Discount Given ($)</label>
                    <input 
                      type="number" 
                      step="0.01"
                      name="first_order_discount"
                      value={formData.first_order_discount}
                      onChange={handleChange}
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-zinc-300 mb-1">Total Quantity</label>
                    <input 
                      type="number" 
                      name="first_order_quantity"
                      value={formData.first_order_quantity}
                      onChange={handleChange}
                      className="input-field"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-zinc-300 mb-1">Sales Channel</label>
                  <select 
                    name="first_order_channel"
                    value={formData.first_order_channel}
                    onChange={handleChange}
                    className="input-field"
                  >
                    <option value="Online">Online</option>
                    <option value="In-Store">In-Store</option>
                    <option value="App">Mobile App</option>
                  </select>
                </div>
              </div>
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full mt-6 btn-primary py-3"
            >
              {loading ? 'Analyzing...' : 'Predict VIP Status'}
            </button>
          </form>
        </div>

        <div className="card flex flex-col items-center justify-center h-full">
          {!result && !error && !loading && (
             <div className="text-zinc-500 text-center flex flex-col items-center">
               <Gem className="w-16 h-16 mx-auto mb-4 opacity-50" />
               <p>Enter first-order features to predict LTV potential</p>
             </div>
          )}

          {loading && (
            <div className="animate-pulse flex flex-col items-center">
              <div className="w-12 h-12 border-4 border-accent-teal border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-zinc-300">Running LightGBM Model...</p>
            </div>
          )}

          {error && (
            <div className="text-red-400 flex flex-col items-center">
              <AlertCircle className="w-12 h-12 mb-2" />
              <p>{error}</p>
            </div>
          )}

          {result && !loading && (
            <div className="w-full space-y-6">
              <div className={`p-6 rounded-xl border ${result.is_high_value ? 'bg-yellow-500/10 border-yellow-500/50' : 'bg-slate-700/30 border-slate-600'}`}>
                {result.is_high_value ? (
                  <Trophy className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
                ) : (
                  <Gem className="w-16 h-16 text-zinc-400 mx-auto mb-4" />
                )}
                
                <h3 className={`text-2xl font-bold mb-1 ${result.is_high_value ? 'text-yellow-500' : 'text-zinc-300'}`}>
                  {result.is_high_value ? 'Likely VIP' : 'Standard LTV'}
                </h3>
                <p className="text-zinc-400">Prediction Result</p>
              </div>

              <div className="bg-zinc-950/50 rounded-xl p-6">
                <div className="flex justify-between items-end mb-2">
                  <span className="text-sm text-zinc-400">Probability Score</span>
                  <span className="text-xl font-bold text-indigo-400">
                    {(result.high_value_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-zinc-900/50 rounded-full h-3">
                  <div 
                    className="bg-accent-teal h-3 rounded-full transition-all duration-1000" 
                    style={{ width: `${result.high_value_probability * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
