
import { Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { ReturnPrediction } from './pages/ReturnPrediction';
import { CustomerSegmentation } from './pages/CustomerSegmentation';
import { HighValueDetection } from './pages/HighValueDetection';
import { SalesForecasting } from './pages/SalesForecasting';
import { RatingPrediction } from './pages/RatingPrediction';
import { SegmentClassification } from './pages/SegmentClassification';
import { DeliveryDelay } from './pages/DeliveryDelay';
import { ReturnReason } from './pages/ReturnReason';
import { ReviewSentiment } from './pages/ReviewSentiment';

function App() {
  return (
    <div className="flex min-h-screen bg-navy-900 text-slate-300 font-sans">
      <Sidebar />
      <main className="flex-1 p-8 overflow-y-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/return-prediction" element={<ReturnPrediction />} />
          <Route path="/customer-segmentation" element={<CustomerSegmentation />} />
          <Route path="/segment-classification" element={<SegmentClassification />} />
          <Route path="/delivery-delay" element={<DeliveryDelay />} />
          <Route path="/return-reason" element={<ReturnReason />} />
          <Route path="/review-sentiment" element={<ReviewSentiment />} />
          <Route path="/high-value-customer" element={<HighValueDetection />} />
          <Route path="/sales-forecasting" element={<SalesForecasting />} />
          <Route path="/rating-prediction" element={<RatingPrediction />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
