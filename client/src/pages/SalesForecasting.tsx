import { useState, useEffect } from 'react';
import { TrendingUp, AlertCircle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { API_URL } from '../config';

export const SalesForecasting = () => {
  const [data, setData] = useState<{ historical: any[], forecast: any[] } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const response = await fetch(`${API_URL}/forecast`);
        if (!response.ok) throw new Error('Failed to fetch forecast data');

        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchForecast();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-accent-teal/30 border-t-accent-teal rounded-full animate-spin" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="card text-center text-red-400 py-12 flex flex-col items-center">
        <AlertCircle className="w-12 h-12 mb-4 opacity-50" />
        <p>Failed to load forecasting data</p>
        <p className="text-sm opacity-70 mt-2">{error}</p>
      </div>
    );
  }

  interface ChartDataPoint {
    date: string;
    actual: number | null;
    forecast: number | null;
    displayDate?: string;
  }

  const chartData: ChartDataPoint[] = [
    ...data.historical.map(d => ({ date: d.date, actual: d.actual_sales, forecast: null })),
    ...data.forecast.map(d => ({ date: d.date, actual: null, forecast: d.predicted_sales }))
  ];


  chartData.forEach(d => {
    const dateObj = new Date(d.date);
    d.displayDate = `${dateObj.getMonth() + 1}/${dateObj.getDate()}`;
  });

  const formatCurrency = (value: number) => {
    if (value >= 1000) return `$${(value / 1000).toFixed(1)}k`;
    return `$${value.toFixed(0)}`;
  };

  const totalProjected = data.forecast.reduce((sum, d) => sum + d.predicted_sales, 0);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-3xl font-bold text-indigo-400 flex items-center gap-2">
          <TrendingUp className="w-8 h-8" />
          Sales Forecasting (30 Days)
        </h2>
        <p className="text-zinc-400 mt-2">
          AI-powered time-series projection of daily revenue based on historical patterns.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card bg-gradient-to-br from-zinc-900/50 to-zinc-950/50 border-indigo-400/20">
          <h3 className="text-zinc-400 text-sm font-medium">Next 30 Days Projected Revenue</h3>
          <div className="text-3xl font-bold text-white mt-2">
            ${totalProjected.toLocaleString('en-US', { maximumFractionDigits: 0 })}
          </div>
        </div>
      </div>

      <div className="card h-[500px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <defs>
              <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4ade80" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#4ade80" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2dd4bf" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#2dd4bf" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis
              dataKey="displayDate"
              stroke="#64748b"
              tick={{ fill: '#94a3b8' }}
              tickMargin={10}
            />
            <YAxis
              stroke="#64748b"
              tick={{ fill: '#94a3b8' }}
              tickFormatter={formatCurrency}
              width={80}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }}
              itemStyle={{ color: '#f8fafc' }}
              formatter={(value: any) => [`$${Number(value).toLocaleString('en-US', { maximumFractionDigits: 0 })}`, 'Revenue']}
              labelStyle={{ color: '#94a3b8', marginBottom: '8px' }}
            />

            <ReferenceLine x={data.historical[data.historical.length - 1].displayDate} stroke="#94a3b8" strokeDasharray="3 3" />

            <Area
              type="monotone"
              dataKey="actual"
              name="Historical Sales"
              stroke="#4ade80"
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#colorActual)"
              isAnimationActive={true}
            />
            <Area
              type="monotone"
              dataKey="forecast"
              name="Forecasted Sales"
              stroke="#2dd4bf"
              strokeWidth={3}
              strokeDasharray="5 5"
              fillOpacity={1}
              fill="url(#colorForecast)"
              isAnimationActive={true}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
