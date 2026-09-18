
import { Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { ReturnPrediction } from './pages/ReturnPrediction';
import { CustomerSegmentation } from './pages/CustomerSegmentation';
import { HighValueDetection } from './pages/HighValueDetection';
import { SalesForecasting } from './pages/SalesForecasting';
import { RatingPrediction } from './pages/RatingPrediction';

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
          <Route path="/sales-forecasting" element={<SalesForecasting />} />
          <Route path="/rating-prediction" element={<RatingPrediction />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
