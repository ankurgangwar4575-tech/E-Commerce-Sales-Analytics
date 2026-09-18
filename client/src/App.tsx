
import { Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { ReturnPrediction } from './pages/ReturnPrediction';
import { CustomerSegmentation } from './pages/CustomerSegmentation';
import { HighValueDetection } from './pages/HighValueDetection';
import { Placeholder } from './pages/Placeholder';

function App() {
  return (
    <div className="flex min-h-screen bg-navy-900 text-slate-300 font-sans">
      <Sidebar />
      <main className="flex-1 p-8 overflow-y-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/return-prediction" element={<ReturnPrediction />} />
          <Route path="/customer-segmentation" element={<CustomerSegmentation />} />
          <Route path="/high-value-customer" element={<HighValueDetection />} />
          <Route path="/churn-risk" element={<Placeholder title="Churn-Risk Analysis" />} />
          <Route path="/sales-forecasting" element={<Placeholder title="Sales Forecasting" />} />
          <Route path="/product-demand" element={<Placeholder title="Product Demand Analysis" />} />
          <Route path="/rating-prediction" element={<Placeholder title="Customer Rating Prediction" />} />
          <Route path="/profitability" element={<Placeholder title="Profitability Prediction" />} />
          <Route path="/customer-value" element={<Placeholder title="Customer Value Prediction" />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
