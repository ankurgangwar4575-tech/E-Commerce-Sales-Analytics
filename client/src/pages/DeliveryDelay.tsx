import React, { useState } from 'react';
import { Truck, MapPin, DollarSign, Package, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { API_URL } from '../config';

export const DeliveryDelay = () => {
  const [formData, setFormData] = useState({
    shipping_method: 'Standard',
    warehouse: 'Warehouse A',
    region: 'North America',
    customer_country: 'United States',
    shipping_cost: 15
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ delay_probability: number, is_high_risk: boolean } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/predict-delay`, {
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
      [name]: name === 'shipping_cost' ? parseFloat(value) || 0 : value
    }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-accent-teal flex items-center gap-2">
          <Truck className="w-8 h-8" />
          Delivery Delay Warning
        </h2>
        <p className="text-slate-400 mt-2">
          Predict if an order will be delivered later than its estimated delivery date.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <form onSubmit={handleSubmit} className="card space-y-6">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white mb-4">Logistics Details</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Shipping Method</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Truck className="h-5 w-5 text-slate-500" />
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
                <label className="block text-sm font-medium text-slate-400 mb-1">Warehouse</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Package className="h-5 w-5 text-slate-500" />
                  </div>
                  <select
                    name="warehouse"
                    value={formData.warehouse}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                  >
                    <option value="Warehouse A">Warehouse A</option>
                    <option value="Warehouse B">Warehouse B</option>
                    <option value="Warehouse C">Warehouse C</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Region</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <MapPin className="h-5 w-5 text-slate-500" />
                  </div>
                  <select
                    name="region"
                    value={formData.region}
                    onChange={handleInputChange}
                    className="input-field pl-10"
                  >
                    <option value="North America">North America</option>
                    <option value="Europe">Europe</option>
                    <option value="Asia">Asia</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Destination Country</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <MapPin className="h-5 w-5 text-slate-500" />
                  </div>
                  <input
                    type="text"
                    name="customer_country"
                    value={formData.customer_country}
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
              <Truck className="w-5 h-5" />
            )}
            {loading ? 'Analyzing Logistics...' : 'Predict Delay Risk'}
          </button>
        </form>

        <div className="space-y-6">
          <div className="card h-full flex flex-col items-center justify-center min-h-[300px]">
            {result ? (
              <div className="text-center animate-in fade-in zoom-in duration-300">
                <div className="mb-6 relative inline-block">
                  <svg className="w-32 h-32 transform -rotate-90">
                    <circle
                      cx="64"
                      cy="64"
                      r="60"
                      stroke="currentColor"
                      strokeWidth="8"
                      fill="transparent"
                      className="text-navy-700"
                    />
                    <circle
                      cx="64"
                      cy="64"
                      r="60"
                      stroke="currentColor"
                      strokeWidth="8"
                      fill="transparent"
                      strokeDasharray={377}
                      strokeDashoffset={377 - (377 * (result.delay_probability))}
                      className={`${result.is_high_risk ? 'text-red-500' : 'text-emerald-500'} transition-all duration-1000`}
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-3xl font-bold text-white">
                      {(result.delay_probability * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                
                <h3 className="text-xl font-semibold mb-2 text-white">
                  {result.is_high_risk ? 'High Risk of Delay' : 'On-Time Expected'}
                </h3>
                <p className="text-slate-400">
                  {result.is_high_risk 
                    ? "This order is likely to arrive later than the estimated delivery date. Consider expediting."
                    : "This order is expected to arrive on time based on historical logistics."}
                </p>
                
                <div className={`mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-full ${
                  result.is_high_risk ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'
                }`}>
                  {result.is_high_risk ? <AlertTriangle className="w-5 h-5" /> : <CheckCircle2 className="w-5 h-5" />}
                  <span className="font-medium">
                    {result.is_high_risk ? 'Action Recommended' : 'No Action Needed'}
                  </span>
                </div>
              </div>
            ) : (
              <div className="text-center text-slate-500">
                <Truck className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>Enter logistics details to predict</p>
                <p>the risk of a delivery delay.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
