
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
  Award
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
  return (
    <aside className="w-64 bg-slate-900/40 min-h-screen border-r border-slate-700/50 flex flex-col backdrop-blur-xl shadow-[4px_0_24px_-10px_rgba(0,0,0,0.5)] z-10 relative">
      <div className="p-6 border-b border-slate-700/50">
        <h1 className="text-xl font-bold text-slate-100 flex items-center gap-3 tracking-tight">
          <div className="p-1.5 bg-blue-500/10 rounded-lg border border-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.2)]">
            <Gem className="w-5 h-5 text-blue-400" />
          </div>
          E-Comm Analytics
        </h1>
      </div>
      <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
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
    </aside>
  );
};
