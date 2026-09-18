import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  RotateCcw, Users, Gem, UserMinus, TrendingUp, Package, Star, DollarSign, Target,
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

const mlFeatures = [
  { path: '/return-prediction', title: 'Return Prediction', desc: 'Build models to investigate factors associated with return behavior.', icon: RotateCcw, active: true },
  { path: '/customer-segmentation', title: 'Customer Segmentation', desc: 'Use behavioral features to discover customer groups.', icon: Users, active: true },
  { path: '/high-value-customer', title: 'High-Value Customer Detection', desc: 'Identify customers with higher historical business value.', icon: Gem, active: false },
  { path: '/churn-risk', title: 'Churn-Risk Analysis', desc: 'Develop analytical approaches for identifying potentially disengaged customers.', icon: UserMinus, active: false },
  { path: '/sales-forecasting', title: 'Sales Forecasting', desc: 'Use historical transaction patterns for time-series and forecasting experiments.', icon: TrendingUp, active: false },
  { path: '/product-demand', title: 'Product Demand Analysis', desc: 'Study demand patterns across products, categories, brands, and time periods.', icon: Package, active: false },
  { path: '/rating-prediction', title: 'Customer Rating Prediction', desc: 'Explore which variables may help explain customer ratings.', icon: Star, active: false },
  { path: '/profitability', title: 'Profitability Prediction', desc: 'Model the relationship between pricing, discounts, products, customers, and profitability.', icon: DollarSign, active: false },
  { path: '/customer-value', title: 'Customer Value Prediction', desc: 'Use historical customer behavior to estimate future customer value.', icon: Target, active: false },
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
    fetch('http://127.0.0.1:8000/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("Failed to load stats:", err));
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Dashboard Overview</h1>
        <p className="text-slate-400">High-level metrics and Machine Learning opportunities.</p>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-accent-teal/20 text-accent-teal rounded-lg">
              <RevenueIcon className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-slate-400">Total Revenue</p>
              <p className="text-2xl font-bold">{stats ? stats['Total Revenue'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-emerald-500/20 text-emerald-400 rounded-lg">
              <DollarSign className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-slate-400">Total Profit</p>
              <p className="text-2xl font-bold">{stats ? stats['Total Profit'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-500/20 text-blue-400 rounded-lg">
              <ShoppingCart className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-slate-400">Transactions</p>
              <p className="text-2xl font-bold">{stats ? stats['Total Transactions'] : '...'}</p>
            </div>
          </div>
        </div>
        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-red-500/20 text-red-400 rounded-lg">
              <Percent className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-slate-400">Return Rate</p>
              <p className="text-2xl font-bold">{stats ? stats['Return Rate'] : '...'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Chart Row */}
      <div className="bg-navy-800 border border-navy-700 rounded-xl p-6">
        <h3 className="text-lg font-semibold mb-6">Revenue vs Returns (YTD)</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={revenueData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#233554" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#112240', borderColor: '#233554', color: '#f8fafc' }}
                itemStyle={{ color: '#f8fafc' }}
              />
              <Bar dataKey="revenue" name="Revenue" fill="#0070f3" radius={[4, 4, 0, 0]} />
              <Bar dataKey="returns" name="Returns" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ML Features Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-6 mt-4">Predictive Analytics Modules</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mlFeatures.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <Link 
                key={idx} 
                to={feature.path}
                className="bg-navy-800 border border-navy-700 rounded-xl p-6 hover:border-accent-teal hover:shadow-lg hover:shadow-accent-teal/10 transition-all group flex flex-col h-full"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className={`p-3 rounded-lg ${feature.active ? 'bg-accent-teal/20 text-accent-teal' : 'bg-navy-700 text-slate-300'}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="font-semibold text-lg group-hover:text-accent-teal transition-colors">{feature.title}</h3>
                </div>
                <p className="text-slate-400 text-sm flex-1">{feature.desc}</p>
                {!feature.active && (
                  <div className="mt-4 inline-block px-3 py-1 bg-navy-700 text-xs rounded-full text-slate-300 self-start">
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
