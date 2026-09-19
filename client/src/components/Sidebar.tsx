import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  RotateCcw, 
  Users, 
  Gem, 
  Star,
  Target,
  HelpCircle,
  MessageSquare,
  TrendingUp,
  Award,
  Menu,
  X
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/return-prediction', label: 'Return Prediction', icon: RotateCcw },
  { path: '/customer-segmentation', label: 'Customer Segmentation', icon: Users },
  { path: '/segment-classification', label: 'Segment Classification', icon: Target },
  { path: '/loyalty-predictor', label: 'Loyalty Points', icon: Award },
  { path: '/return-reason', label: 'Return Reason', icon: HelpCircle },
  { path: '/review-sentiment', label: 'Review Sentiment', icon: MessageSquare },
  { path: '/high-value-customer', label: 'High-Value Detection', icon: Gem },
  { path: '/sales-forecasting', label: 'Sales Forecasting', icon: TrendingUp },
  { path: '/rating-prediction', label: 'Rating Prediction', icon: Star },
];

export const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {!isOpen && (
        <button 
          onClick={() => setIsOpen(true)}
          className="fixed top-6 left-6 z-50 p-2.5 bg-slate-800/80 backdrop-blur-md rounded-xl text-slate-300 hover:text-white shadow-lg border border-slate-700/50 transition-all hover:scale-105"
        >
          <Menu className="w-6 h-6" />
        </button>
      )}

      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 transition-opacity"
          onClick={() => setIsOpen(false)}
        />
      )}

      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-slate-900/95 min-h-screen border-r border-slate-700/50 flex flex-col shadow-[4px_0_24px_-10px_rgba(0,0,0,0.8)] transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-6 border-b border-slate-700/50 flex items-center justify-between">
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-3 tracking-tight">
            <div className="p-1.5 bg-blue-500/10 rounded-lg border border-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.2)]">
              <Gem className="w-5 h-5 text-blue-400" />
            </div>
            AI Store Insights
          </h1>
          <button 
            onClick={() => setIsOpen(false)}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setIsOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-300 relative group ${
                  isActive 
                    ? 'bg-blue-600/15 text-blue-400 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.05),0_0_15px_-3px_rgba(59,130,246,0.15)] border border-blue-500/20 font-medium' 
                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 border border-transparent font-medium'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon className={`w-5 h-5 transition-transform duration-300 ${isActive ? 'scale-110' : 'group-hover:scale-110'}`} />
                  <span className="text-sm">{item.label}</span>
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-blue-400 rounded-r-full shadow-[0_0_10px_rgba(96,165,250,0.5)]"></div>
                  )}
                </>
              )}
            </NavLink>
          );
        })}
      </nav>
      <div className="p-4 border-t border-slate-700/50 space-y-4 bg-slate-900/50">
        <div className="flex items-center justify-between px-3 py-2 bg-slate-800/40 rounded-xl border border-slate-700/50">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse"></div>
            <span className="text-xs font-medium text-slate-300">ML Engines Active</span>
          </div>
        </div>
        <div className="flex items-center gap-3 px-2 pb-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <span className="font-bold text-white text-sm">AD</span>
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-slate-200">Admin User</p>
            <p className="text-xs text-slate-500">Manager</p>
          </div>
        </div>
      </div>
    </aside>
    </>
  );
};
