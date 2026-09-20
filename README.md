# 🛍️ E-Commerce Sales Analytics & ML Platform

An end-to-end e-commerce analytics platform combining exploratory analysis, leakage-aware machine learning, a FastAPI backend, and a React dashboard.

## 🔗 Project links

| Resource | Link |
| Live application |[Live-Application] (https://saless-analyticss.vercel.app )|
 

## 👥 Authors

| Contributor | Profile / repository |
| --- | --- |
| **Dhairya Vishwakarma** | [GitHub profile](https://github.com/Dhairya-v72) |
| **Ankur Gangwar** | [GitHub profile](https://github.com/ankurgangwar4575-tech) |

## 🎯 What this project does

- Predicts the probability that an order will be returned.
- Segments customers using behavioural and value-based features.
- Detects high-value customers.
- Forecasts future sales.
- Predicts delivery-delay risk, loyalty points, likely return reason, customer rating, review sentiment, and customer segment.
- Exposes trained models through FastAPI.
- Provides an interactive React dashboard.

## ✅ What has been achieved

- Built a reproducible, chronological return-risk pipeline from raw CSV data through validation, leakage-safe feature engineering, model comparison, final evaluation, and model export.
- Compared Logistic Regression, LightGBM, XGBoost, and CatBoost for return prediction; the versioned LightGBM artifact is the selected production candidate.
- Delivered supporting analytics models for customer segmentation, segment classification, high-value customers, loyalty points, delivery delay, return reason, review sentiment, and rating prediction.
- Published trained artifacts and metadata in `models/`, exposed predictions through FastAPI, and connected them to the React/Vite dashboard.
- Created a Power BI report with executive, sales, product, customer, marketing, and operations/returns views.
- Added `src/export_predictions.py` to generate eight dashboard-ready prediction CSVs under `data/predictions/`.

## 🧭 Architecture

~~~text
CSV sources
   │
   ├── validation and relationship checks
   ├── customer feature engineering
   ├── product/item feature engineering
   └── one-row-per-order training table
            │
            ├── chronological model comparison
            ├── final evaluation and export
            └── versioned artifacts in models/
                            │
                   FastAPI backend
                            │
                   React + Vite dashboard
~~~

## 🧰 Tech stack

| Layer | Technologies | Purpose |
| --- | --- | --- |
| Data processing | Python, Pandas, NumPy | Loading, cleaning, joining, and transforming CSV data |
| Exploratory analysis | Jupyter, Matplotlib, Seaborn | Data-quality checks, EDA, and model visualizations |
| Machine learning | Scikit-learn, LightGBM, XGBoost, CatBoost | Classification, regression, clustering, and return-risk modelling |
| Model persistence | Joblib, JSON | Saving models, metadata, thresholds, and forecast output |
| Backend API | FastAPI, Pydantic, Uvicorn | Validated prediction endpoints and interactive API documentation |
| Frontend | React, TypeScript, Vite | Interactive analytics and prediction dashboard |
| UI styling | Tailwind CSS, Lucide React | Dashboard layout, styling, and icons |
| Charts | Recharts, Matplotlib, Seaborn | Dashboard and notebook visualizations |
| Testing | Pytest | Data, feature-engineering, pipeline, and prediction tests |
| Development | Git, GitHub, VS Code/JupyterLab | Version control, collaboration, and development workflow |

## 📁 Repository structure

~~~text
data/       Source CSV files, engineered features, processed datasets, and Power BI exports
notebooks/  Guided EDA, feature engineering, training, and prediction workflow
src/        Reusable data, feature, training, evaluation, and prediction code
models/     Versioned model artifacts, metadata, and forecast output
server/     FastAPI app, schemas, and model services
client/     React + TypeScript + Vite dashboard
dashboard/  Power BI report, page screenshots, and dashboard documentation
tests/      Data, feature, pipeline, and prediction tests
images/     EDA and model-evaluation visuals
~~~

## 🗃️ Data sources

| File | Purpose | Main key |
| --- | --- | --- |
| customer_master.csv | Customer demographics, locations, segment, acquisition cost | customer_id |
| ecommerce_sales_customer_analytics_150k.csv | Order-level sales, customer, delivery, review, and return data | order_id, customer_id |
| order_items.csv | Item quantities, prices, sales, cost, tax, shipping, and profit | order_id, product_id |
| product_catalog.csv | Product category, subcategory, brand, supplier, price, cost, rating | product_id |
| dataset_statistics.csv | Dataset-level reference statistics | — |

The final return-risk dataset contains one row per eligible order. Customer and product tables are joined through validated keys, and item rows are aggregated to order level.

## 🤖 Return-risk model

The target is:

~~~python
return_label = (return_status == "Returned").astype(int)
~~~

The chronological split is:

| Period | Use |
| --- | --- |
| 2021–2024 | Model training |
| January–June 2025 | Model comparison and threshold selection |
| July–December 2025 | One final untouched test evaluation |

PR-AUC is the primary selection metric because returned orders are the minority class. ROC-AUC, precision, recall, F1-score, accuracy, and confusion matrices are also reported.

### Final artifact

The selected model is LightGBM, saved as return_risk_v1, with a decision threshold of 0.70.

| Metric | Validation | Final test |
| --- | ---: | ---: |
| PR-AUC | 0.6264 | 0.8353 |
| ROC-AUC | 0.9342 | 0.9696 |
| Precision | 0.6048 | 0.7071 |
| Recall | 0.6225 | 0.8142 |
| F1-score | 0.6135 | 0.7569 |
| Accuracy | — | 0.9595 |

Saved files:

~~~text
models/return_risk_v1.joblib
models/return_risk_v1_metadata.json
~~~

The model excludes post-outcome fields such as return status/reason, delivery outcomes, reviews, sentiment, payment status, loyalty points, estimated delivery days, and the discount-derived target proxies identified during data auditing. Customer history features use earlier orders only.

## 📓 Notebook roadmap

| Notebook | Purpose |
| --- | --- |
| 00_project_setup.ipynb | Shared paths, imports, and data availability |
| 01_data_quality_and_relationships.ipynb | Schemas, missingness, duplicates, keys, and joins |
| 02_order_and_customer_eda.ipynb | Order, customer, channel, geography, and return analysis |
| 03_product_and_item_eda.ipynb | Product, item, category, brand, supplier, and rating analysis |
| 04_customer_feature_engineering.ipynb | Leakage-safe prior customer history features |
| 05_product_feature_engineering.ipynb | One product/item feature row per order |
| 06_build_training_dataset.ipynb | Final order-level modelling table |
| 07_baseline_model.ipynb | Logistic Regression baseline |
| 08_tree_model_comparison.ipynb | LightGBM, XGBoost, and CatBoost comparison |
| 09_final_evaluation_and_model_export.ipynb | Winner selection, final test, export, and metadata |
| 10_prediction_demo.ipynb | Loading the saved artifact and generating predictions |

The reusable equivalents are in src/; notebooks provide the guided workflow.

## 🧠 Available model artifacts

| Artifact | Capability |
| --- | --- |
| customer_segmentation_v1.joblib | KMeans customer clustering |
| segmentation_scaler.joblib | Customer segmentation scaler |
| return_risk_v1.joblib | Return probability and risk classification |
| high_value_v1.joblib | High-value customer classification |
| loyalty_predictor_v1.joblib | Loyalty-points regression |
| delay_classifier_v1.joblib | Delivery-delay risk classification |
| rating_prediction_v1.joblib | Customer-rating regression |
| segment_classifier_v1.joblib | Consumer/Premium/VIP/Business classification |
| return_reason_classifier_v1.joblib | Multi-class return-reason prediction |
| sentiment_classifier_v1.joblib | Review sentiment classification |
| sales_forecast_v1.json | Historical data and generated sales forecast |

Each model has a matching metadata JSON file containing its feature contract and, where available, evaluation information.

## ⚙️ Setup

### Python environment

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install fastapi uvicorn pydantic joblib
~~~

server/requirements.txt contains older pinned pandas/scikit-learn versions. Avoid installing it over the root ML environment unless those versions are intentionally aligned with the serialized model artifact.

### Run the reusable ML pipeline

~~~powershell
python -m src.run_pipeline
~~~

This validates data, creates features, builds the training table, compares candidate models, evaluates the winner, and writes model artifacts.

Individual stages:

~~~powershell
python -m src.validate_data
python -m src.customer_features
python -m src.product_features
python -m src.build_training_data
python -m src.train_models
python -m src.evaluate_model
python -m src.predict
~~~

### Run notebooks

~~~powershell
jupyter lab
~~~

Run notebooks 00–10 in order when rebuilding the documented analysis.

### Start the backend

~~~powershell
python -m uvicorn server.main:app --reload --host 127.0.0.1 --port 8000
~~~

Interactive documentation is available at:

~~~text
http://127.0.0.1:8000/docs
~~~

### Start the dashboard

~~~powershell
cd client
npm install
npm run dev
~~~

The dashboard normally runs at http://localhost:5173. To change the backend URL, create client/.env:

~~~text
VITE_API_URL=http://127.0.0.1:8000
~~~

Frontend commands:

~~~powershell
npm run lint
npm run build
npm run preview
~~~

## 🔌 API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | / | API welcome message |
| GET | /health | Backend and return-risk model status |
| GET | /stats | Dataset statistics |
| GET | /forecast | Saved sales forecast |
| POST | /predict | Return-risk score |
| POST | /segment | Customer clustering result |
| POST | /high-value | High-value customer probability |
| POST | /predict-loyalty | Predicted loyalty points |
| POST | /rating | Predicted customer rating |
| POST | /predict-segment | Predicted customer segment |
| POST | /predict-delay | Delivery-delay probability |
| POST | /predict-return-reason | Likely return reason and probabilities |
| POST | /predict-sentiment | Review sentiment and probabilities |

The return-risk endpoint expects a features dictionary containing all 50 model-ready fields listed in models/return_risk_v1_metadata.json and returns:

~~~json
{
  "risk_score": 0.78,
  "is_high_risk": true
}
~~~

## 🖥️ Dashboard modules

- 📊 Dashboard overview
- 🔁 Return prediction
- 👥 Customer segmentation
- 🎯 Segment classification
- 🚚 Delivery-delay warning
- ❓ Return-reason prediction
- 💬 Review sentiment analysis
- 💎 High-value customer detection
- 📈 Sales forecasting
- ⭐ Customer-rating prediction

The client uses React, TypeScript, Vite, React Router, Recharts, Tailwind CSS, and Lucide icons.

The dashboard includes return prediction, customer segmentation, segment classification,
loyalty points, delivery-delay warnings, return-reason prediction, review sentiment,
high-value customer detection, sales forecasting, and rating prediction.

## 📊 Power BI prediction exports

Generate the dashboard-ready CSV files with:

~~~powershell
python -m src.export_predictions
~~~

The command loads the saved artifacts from models/ and writes these files to data/predictions/:

| File | Grain | Contents |
| --- | --- | --- |
| return_predictions.csv | One row per eligible order | Return probability, risk level, and actual outcome |
| customer_segmentation.csv | One row per customer | Cluster, profile, spend, orders, and return rate |
| segment_classification.csv | One row per order | Predicted customer segment and class probabilities |
| loyalty_point_predictions.csv | One row per order | Predicted and actual loyalty points |
| return_reason_predictions.csv | One row per order | Predicted reason, reason probabilities, and return flag |
| review_sentiment_predictions.csv | One row per order with required inputs | Predicted sentiment and class probabilities |
| high_value_predictions.csv | One row per customer | High-value probability and classification |
| rating_predictions.csv | One row per order with required inputs | Predicted rating and prediction error |

Sales forecasting is already exported as models/sales_forecast_v1.json because it is a date-level forecast rather than an order-level prediction table. Rating and sentiment exports contain fewer rows when the source record is missing a feature required by their saved models.

## 🧪 Testing

~~~powershell
python -m pytest -q
~~~

The tests cover raw-data loading, schema validation, joins, customer features, product features, training-data construction, and prediction behaviour.

## 🔐 Production notes

- Keep credentials, local environments, and temporary outputs out of Git.
- Validate API payloads against the saved metadata feature contract.
- Keep preprocessing and model versions together; serialized scikit-learn pipelines are sensitive to package-version changes.
- Recalculate customer history using only information available before the scored order.
- Treat auxiliary models according to their own feature contracts; some are descriptive or post-order analytics models rather than pre-order return-risk models.
- Retrain and version the model when the schema, feature definitions, or business threshold changes.

## 🚀 Future improvements

- Add a feature-building endpoint so the dashboard can submit an order ID or raw order details instead of manually sending 50 engineered features.
- Add authentication, request logging, rate limiting, and structured API errors.
- Add model monitoring for drift, calibration, precision, recall, and return-rate changes.
- Add CI for tests, frontend lint/build, and model-schema validation.
- Add per-prediction explanations such as top contributing features.

## 👥 Collaboration

Keep exploratory work in notebooks/, reusable logic in src/, API logic in server/, and UI work in client/. Use focused branches and review changes before merging into main.

## 📄 License

Add a project license before public distribution.
