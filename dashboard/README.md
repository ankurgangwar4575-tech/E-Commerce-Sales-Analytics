# 📊 Power BI Analytics Dashboard — E-Commerce Sales & ML Insights

Welcome to the **Power BI Analytics Dashboard** module of the **E-Commerce Sales Analytics & ML Platform**. This directory contains the interactive Power BI report (`.pbix`) along with high-resolution visual previews of every dashboard view.

The Power BI report integrates descriptive sales analytics with machine learning predictions (return risk, customer segmentation, delay warnings, and rating forecasts) exported directly from the Python backend pipeline.

---

## 📂 Folder Structure

```text
dashboard/
├── 📄 E-Commerce-Sales-Analytics.pbix      # Main Power BI Report file
├── 📁 Dashboard_Images/                   # High-resolution dashboard screenshots
│   ├── executive-overview.png            # 1. Executive Summary & Core KPIs
│   ├── sales-profitability.png           # 2. Revenue, Profit & Margin Deep-Dive
│   ├── product-performance.png           # 3. Product, Category & Rating Insights
│   ├── customer-intelligence.png         # 4. Customer Segmentation & Value Metrics
│   ├── marketing-analytics.png           # 5. Channel Acquisition & Campaign Performance
│   └── operations-returns.png            # 6. Logistics Delays & ML Return-Risk Analytics
└── 📄 README.md                           # Documentation for the dashboard folder
```

---

## 🖼️ Dashboard Pages & Visual Showcase

The Power BI report consists of six specialized views designed for executive leaders, sales managers, marketing strategists, and operations teams.

### 1. 📈 Executive Overview
High-level strategic view aggregating revenue, profit margins, order volume, top performance drivers, and global geographic sales distribution.

![Executive Overview](Dashboard_Images/executive-overview.png)

* **Key KPIs**: Total Sales Revenue, Net Profit, Profit Margin %, Total Orders, Average Order Value (AOV).
* **Core Visuals**: Monthly Revenue Trend vs Target, Top Performing Regions, Revenue by Category Breakdown.

---

### 2. 💰 Sales & Profitability Analytics
In-depth financial analysis focusing on discount impacts, regional sales performance, payment methods, and profit contributions.

![Sales & Profitability Analytics](Dashboard_Images/sales-profitability.png)

* **Key KPIs**: Gross Revenue, Net Margin %, Discount Impact ($), Average Profit Per Order.
* **Core Visuals**: Profit Margin by Product Category, Discount vs Profit Correlation, Payment Method Share, Regional Profit Heatmap.

---

### 3. 📦 Product Performance & Inventory Insights
Granular insights into individual product SKU demand, category revenue growth, customer rating distributions, and supplier performance.

![Product Performance](Dashboard_Images/product-performance.png)

* **Key KPIs**: Total Units Sold, Top Category Revenue, Average Product Rating, Active Suppliers.
* **Core Visuals**: Top 10 Best-Selling Products, Revenue vs Rating Scatter Plot, Category Returns vs Sales, Brand Performance Matrix.

---

### 4. 👥 Customer Intelligence & Segmentation
Comprehensive customer analytics combining RFM analysis (Recency, Frequency, Monetary) with Machine Learning KMeans clustering results.

![Customer Intelligence](Dashboard_Images/customer-intelligence.png)

* **Key KPIs**: Total Active Customers, Customer Lifetime Value (CLV), Average Repeat Order Rate, High-Value Customer Count.
* **Core Visuals**: Customer Cluster Distribution (VIP, Premium, Consumer, Business), Customer Acquisition YoY Growth, Spend Distribution by Segment.

---

### 5. 🎯 Marketing & Channel Analytics
Performance metrics for marketing channels, acquisition efficiency, campaign conversions, and customer retention.

![Marketing Analytics](Dashboard_Images/marketing-analytics.png)

* **Key KPIs**: Customer Acquisition Cost (CAC), Return on Ad Spend (ROAS), Total Marketing Spend, Conversion Rate %.
* **Core Visuals**: Revenue by Marketing Channel (Organic, Paid Search, Social, Direct, Email), Campaign Performance Comparison, Acquisition Trend by Channel.

---

### 6. 🚚 Operations, Logistics & Returns Management
Operational bottleneck identification combined with ML-predicted return risks, delivery delay forecasts, and return-reason classifications.

![Operations & Returns](Dashboard_Images/operations-returns.png)

