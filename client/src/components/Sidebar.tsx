
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  RotateCcw, 
  Users, 
  Gem, 
  UserMinus, 
  TrendingUp, 
  Package, 
  Star, 
  DollarSign, 
  Target 
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/return-prediction', label: 'Return Prediction', icon: RotateCcw },
  { path: '/customer-segmentation', label: 'Customer Segmentation', icon: Users },
  { path: '/high-value-customer', label: 'High-Value Detection', icon: Gem },
  { path: '/churn-risk', label: 'Churn-Risk Analysis', icon: UserMinus },
  { path: '/sales-forecasting', label: 'Sales Forecasting', icon: TrendingUp },
  { path: '/product-demand', label: 'Product Demand Analysis', icon: Package },
  { path: '/rating-prediction', label: 'Rating Prediction', icon: Star },
  { path: '/profitability', label: 'Profitability Prediction', icon: DollarSign },
  { path: '/customer-value', label: 'Customer Value Prediction', icon: Target },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-navy-800 min-h-screen border-r border-navy-700 flex flex-col">
      <div className="p-6 border-b border-navy-700">
        <h1 className="text-xl font-bold text-accent-teal flex items-center gap-2">
          <Gem className="w-6 h-6" /> E-Comm Analytics
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
                `flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                  isActive 
                    ? 'bg-navy-700 text-accent-teal' 
                    : 'text-slate-400 hover:bg-navy-700 hover:text-slate-200'
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
