import React, { useState } from 'react';
import { MessageSquare, Package, Clock, RotateCcw, DollarSign, Percent, Smile, Frown, Meh } from 'lucide-react';
import { API_URL } from '../config';

export const ReviewSentiment = () => {
  const [formData, setFormData] = useState(() => {
    const statuses = ['Delivered', 'Processing', 'Shipped', 'Cancelled'];
    const returns = ['Not Returned', 'Returned'];
    const delDays = Math.floor(Math.random() * 10) + 1;
    return {
      order_status: statuses[Math.floor(Math.random() * statuses.length)],
      return_status: returns[Math.floor(Math.random() * returns.length)],
      delivery_days: delDays,
      estimated_delivery_days: delDays + Math.floor(Math.random() * 4) - 1,
      discount_amount: parseFloat((Math.random() * 50).toFixed(2)),
      gross_sales: parseFloat((Math.random() * 500 + 50).toFixed(2))
    };
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ predicted_sentiment: string, probabilities: any[] } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/predict-sentiment`, {
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
      [name]: (name === 'order_status' || name === 'return_status') ? value : parseFloat(value) || 0
    }));
  };

  const getSentimentIcon = (sentiment: string, className: string) => {
    switch (sentiment) {
      case 'Positive': return <Smile className={className} />;
      case 'Negative': return <Frown className={className} />;
      default: return <Meh className={className} />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'Positive': return 'text-emerald-500';
      case 'Negative': return 'text-red-500';
      default: return 'text-yellow-500';
    }
  };

  const getSentimentBg = (sentiment: string) => {
    switch (sentiment) {
      case 'Positive': return 'bg-emerald-500';
      case 'Negative': return 'bg-red-500';
      default: return 'bg-yellow-500';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-indigo-400 flex items-center gap-2">
          <MessageSquare className="w-8 h-8" />
          Review Sentiment Analyzer
        </h2>
        <p className="text-zinc-400 mt-2">
          Predict the sentiment of a customer's review based on their order experience.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <form onSubmit={handleSubmit} className="card space-y-6">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white mb-4">Order Experience</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Order Status</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Package className="h-5 w-5 text-zinc-500" />
                  </div>
                  <select
                    name="order_status"
                    value={formData.order_status}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                  >
                    <option value="Delivered">Delivered</option>
                    <option value="Shipped">Shipped</option>
                    <option value="Processing">Processing</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Return Status</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <RotateCcw className="h-5 w-5 text-zinc-500" />
                  </div>
                  <select
                    name="return_status"
                    value={formData.return_status}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                  >
                    <option value="Not Returned">Not Returned</option>
                    <option value="Returned">Returned</option>
                    <option value="Pending">Pending</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Actual Delivery Days</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Clock className="h-5 w-5 text-zinc-500" />
                  </div>
                  <input
                    type="number"
                    name="delivery_days"
                    value={formData.delivery_days}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Estimated Delivery Days</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Clock className="h-5 w-5 text-zinc-500" />
                  </div>
                  <input
                    type="number"
                    name="estimated_delivery_days"
                    value={formData.estimated_delivery_days}
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
              <MessageSquare className="w-5 h-5" />
            )}
            {loading ? 'Analyzing...' : 'Predict Sentiment'}
          </button>
        </form>

        <div className="space-y-6">
          <div className="card h-full flex flex-col items-center justify-center min-h-[300px]">
            {result ? (
              <div className="w-full animate-in fade-in zoom-in duration-300">
                <div className="text-center mb-8 flex flex-col items-center">
                  <div className={`mb-4 ${getSentimentColor(result.predicted_sentiment)}`}>
                    {getSentimentIcon(result.predicted_sentiment, "w-24 h-24")}
                  </div>
                  <h3 className="text-xl font-medium text-zinc-400 mb-2">Predicted Sentiment</h3>
                  <div className={`text-3xl font-bold tracking-tight ${getSentimentColor(result.predicted_sentiment)}`}>
                    {result.predicted_sentiment}
                  </div>
                </div>
                
                <div className="space-y-4 mt-8 w-full">
                  {result.probabilities.map((prob, idx) => (
                    <div key={idx} className="relative">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-zinc-300 font-medium truncate pr-4 flex items-center gap-2">
                          {getSentimentIcon(prob.sentiment, "w-4 h-4")}
                          {prob.sentiment}
                        </span>
                        <span className="text-zinc-400">{(prob.probability * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-2 bg-zinc-950/50 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full transition-all duration-1000 ${getSentimentBg(prob.sentiment)} opacity-80`}
                          style={{ width: `${prob.probability * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center text-zinc-500">
                <MessageSquare className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>Enter order details to predict</p>
                <p>the customer's review sentiment.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
