import { useState } from 'react';
import { Star, Truck, Calendar, DollarSign, Percent } from 'lucide-react';
import { API_URL } from '../config';

export const RatingPrediction = () => {
  const [formData, setFormData] = useState({
    delivery_days: 3,
    estimated_delivery_days: 4,
    discount_amount: 10,
    shipping_cost: 5,
    gross_sales: 150
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<number | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/rating`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) throw new Error('Prediction failed');
      
      const data = await response.json();
      setResult(data.predicted_rating);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-accent-teal flex items-center gap-2">
          <Star className="w-8 h-8" />
          Customer Rating Prediction
        </h2>
        <p className="text-slate-400 mt-2">
          Predict the star rating a customer will give based on order fulfillment details.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <form onSubmit={handleSubmit} className="card space-y-6">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white mb-4">Order Details</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Actual Delivery Days</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Truck className="h-5 w-5 text-slate-500" />
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
                <label className="block text-sm font-medium text-slate-400 mb-1">Estimated Delivery Days</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Calendar className="h-5 w-5 text-slate-500" />
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
                <label className="block text-sm font-medium text-slate-400 mb-1">Gross Sales ($)</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <DollarSign className="h-5 w-5 text-slate-500" />
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
                <label className="block text-sm font-medium text-slate-400 mb-1">Discount Amount ($)</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Percent className="h-5 w-5 text-slate-500" />
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
                <label className="block text-sm font-medium text-slate-400 mb-1">Shipping Cost ($)</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <DollarSign className="h-5 w-5 text-slate-500" />
                  </div>
                  <input
                    type="number"
                    name="shipping_cost"
                    value={formData.shipping_cost}
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
              <Star className="w-5 h-5" />
            )}
            {loading ? 'Analyzing...' : 'Predict Customer Rating'}
          </button>
        </form>

        <div className="space-y-6">
          <div className="card h-full flex flex-col items-center justify-center min-h-[300px]">
            {result !== null ? (
              <div className="text-center animate-in fade-in zoom-in duration-300">
                <div className="w-24 h-24 rounded-full bg-accent-teal/10 flex items-center justify-center mx-auto mb-6">
                  <Star className="w-12 h-12 text-accent-teal fill-accent-teal" />
                </div>
                <h3 className="text-xl font-medium text-slate-400 mb-2">Predicted Rating</h3>
                <div className="text-5xl font-bold text-white mb-2">
                  {result.toFixed(1)} <span className="text-2xl text-slate-400">/ 5.0</span>
                </div>
                <div className="flex justify-center gap-1 mt-4">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                      key={star}
                      className={`w-8 h-8 ${
                        star <= Math.round(result)
                          ? 'text-accent-teal fill-accent-teal'
                          : 'text-navy-700 fill-navy-700'
                      } transition-all duration-500`}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center text-slate-500">
                <Star className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>Enter order details to predict</p>
                <p>the customer's star rating.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
