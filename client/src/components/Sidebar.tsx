
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  RotateCcw, 
  Users, 
  Gem, 
  Star,
  Target,
  Truck,
  HelpCircle,
  MessageSquare,
  TrendingUp
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/return-prediction', label: 'Return Prediction', icon: RotateCcw },
  { path: '/customer-segmentation', label: 'Customer Segmentation', icon: Users },
  { path: '/segment-classification', label: 'Segment Classification', icon: Target },
  { path: '/delivery-delay', label: 'Delivery Delay', icon: Truck },
  { path: '/return-reason', label: 'Return Reason', icon: HelpCircle },
  { path: '/review-sentiment', label: 'Review Sentiment', icon: MessageSquare },
  { path: '/high-value-customer', label: 'High-Value Detection', icon: Gem },
  { path: '/sales-forecasting', label: 'Sales Forecasting', icon: TrendingUp },
  { path: '/rating-prediction', label: 'Rating Prediction', icon: Star },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-zinc-950/50 min-h-screen border-r border-zinc-800/50 flex flex-col backdrop-blur-xl">
      <div className="p-6 border-b border-zinc-800/50">
        <h1 className="text-xl font-bold text-zinc-100 flex items-center gap-2 tracking-tight">
          <Gem className="w-6 h-6 text-indigo-400" /> E-Comm Analytics
        </h1>
      </div>
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-xl transition-all duration-200 ${
                  isActive 
                    ? 'bg-zinc-800/50 text-indigo-400 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.05)]' 
                    : 'text-zinc-500 hover:bg-zinc-900/50 hover:text-zinc-300'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span className="text-sm font-medium">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
};
