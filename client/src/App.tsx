import { Routes, Route, useLocation } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { ReturnPrediction } from './pages/ReturnPrediction';
import { CustomerSegmentation } from './pages/CustomerSegmentation';
import { HighValueDetection } from './pages/HighValueDetection';
import { SalesForecasting } from './pages/SalesForecasting';
import { RatingPrediction } from './pages/RatingPrediction';
import { SegmentClassification } from './pages/SegmentClassification';
import { ReturnReason } from './pages/ReturnReason';
import { LoyaltyPredictor } from './pages/LoyaltyPredictor';
import { ReviewSentiment } from './pages/ReviewSentiment';

function App() {
  const location = useLocation();
  const isDashboard = location.pathname === '/';

  return (
    <div className="flex min-h-screen bg-zinc-950 text-zinc-400 font-sans selection:bg-indigo-500/30">
      <Sidebar />
      <main className="flex-1 p-8 pt-24 lg:pt-8 lg:pl-24 overflow-y-auto bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-900/10 via-zinc-950 to-zinc-950">
        <div className="relative mb-8 text-center flex flex-col items-center">
          <div className="absolute -top-10 -left-10 w-40 h-40 bg-blue-500/20 rounded-full blur-[60px] pointer-events-none"></div>
          <div className="absolute top-0 right-20 w-32 h-32 bg-indigo-500/10 rounded-full blur-[50px] pointer-events-none"></div>
          <h1 className="text-4xl font-bold mb-2 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 drop-shadow-sm">E-Commerce Sales Analytics</h1>
          {isDashboard && (
            <p className="text-slate-400 max-w-2xl mt-3 leading-relaxed">AI-powered insights, financial metrics, and predictive models for your platform.</p>
          )}
        </div>

        <div className="min-h-[calc(100vh-250px)]">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/return-prediction" element={<ReturnPrediction />} />
            <Route path="/customer-segmentation" element={<CustomerSegmentation />} />
            <Route path="/segment-classification" element={<SegmentClassification />} />
            <Route path="/loyalty-predictor" element={<LoyaltyPredictor />} />
            <Route path="/return-reason" element={<ReturnReason />} />
            <Route path="/review-sentiment" element={<ReviewSentiment />} />
            <Route path="/high-value-customer" element={<HighValueDetection />} />
            <Route path="/sales-forecasting" element={<SalesForecasting />} />
            <Route path="/rating-prediction" element={<RatingPrediction />} />
          </Routes>
        </div>

        <footer className="mt-12 pt-6 border-t border-slate-800/60 text-center text-slate-500 text-sm">
          &copy; {new Date().getFullYear()} E-Commerce Analytics Platform. All rights reserved.
        </footer>
      </main>
    </div>
  );
}

export default App;
