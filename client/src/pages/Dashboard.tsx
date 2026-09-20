import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  RotateCcw, Users, Gem, TrendingUp, Star, Target, HelpCircle, MessageSquare, Award,
  Banknote, PiggyBank, CreditCard, Activity
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
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

const segmentData = [
  { name: 'Consumer', sales: 45000, returns: 1200 },
  { name: 'Corporate', sales: 32000, returns: 800 },
  { name: 'Home Office', sales: 18000, returns: 450 },
];

const productData = [
  { name: 'Laptops', sales: 1250 },
  { name: 'Phones', sales: 2100 },
  { name: 'Tablets', sales: 850 },
  { name: 'Monitors', sales: 1400 },
  { name: 'Audio', sales: 950 },
];

const trafficData = [
  { name: 'Mon', users: 1200 },
  { name: 'Tue', users: 1800 },
  { name: 'Wed', users: 2400 },
  { name: 'Thu', users: 2100 },
  { name: 'Fri', users: 2800 },
  { name: 'Sat', users: 3500 },
  { name: 'Sun', users: 3100 },
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
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-blue-500/10 text-blue-400 rounded-xl shadow-[inset_0_0_10px_rgba(59,130,246,0.2)]">
              <Banknote className="w-6 h-6" />
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
              <PiggyBank className="w-6 h-6" />
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
              <CreditCard className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Transactions</p>
              <p className="text-2xl font-bold tracking-tight text-white drop-shadow-md">{stats ? Number(stats['Total Transactions']).toLocaleString('en-US') : '...'}</p>
            </div>
          </div>
        </div>
        <div className="card !p-5 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex items-center gap-4 relative">
            <div className="p-3 bg-purple-500/10 text-purple-400 rounded-xl shadow-[inset_0_0_10px_rgba(168,85,247,0.2)]">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Return Rate</p>
              <p className="text-2xl font-bold tracking-tight text-white drop-shadow-md">{stats ? stats['Return Rate'] : '...'}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card relative overflow-hidden">
          <div className="absolute right-0 top-0 w-64 h-64 bg-blue-500/5 rounded-full blur-[80px] pointer-events-none"></div>
          <h3 className="text-lg font-semibold mb-6 text-slate-100 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]"></div>
            Revenue vs Returns
          </h3>
          <div className="h-72 w-full relative z-10">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={revenueData} margin={{ top: 15, right: 10, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} strokeOpacity={0.4} />
                <XAxis dataKey="name" stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', backdropFilter: 'blur(10px)', borderColor: '#334155', color: '#f8fafc', borderRadius: '12px', boxShadow: '0 10px 25px -5px rgb(0 0 0 / 0.5)' }}
                  itemStyle={{ color: '#f8fafc' }}
                  cursor={{ stroke: '#334155', strokeWidth: 1, strokeDasharray: '5 5' }}
                />
                <Line type="linear" dataKey="revenue" name="Revenue" stroke="#84cc16" strokeWidth={3} dot={{ r: 3, fill: '#84cc16', strokeWidth: 0 }} activeDot={{ r: 5, fill: '#bef264', strokeWidth: 0 }} />
                <Line type="linear" dataKey="returns" name="Returns" stroke="#ef4444" strokeWidth={3} dot={{ r: 3, fill: '#ef4444', strokeWidth: 0 }} activeDot={{ r: 5, fill: '#fca5a5', strokeWidth: 0 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="card relative overflow-hidden flex-1">
            <div className="absolute right-0 top-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-[40px] pointer-events-none"></div>
            <h3 className="text-sm font-semibold mb-3 text-slate-100 flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.8)]"></div>
              Sales by Segment
            </h3>
            <div className="h-28 w-full relative z-10">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={segmentData} margin={{ top: 5, right: 10, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 10, fill: '#94a3b8' }} />
                  <YAxis tickFormatter={(value) => value >= 1000 ? `${value / 1000}k` : value} stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 10, fill: '#94a3b8' }} width={35} />
                  <Tooltip
                    contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', backdropFilter: 'blur(10px)', borderColor: '#334155', color: '#f8fafc', borderRadius: '12px', boxShadow: '0 10px 25px -5px rgb(0 0 0 / 0.5)' }}
                    itemStyle={{ color: '#f8fafc' }}
                  />
                  <Area type="monotone" dataKey="sales" name="Sales" stroke="#8b5cf6" strokeWidth={2} fillOpacity={1} fill="url(#colorSales)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card relative overflow-hidden flex-1">
            <div className="absolute right-0 top-0 w-32 h-32 bg-amber-500/5 rounded-full blur-[40px] pointer-events-none"></div>
            <h3 className="text-sm font-semibold mb-3 text-slate-100 flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.8)]"></div>
              Weekly Traffic
            </h3>
            <div className="h-28 w-full relative z-10">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trafficData} margin={{ top: 5, right: 10, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 10, fill: '#94a3b8' }} />
                  <YAxis tickFormatter={(value) => value >= 1000 ? `${value / 1000}k` : value} stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 10, fill: '#94a3b8' }} width={35} />
                  <Tooltip
                    contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', backdropFilter: 'blur(10px)', borderColor: '#334155', color: '#f8fafc', borderRadius: '12px', boxShadow: '0 10px 25px -5px rgb(0 0 0 / 0.5)' }}
                    itemStyle={{ color: '#f8fafc' }}
                  />
                  <Area type="monotone" dataKey="users" name="Users" stroke="#f59e0b" strokeWidth={2} fillOpacity={1} fill="url(#colorUsers)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="card relative overflow-hidden">
          <div className="absolute right-0 top-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-[80px] pointer-events-none"></div>
          <h3 className="text-lg font-semibold mb-6 text-slate-100 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
            Top Categories
          </h3>
          <div className="h-72 w-full relative z-10">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={productData} margin={{ top: 15, right: 10, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} strokeOpacity={0.4} />
                <XAxis dataKey="name" stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} />
                <YAxis stroke="#64748b" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} width={35} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', backdropFilter: 'blur(10px)', borderColor: '#334155', color: '#f8fafc', borderRadius: '12px', boxShadow: '0 10px 25px -5px rgb(0 0 0 / 0.5)' }}
                  itemStyle={{ color: '#f8fafc' }}
                  cursor={{ fill: '#334155', opacity: 0.3 }}
                />
                <Bar dataKey="sales" name="Units" fill="#10b981" radius={[4, 4, 0, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
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
