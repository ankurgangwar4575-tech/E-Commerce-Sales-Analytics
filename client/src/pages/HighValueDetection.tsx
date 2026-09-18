import React, { useState } from 'react';
import { Gem, AlertCircle, Trophy } from 'lucide-react';

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
      const response = await fetch('http://127.0.0.1:8000/high-value', {
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
        <p className="text-slate-400">Predict if a customer will become a top-tier spender based on their first order.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-6 text-accent-teal">New Customer Data</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Age</label>
                <input 
                  type="number" 
                  name="customer_age"
                  value={formData.customer_age}
                  onChange={handleChange}
                  className="w-full bg-navy-900 border border-navy-700 rounded-lg p-2.5 text-white focus:ring-accent-teal focus:border-accent-teal"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Gender</label>
                <select 
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full bg-navy-900 border border-navy-700 rounded-lg p-2.5 text-white focus:ring-accent-teal focus:border-accent-teal"
                >
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Acquisition Cost ($)</label>
              <input 
                type="number" 
                step="0.01"
                name="customer_acquisition_cost"
                value={formData.customer_acquisition_cost}
                onChange={handleChange}
                className="w-full bg-navy-900 border border-navy-700 rounded-lg p-2.5 text-white focus:ring-accent-teal focus:border-accent-teal"
              />
            </div>

            <div className="pt-4 border-t border-navy-700">
              <h3 className="text-sm font-bold text-slate-400 mb-4 uppercase">First Order Details</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Order Value ($)</label>
                  <input 
                    type="number" 
                    step="0.01"
                    name="first_order_value"
                    value={formData.first_order_value}
                    onChange={handleChange}
                    className="w-full bg-navy-900 border border-navy-700 rounded-lg p-2.5 text-white focus:ring-accent-teal focus:border-accent-teal"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">Discount Given ($)</label>
                    <input 
                      type="number" 
                      step="0.01"
                      name="first_order_discount"
                      value={formData.first_order_discount}
                      onChange={handleChange}
                      className="w-full bg-navy-900 border border-navy-700 rounded-lg p-2.5 text-white focus:ring-accent-teal focus:border-accent-teal"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">Total Quantity</label>
                    <input 
                      type="number" 
                      name="first_order_quantity"
                      value={formData.first_order_quantity}
                      onChange={handleChange}
                      className="w-full bg-navy-900 border border-navy-700 rounded-lg p-2.5 text-white focus:ring-accent-teal focus:border-accent-teal"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Sales Channel</label>
                  <select 
                    name="first_order_channel"
                    value={formData.first_order_channel}
                    onChange={handleChange}
                    className="w-full bg-navy-900 border border-navy-700 rounded-lg p-2.5 text-white focus:ring-accent-teal focus:border-accent-teal"
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
              className="w-full mt-6 bg-accent-teal text-navy-900 font-bold py-3 px-4 rounded-lg hover:bg-[#4ddbb8] transition-colors disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Predict VIP Status'}
            </button>
          </form>
        </div>

        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 flex flex-col justify-center items-center text-center">
          {!result && !error && !loading && (
             <div className="text-slate-500">
               <Gem className="w-16 h-16 mx-auto mb-4 opacity-50" />
               <p>Enter first-order features to predict LTV potential</p>
             </div>
          )}

          {loading && (
            <div className="animate-pulse flex flex-col items-center">
              <div className="w-12 h-12 border-4 border-accent-teal border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-slate-300">Running LightGBM Model...</p>
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
                  <Gem className="w-16 h-16 text-slate-400 mx-auto mb-4" />
                )}
                
                <h3 className={`text-2xl font-bold mb-1 ${result.is_high_value ? 'text-yellow-500' : 'text-slate-300'}`}>
                  {result.is_high_value ? 'Likely VIP' : 'Standard LTV'}
                </h3>
                <p className="text-slate-400">Prediction Result</p>
              </div>

              <div className="bg-navy-900 rounded-xl p-6">
                <div className="flex justify-between items-end mb-2">
                  <span className="text-sm text-slate-400">Probability Score</span>
                  <span className="text-xl font-bold text-accent-teal">
                    {(result.high_value_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-navy-800 rounded-full h-3">
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
