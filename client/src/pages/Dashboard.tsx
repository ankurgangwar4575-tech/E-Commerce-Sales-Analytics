import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  RotateCcw, Users, Gem, TrendingUp, Star, DollarSign, Target, HelpCircle, MessageSquare, Award,
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
  { path: '/loyalty-predictor', title: 'Loyalty Point Predictor', desc: 'Predict the number of loyalty points earned on a purchase.', icon: Award, active: true },
  { path: '/return-reason', title: 'Return Reason Predictor', desc: 'Predict the primary reason a customer might return an order.', icon: HelpCircle, active: true },
  { path: '/review-sentiment', title: 'Review Sentiment Analyzer', desc: 'Predict the sentiment of a customer\'s review based on their order experience.', icon: MessageSquare, active: true },
  { path: '/high-value-customer', title: 'High-Value Customer Detection', desc: 'Identify customers with higher historical business value.', icon: Gem, active: true },
  { path: '/sales-forecasting', title: 'Sales Forecasting', desc: 'Use historical transaction patterns for time-series and forecasting experiments.', icon: TrendingUp, active: true },
  { path: '/rating-prediction', title: 'Customer Rating Prediction', desc: 'Explore which variables may help explain customer ratings.', icon: Star, active: true },
];

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
    <div className="space-y-8 animate-in fade-in duration-700">
      <div className="relative">
        <div className="absolute -top-10 -left-10 w-40 h-40 bg-blue-500/20 rounded-full blur-[60px] pointer-events-none"></div>
        <div className="absolute top-0 right-20 w-32 h-32 bg-indigo-500/10 rounded-full blur-[50px] pointer-events-none"></div>
        <h1 className="text-4xl font-bold mb-2 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 drop-shadow-sm">Dashboard Overview</h1>
        <p className="text-slate-400">High-level metrics and Machine Learning opportunities.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-blue-500/10 text-blue-400 rounded-xl shadow-[inset_0_0_10px_rgba(59,130,246,0.2)]">
              <RevenueIcon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Total Revenue</p>
              <p className="text-2xl font-bold tracking-tight text-white drop-shadow-md">{stats ? stats['Total Revenue'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-teal-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-teal-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-teal-500/10 text-teal-400 rounded-xl shadow-[inset_0_0_10px_rgba(20,184,166,0.2)]">
              <DollarSign className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Total Profit</p>
              <p className="text-2xl font-bold tracking-tight text-white drop-shadow-md">{stats ? stats['Total Profit'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl shadow-[inset_0_0_10px_rgba(99,102,241,0.2)]">
              <ShoppingCart className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Transactions</p>
              <p className="text-2xl font-bold tracking-tight text-white drop-shadow-md">{stats ? stats['Total Transactions'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-purple-500/10 text-purple-400 rounded-xl shadow-[inset_0_0_10px_rgba(168,85,247,0.2)]">
              <Percent className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Return Rate</p>
              <p className="text-2xl font-bold tracking-tight text-white drop-shadow-md">{stats ? stats['Return Rate'] : '...'}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card relative overflow-hidden">
        <div className="absolute right-0 top-0 w-64 h-64 bg-blue-500/5 rounded-full blur-[80px] pointer-events-none"></div>
        <h3 className="text-lg font-semibold mb-6 text-slate-100 flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]"></div>
          Revenue vs Returns (YTD)
        </h3>
        <div className="h-72 w-full relative z-10">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={revenueData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} strokeOpacity={0.4} />
              <XAxis dataKey="name" stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
              <YAxis stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
              <Tooltip 
                contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', backdropFilter: 'blur(10px)', borderColor: '#334155', color: '#f8fafc', borderRadius: '12px', boxShadow: '0 10px 25px -5px rgb(0 0 0 / 0.5)' }}
                itemStyle={{ color: '#f8fafc' }}
                cursor={{ fill: '#334155', opacity: 0.3 }}
              />
              <Bar dataKey="revenue" name="Revenue" fill="#3b82f6" radius={[6, 6, 0, 0]} />
              <Bar dataKey="returns" name="Returns" fill="#8b5cf6" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="pt-4">
        <h2 className="text-2xl font-bold mb-6 tracking-tight text-white flex items-center gap-3">
          Predictive Analytics Modules
          <div className="h-px bg-gradient-to-r from-slate-700 to-transparent flex-1 ml-4"></div>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mlFeatures.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <Link 
                key={idx} 
                to={feature.path}
                className="card group flex flex-col h-full hover:border-blue-500/40 relative overflow-hidden transition-all duration-300 transform hover:-translate-y-1"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600/5 via-transparent to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="absolute -inset-px bg-gradient-to-r from-blue-500/20 to-purple-500/20 opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-300 blur-sm -z-10"></div>
                <div className="flex items-center gap-4 mb-4 relative z-10">
                  <div className={`p-3 rounded-xl transition-all duration-300 ${feature.active ? 'bg-slate-800/80 text-blue-400 group-hover:bg-blue-500/20 group-hover:text-blue-300 group-hover:shadow-[0_0_15px_rgba(59,130,246,0.3)]' : 'bg-slate-800/40 text-slate-600'}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="font-semibold text-lg text-slate-200 group-hover:text-white transition-colors">{feature.title}</h3>
                </div>
                <p className="text-slate-400 text-sm flex-1 leading-relaxed relative z-10 group-hover:text-slate-300 transition-colors">{feature.desc}</p>
                {!feature.active && (
                  <div className="mt-4 inline-block px-3 py-1 bg-slate-800/50 text-xs rounded-full text-slate-500 self-start border border-slate-700 relative z-10">
                    Coming Soon
                  </div>
                )}
                {feature.active && (
                  <div className="mt-4 flex items-center text-xs font-medium text-blue-500/0 group-hover:text-blue-400 transition-colors relative z-10">
                    Explore Module <TrendingUp className="w-3 h-3 ml-1 opacity-0 group-hover:opacity-100 transition-opacity group-hover:translate-x-1 duration-300" />
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
