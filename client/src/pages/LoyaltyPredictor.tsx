import React, { useState } from 'react';
import { Award, DollarSign, Percent, ShoppingCart, Users, CreditCard } from 'lucide-react';
import { API_URL } from '../config';

export const LoyaltyPredictor = () => {
  const [formData, setFormData] = useState(() => {
    const segments = ['New', 'Loyal', 'At Risk'];
    const payments = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'];
    return {
      customer_segment: segments[Math.floor(Math.random() * segments.length)],
      payment_method: payments[Math.floor(Math.random() * payments.length)],
      gross_sales: parseFloat((Math.random() * 500 + 50).toFixed(2)),
      discount_amount: parseFloat((Math.random() * 50).toFixed(2)),
      quantity: Math.floor(Math.random() * 5) + 1
    };
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ predicted_points: number } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/predict-loyalty`, {
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
      [name]: (name === 'customer_segment' || name === 'payment_method') ? value : parseFloat(value) || 0
    }));
  };

  return (
    <div className="space-y-6">
      <div className="animate-in fade-in zoom-in duration-500">
        <h2 className="text-3xl font-bold text-indigo-400 flex items-center gap-2 tracking-tight">
          <Award className="w-8 h-8" />
          Loyalty Point Predictor
        </h2>
        <p className="text-zinc-400 mt-2">
          Predict exactly how many loyalty points a customer will earn on a transaction.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <form onSubmit={handleSubmit} className="card space-y-6 flex flex-col relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>

          <div className="space-y-4 relative z-10">
            <h3 className="text-xl font-semibold text-zinc-100 mb-4 tracking-tight">Cart & Customer Details</h3>

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
                    <option value="New">New</option>
                    <option value="Loyal">Loyal</option>
                    <option value="At Risk">At Risk</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Payment Method</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <CreditCard className="h-5 w-5 text-zinc-500" />
                  </div>
                  <select
                    name="payment_method"
                    value={formData.payment_method}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                  >
                    <option value="Credit Card">Credit Card</option>
                    <option value="Debit Card">Debit Card</option>
                    <option value="PayPal">PayPal</option>
                    <option value="Bank Transfer">Bank Transfer</option>
                  </select>
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

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-zinc-400 mb-1">Item Quantity</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <ShoppingCart className="h-5 w-5 text-zinc-500" />
                  </div>
                  <input
                    type="number"
                    name="quantity"
                    value={formData.quantity}
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
            className="w-full btn-primary py-3 flex items-center justify-center gap-2 mt-auto relative z-10"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-zinc-900/20 border-t-zinc-900 rounded-full animate-spin" />
            ) : (
              <Award className="w-5 h-5" />
            )}
            {loading ? 'Analyzing Cart...' : 'Predict Points Earned'}
          </button>
        </form>

        <div className="space-y-6">
          <div className="card h-full flex flex-col items-center justify-center min-h-[300px] relative overflow-hidden">
            {result ? (
              <div className="w-full animate-in fade-in zoom-in duration-500">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

                <div className="text-center flex flex-col items-center relative z-10">
                  <div className="mb-4 p-6 bg-indigo-500/10 rounded-full text-indigo-400 shadow-[0_0_30px_rgba(99,102,241,0.2)]">
                    <Award className="w-16 h-16" />
                  </div>
                  <h3 className="text-xl font-medium text-zinc-400 mb-2">Predicted Loyalty Points</h3>
                  <div className="text-6xl font-bold tracking-tight text-white mb-2">
                    {Math.round(result.predicted_points).toLocaleString('en-US')}
                  </div>
                  <p className="text-sm text-indigo-400/80 font-medium">Points Earned on this Order</p>
                </div>
              </div>
            ) : (
              <div className="text-center text-zinc-500 animate-in fade-in duration-500">
                <Award className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>Enter cart and customer details</p>
                <p>to predict loyalty points earned.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
