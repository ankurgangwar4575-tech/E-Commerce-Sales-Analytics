import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  RotateCcw, Users, Gem, TrendingUp, Star, DollarSign, Target, Truck, HelpCircle, MessageSquare,
  DollarSign as RevenueIcon, ShoppingCart, Percent
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { API_URL } from '../config';

const mlFeatures = [
  { path: '/return-prediction', title: 'Return Prediction', desc: 'Predict the exact probability of an order being returned.', icon: RotateCcw, active: true },
  { path: '/customer-segmentation', title: 'Customer Segmentation', desc: 'Use behavioral features to discover customer groups using KMeans.', icon: Users, active: true },
  { path: '/segment-classification', title: 'Segment Predictor', desc: 'Predict whether a customer is Consumer, Premium, VIP, or Business.', icon: Target, active: true },
  { path: '/delivery-delay', title: 'Delivery Delay Warning', desc: 'Predict if an order will be delivered later than its estimated delivery date.', icon: Truck, active: true },
  { path: '/return-reason', title: 'Return Reason Predictor', desc: 'Predict the primary reason a customer might return an order.', icon: HelpCircle, active: true },
  { path: '/review-sentiment', title: 'Review Sentiment Analyzer', desc: 'Predict the sentiment of a customer\'s review based on their order experience.', icon: MessageSquare, active: true },
  { path: '/high-value-customer', title: 'High-Value Customer Detection', desc: 'Identify customers with higher historical business value.', icon: Gem, active: true },
  { path: '/sales-forecasting', title: 'Sales Forecasting', desc: 'Use historical transaction patterns for time-series and forecasting experiments.', icon: TrendingUp, active: true },
  { path: '/rating-prediction', title: 'Customer Rating Prediction', desc: 'Explore which variables may help explain customer ratings.', icon: Star, active: true },
];

// Mock data for the chart since the backend only provides aggregates right now
const revenueData = [
  { name: 'Jan', revenue: 4000, returns: 240 },
  { name: 'Feb', revenue: 3000, returns: 139 },
  { name: 'Mar', revenue: 2000, returns: 980 },
  { name: 'Apr', revenue: 2780, returns: 390 },
  { name: 'May', revenue: 1890, returns: 480 },
  { name: 'Jun', revenue: 2390, returns: 380 },
  { name: 'Jul', revenue: 3490, returns: 430 },
];

export const Dashboard = () => {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_URL}/stats`)
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("Failed to load stats:", err));
  }, []);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="relative">
        <div className="absolute -top-10 -left-10 w-40 h-40 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <h1 className="text-4xl font-bold mb-2 tracking-tight">Dashboard Overview</h1>
        <p className="text-zinc-400">High-level metrics and Machine Learning opportunities.</p>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl">
              <RevenueIcon className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-1">Total Revenue</p>
              <p className="text-2xl font-semibold tracking-tight text-zinc-100">{stats ? stats['Total Revenue'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl">
              <DollarSign className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-1">Total Profit</p>
              <p className="text-2xl font-semibold tracking-tight text-zinc-100">{stats ? stats['Total Profit'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-blue-500/10 text-blue-400 rounded-xl">
              <ShoppingCart className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-1">Transactions</p>
              <p className="text-2xl font-semibold tracking-tight text-zinc-100">{stats ? stats['Total Transactions'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-rose-500/10 text-rose-400 rounded-xl">
              <Percent className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-1">Return Rate</p>
              <p className="text-2xl font-semibold tracking-tight text-zinc-100">{stats ? stats['Return Rate'] : '...'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Chart Row */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-6 text-zinc-100">Revenue vs Returns (YTD)</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={revenueData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
              <XAxis dataKey="name" stroke="#71717a" tickLine={false} axisLine={false} />
              <YAxis stroke="#71717a" tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#f4f4f5', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.5)' }}
                itemStyle={{ color: '#f4f4f5' }}
                cursor={{ fill: '#27272a', opacity: 0.4 }}
              />
              <Bar dataKey="revenue" name="Revenue" fill="#6366f1" radius={[4, 4, 0, 0]} />
              <Bar dataKey="returns" name="Returns" fill="#f43f5e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ML Features Grid */}
      <div className="pt-4">
        <h2 className="text-2xl font-bold mb-6 tracking-tight">Predictive Analytics Modules</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mlFeatures.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <Link 
                key={idx} 
                to={feature.path}
                className="card group flex flex-col h-full hover:border-indigo-500/50 hover:shadow-[0_0_30px_-5px_rgba(99,102,241,0.15)] relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-b from-indigo-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="flex items-center gap-4 mb-4 relative">
                  <div className={`p-3 rounded-xl transition-colors duration-300 ${feature.active ? 'bg-zinc-800 text-indigo-400 group-hover:bg-indigo-500/20 group-hover:text-indigo-300' : 'bg-zinc-900/50 text-zinc-600'}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="font-semibold text-lg text-zinc-200 group-hover:text-indigo-300 transition-colors">{feature.title}</h3>
                </div>
                <p className="text-zinc-500 text-sm flex-1 leading-relaxed relative">{feature.desc}</p>
                {!feature.active && (
                  <div className="mt-4 inline-block px-3 py-1 bg-zinc-800/50 text-xs rounded-full text-zinc-500 self-start border border-zinc-800 relative">
                    Coming Soon
                  </div>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};
