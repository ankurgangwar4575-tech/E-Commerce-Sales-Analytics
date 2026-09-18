import React, { useState } from 'react';
import { HelpCircle, Users, DollarSign, Truck, Percent } from 'lucide-react';
import { API_URL } from '../config';

export const ReturnReason = () => {
  const [formData, setFormData] = useState({
    customer_segment: 'Consumer',
    shipping_method: 'Standard',
    customer_age: 35,
    gross_sales: 150,
    discount_amount: 10
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ predicted_reason: string, probabilities: any[] } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/predict-return-reason`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) throw new Error('Prediction failed');
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'customer_segment' || name === 'shipping_method' ? value : parseFloat(value) || 0
    }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-indigo-400 flex items-center gap-2">
          <HelpCircle className="w-8 h-8" />
          Return Reason Predictor
        </h2>
        <p className="text-zinc-400 mt-2">
          Predict the primary reason a customer might return an order.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <form onSubmit={handleSubmit} className="card space-y-6">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white mb-4">Order Details</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Customer Segment</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Users className="h-5 w-5 text-zinc-500" />
                  </div>
                  <select
                    name="customer_segment"
                    value={formData.customer_segment}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                  >
                    <option value="Consumer">Consumer</option>
                    <option value="Premium">Premium</option>
                    <option value="VIP">VIP</option>
                    <option value="Business">Business</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Shipping Method</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Truck className="h-5 w-5 text-zinc-500" />
                  </div>
                  <select
                    name="shipping_method"
                    value={formData.shipping_method}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                  >
                    <option value="Standard">Standard</option>
                    <option value="Express">Express</option>
                    <option value="Same-Day">Same-Day</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Customer Age</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Users className="h-5 w-5 text-zinc-500" />
                  </div>
                  <input
                    type="number"
                    name="customer_age"
                    value={formData.customer_age}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Gross Sales ($)</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <DollarSign className="h-5 w-5 text-zinc-500" />
                  </div>
                  <input
                    type="number"
                    name="gross_sales"
                    value={formData.gross_sales}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Discount Amount ($)</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Percent className="h-5 w-5 text-zinc-500" />
                  </div>
                  <input
                    type="number"
                    name="discount_amount"
                    value={formData.discount_amount}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                    required
                  />
                </div>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary flex items-center justify-center gap-2 py-3"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
            ) : (
              <HelpCircle className="w-5 h-5" />
            )}
            {loading ? 'Analyzing...' : 'Predict Return Reason'}
          </button>
        </form>

        <div className="space-y-6">
          <div className="card h-full flex flex-col items-center justify-center min-h-[300px]">
            {result ? (
              <div className="w-full animate-in fade-in zoom-in duration-300">
                <div className="text-center mb-6">
                  <h3 className="text-xl font-medium text-zinc-400 mb-2">Most Likely Reason</h3>
                  <div className="text-3xl font-bold text-white tracking-tight">
                    {result.predicted_reason}
                  </div>
                </div>
                
                <div className="space-y-4 mt-8 w-full">
                  {result.probabilities.slice(0, 5).map((prob, idx) => (
                    <div key={idx} className="relative">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-zinc-300 font-medium truncate pr-4">{prob.reason}</span>
                        <span className="text-zinc-400">{(prob.probability * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-2 bg-zinc-950/50 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full transition-all duration-1000 ${idx === 0 ? 'bg-red-500' : 'bg-slate-600'}`}
                          style={{ width: `${prob.probability * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center text-zinc-500">
                <HelpCircle className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>Enter order details to predict</p>
                <p>the reason it might be returned.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
