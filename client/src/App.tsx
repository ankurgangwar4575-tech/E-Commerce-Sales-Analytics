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
    <div className="relative min-h-screen bg-slate-950 text-slate-300 font-sans selection:bg-blue-500/30 overflow-x-hidden">
      <div
        className="fixed inset-0 z-0 bg-cover bg-center bg-no-repeat pointer-events-none opacity-60 sm:opacity-70 mix-blend-screen transition-opacity duration-500"
        style={{ backgroundImage: `url('/background.jpg')` }}
      />

      <div className="fixed inset-0 z-0 bg-gradient-to-b from-slate-950/70 via-slate-950/40 to-slate-950/85 pointer-events-none" />
      <div className="fixed inset-0 z-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-sky-900/30 via-transparent to-slate-950/80 pointer-events-none" />

      <div className="relative z-10 flex min-h-screen">
        <Sidebar />
        <main className="flex-1 p-8 pt-24 lg:pt-8 lg:pl-24 overflow-y-auto">
          <div className="relative mb-8 text-center flex flex-col items-center">
            <div className="absolute -top-10 -left-10 w-40 h-40 bg-blue-500/20 rounded-full blur-[60px] pointer-events-none"></div>
            <div className="absolute top-0 right-20 w-32 h-32 bg-indigo-500/10 rounded-full blur-[50px] pointer-events-none"></div>
            <h1 className="text-4xl font-bold mb-2 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-sky-300 drop-shadow-sm">Next Gen E-Commerce Intelligence</h1>
            {isDashboard && (
              <p className="text-slate-400 max-w-2xl mt-3 leading-relaxed">Real-time machine learning predictions, sales forecasting, and customer behavior analytics</p>
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
    </div>
  );
}

export default App;
