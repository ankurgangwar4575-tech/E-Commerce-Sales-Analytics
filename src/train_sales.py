import pandas as pd
import json
from pathlib import Path
from lightgbm import LGBMRegressor

def train_sales_model():
    print("Loading data for Sales Forecasting...")
    data_path = Path("data/ecommerce_sales_customer_analytics_150k.csv")
    df = pd.read_csv(data_path)
    
    df['order_date'] = pd.to_datetime(df['order_date']).dt.date
    daily_sales = df.groupby('order_date')['net_sales'].sum().reset_index()
    daily_sales.columns = ['date', 'sales']
    daily_sales = daily_sales.sort_values('date').reset_index(drop=True)
    
    for i in [1, 2, 3, 7, 14]:
        daily_sales[f'lag_{i}'] = daily_sales['sales'].shift(i)
    
    daily_sales['rolling_7'] = daily_sales['sales'].shift(1).rolling(7).mean()
    
    train_data = daily_sales.dropna().copy()
    
    features = ['lag_1', 'lag_2', 'lag_3', 'lag_7', 'lag_14', 'rolling_7']
    X = train_data[features]
    y = train_data['sales']
    
    print("Training LightGBM Regressor for Sales Forecasting...")
    model = LGBMRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    last_known_data = daily_sales.tail(30).copy()
    future_dates = pd.date_range(start=pd.to_datetime(last_known_data['date'].iloc[-1]) + pd.Timedelta(days=1), periods=30)
    
    forecast_results = []
    
    history_sales = list(last_known_data['sales'].values)
    
    for date in future_dates:
        row = {
            'lag_1': history_sales[-1],
            'lag_2': history_sales[-2],
            'lag_3': history_sales[-3],
            'lag_7': history_sales[-7],
            'lag_14': history_sales[-14],
            'rolling_7': sum(history_sales[-7:]) / 7
        }
        
        pred_sales = model.predict(pd.DataFrame([row]))[0]
        pred_sales = max(0, pred_sales)
        
        history_sales.append(pred_sales)
        forecast_results.append({
            "date": date.strftime("%Y-%m-%d"),
            "predicted_sales": round(pred_sales, 2)
        })
        
    print("Saving forecast data...")
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    historical_results = [
        {
            "date": row['date'].strftime("%Y-%m-%d"),
            "actual_sales": round(row['sales'], 2)
        }
        for _, row in last_known_data.iterrows()
    ]
    
    final_output = {
        "historical": historical_results,
        "forecast": forecast_results
    }
    
    with open(model_dir / "sales_forecast_v1.json", "w") as f:
        json.dump(final_output, f, indent=4)
        
    print("Sales Forecasting model training & prediction complete!")

if __name__ == "__main__":
    train_sales_model()