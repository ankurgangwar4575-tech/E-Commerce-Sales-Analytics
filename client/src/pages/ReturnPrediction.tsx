import React, { useState } from 'react';
import { AlertCircle, CheckCircle2, RotateCcw } from 'lucide-react';
import { API_URL } from '../config';

export const ReturnPrediction = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ risk_score: number; is_high_risk: boolean } | null>(null);
  const [error, setError] = useState<string | null>(null);

  // We are creating a simplified form for demo purposes.
  // In a real scenario, this would capture all 50 features or fetch them based on an Order ID.
  const [formData, setFormData] = useState({
    customer_segment: 'Loyal',
    order_amount: '150.00',
    prior_return_rate: '0.1',
    days_since_previous_order: '30',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Build the 50-feature payload. 
    // We send dummy data for the un-captured features to satisfy the backend model.
    const payload = {
      features: {
        "order_month": 12,
        "order_day_of_week": 5,
        "order_hour": 14,
        "order_quarter": 4,
        "sales_channel": "Online",
        "payment_method": "Credit Card",
        "currency": "USD",
        "shipping_method": "Standard",
        "warehouse": "WH-1",
        "marketing_channel": "Organic",
        "campaign_name": "None",
        "coupon_code": "None",
        "prior_order_count": 5,
        "prior_total_spend": 500,
        "prior_total_discount": 50,
        "prior_return_count": 1,
        "prior_average_order_value": 100,
        "prior_return_rate": parseFloat(formData.prior_return_rate),
        "prior_average_discount": 10,
        "days_since_previous_order": parseInt(formData.days_since_previous_order),
        "is_first_order": 0,
        "customer_age": 35,
        "gender": "F",
        "customer_segment": formData.customer_segment,
        "customer_state": "CA",
        "customer_country": "USA",
        "region": "West",
        "customer_acquisition_cost": 15,
        "item_count": 2,
        "unique_product_count": 2,
        "total_quantity": 2,
        "category_count": 1,
        "subcategory_count": 1,
        "brand_count": 1,
        "supplier_count": 1,
        "total_gross_sales": parseFloat(formData.order_amount),
        "total_tax_amount": 10,
        "total_shipping_cost": 5,
        "total_item_net_sales": parseFloat(formData.order_amount) - 10,
        "total_item_product_cost": 80,
        "total_item_profit": 60,
        "minimum_item_unit_price": 50,
        "maximum_item_unit_price": 100,
        "average_item_unit_price": 75,
        "minimum_product_rating": 4.0,
        "maximum_product_rating": 5.0,
        "average_product_rating": 4.5,
        "average_quantity_per_item": 1,
        "order_profit_margin_percentage": 0.4,
        "dominant_product_category": "Electronics"
      }
    };

    try {
      const response = await fetch(`${API_URL}/predict`, {
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
        <h1 className="text-3xl font-bold mb-2">Return Prediction</h1>
        <p className="text-zinc-400">Score an order at placement to determine return likelihood.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Form Card */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-6 text-indigo-400">Order Details</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            
            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Customer Segment</label>
              <select 
                name="customer_segment" 
                value={formData.customer_segment}
                onChange={handleChange}
                className="input-field"
              >
                <option value="New">New</option>
                <option value="Loyal">Loyal</option>
                <option value="At Risk">At Risk</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Order Amount ($)</label>
              <input 
                type="number" 
                name="order_amount"
                value={formData.order_amount}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Prior Return Rate (0-1)</label>
              <input 
                type="number" 
                step="0.01"
                name="prior_return_rate"
                value={formData.prior_return_rate}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1">Days Since Last Order</label>
              <input 
                type="number" 
                name="days_since_previous_order"
                value={formData.days_since_previous_order}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full mt-6 btn-primary py-3"
            >
              {loading ? 'Analyzing Risk...' : 'Predict Return Risk'}
            </button>
          </form>
        </div>

        {/* Results Card */}
        <div className="card flex flex-col justify-center items-center text-center">
          {!result && !error && !loading && (
             <div className="text-zinc-500">
               <RotateCcw className="w-16 h-16 mx-auto mb-4 opacity-50" />
               <p>Enter order details to see prediction</p>
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
              <p className="text-sm mt-2">Make sure the FastAPI server is running!</p>
            </div>
          )}

          {result && !loading && (
            <div className="w-full">
              <div className={`p-6 rounded-xl border ${result.is_high_risk ? 'bg-red-500/10 border-red-500/50' : 'bg-emerald-500/10 border-emerald-500/50'}`}>
                {result.is_high_risk ? (
                  <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
                ) : (
                  <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto mb-4" />
                )}
                <h3 className="text-2xl font-bold mb-1">
                  {result.is_high_risk ? 'High Risk' : 'Low Risk'}
                </h3>
                <p className="text-zinc-300 mb-6">of order being returned</p>
                
                <div className="bg-zinc-950/50 rounded-lg p-4">
                  <p className="text-sm text-zinc-400 mb-1">Risk Probability Score</p>
                  <p className="text-3xl font-mono font-bold text-white">
                    {(result.risk_score * 100).toFixed(1)}%
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