* **Key KPIs**: Overall Return Rate %, High Return-Risk Orders, Average Delivery Delay (Days), On-Time Delivery Rate %.
* **Core Visuals**: ML Return-Risk Distribution, Delivery Delay Warnings by Carrier, Return Reasons Breakdown, Predicted vs Actual Returns by Product Group.

---

## 🔌 Data Architecture & ML Integration

The Power BI data model follows a **Star Schema** architecture designed for fast querying and DAX calculations.

```text
                              ┌──────────────────────────┐
                              │    dim_customer_master   │
                              └────────────┬─────────────┘
                                           │ (1:N)
┌─────────────────────────┐   ┌────────────▼─────────────┐   ┌──────────────────────────┐
│   dim_product_catalog   ├───►    fact_sales_orders     ◄───┤        dim_date          │
└─────────────────────────┘   └────────────┬─────────────┘   └──────────────────────────┘
                                           │ (1:1)
                              ┌────────────▼─────────────┐
                              │  fact_ml_predictions     │
                              │  - return_risk_score     │
                              │  - predicted_segment     │
                              │  - delay_warning_flag    │
                              │  - predicted_sentiment   │
                              └──────────────────────────┘
```

### Data Sources & Refreshes
1. **Primary Data Sources**: Source CSV files located in `data/` (`customer_master.csv`, `ecommerce_sales_customer_analytics_150k.csv`, `order_items.csv`, `product_catalog.csv`).
2. **Machine Learning Model Exports**: Processed ML outputs generated via `python -m src.export_predictions` into `data/predictions/`:
   * `return_predictions.csv` — Order-level return probability & risk class.
   * `customer_segmentation.csv` — Customer cluster profiles & RFM scores.
   * `segment_classification.csv` — Predicted customer segments.
   * `loyalty_point_predictions.csv` — Forecasted customer loyalty points.
   * `return_reason_predictions.csv` — Multi-class return reason probabilities.
   * `review_sentiment_predictions.csv` — Sentiment classification per order.
   * `high_value_predictions.csv` — High-value customer classification.
   * `rating_predictions.csv` — Predicted rating score.

---

## 🛠️ How to Open & Update the Power BI Report

### Prerequisites
* **Microsoft Power BI Desktop** (Latest version recommended; minimum version: 2023 or later).
* Windows OS (or Windows Virtual Machine on macOS/Linux).

### Quick Start Guide

1. **Generate Up-to-Date ML Predictions**:
   Ensure you have run the Python pipeline so that fresh prediction exports exist in `data/predictions/`:
   ```powershell
   # From root project directory
   python -m src.export_predictions
   ```

2. **Open the Report**:
   Double-click `E-Commerce-Sales-Analytics.pbix` or open Power BI Desktop and select **File > Open** pointing to:
   ```text
   dashboard/E-Commerce-Sales-Analytics.pbix
   ```

3. **Re-path Data Parameters (If Prompted)**:
   If Power BI shows a data source path mismatch:
   1. Click **Transform Data > Data source settings**.
   2. Select **Change Source** for the dataset tables.
   3. Update the folder path to point to your local project directory `.../E-Commerce-Sales-Analytics/data/`.
   4. Click **Apply Changes** to refresh queries.

4. **Refresh Report Data**:
   Click the **Refresh** button on the Home ribbon to pull the latest sales data and ML prediction exports into all dashboard visualizations.

---

## 💡 Key DAX Measures Included

Here are some of the key custom DAX measures implemented inside `E-Commerce-Sales-Analytics.pbix`:

* **Total Revenue**:
  ```dax
  Total Revenue = SUM(fact_sales_orders[sales_amount])
  ```
* **Profit Margin %**:
  ```dax
  Profit Margin % = DIVIDE(SUM(fact_sales_orders[profit]), SUM(fact_sales_orders[sales_amount]), 0)
  ```
* **Return Rate %**:
  ```dax
  Return Rate % = DIVIDE(CALCULATE(COUNT(fact_sales_orders[order_id]), fact_sales_orders[return_status] = "Returned"), COUNT(fact_sales_orders[order_id]), 0)
  ```
* **High-Risk Return Order Count**:
  ```dax
  High Risk Returns Count = CALCULATE(COUNT(fact_ml_predictions[order_id]), fact_ml_predictions[risk_score] >= 0.70)
  ```

---

## 🤝 Support & Contribution

If you encounter issues loading data, updating DAX formulas, or connecting prediction CSVs, please refer to the main repository [README.md](../README.md) or open an issue in the project repository.
