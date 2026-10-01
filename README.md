# DoorDash 美國外送平台分析與預測

本專題以 **DoorDash** 為研究對象，使用 SEC 公開財務資料，透過 Python 進行資料擷取、整理、探索性資料分析與時間序列預測，並使用 Power BI 建立互動式商業分析與預測儀表板。

## Project Overview

本專題主要分析 DoorDash 的季度營運與財務表現，並比較不同時間序列模型的預測結果。

### Analysis Metrics

* Total Orders
* Marketplace GOV
* Revenue
* Adjusted EBITDA

資料期間為 **2023 Q1 – 2026 Q2，共 14 季**。

## Project Workflow

```text
SEC Public Filings
        ↓
Python Data Collection
        ↓
Data Cleaning & Processing
        ↓
Exploratory Data Analysis
        ↓
Growth & Correlation Analysis
        ↓
Power BI Dashboard
        ↓
Time Series Forecasting
        ↓
ARIMA / Prophet
        ↓
Forecast & Model Evaluation
```

## Data Source

本專題主要使用 DoorDash 向 **U.S. Securities and Exchange Commission (SEC)** 提交的公開 10-Q 與 10-K 文件。

透過 Python 擷取並整理季度營運與財務資料。

## Python Analysis

使用 Python 完成：

* SEC filings data collection
* Quarterly data preparation
* Growth rate analysis
* Correlation analysis
* Trend visualization
* Time series forecasting
* Model evaluation

主要 Python 套件：

* pandas
* NumPy
* requests
* statsmodels
* Prophet
* scikit-learn
* matplotlib

## Power BI Dashboard

本專題建立 12 頁 Power BI 報告，涵蓋：

1. Executive Overview
2. Business Performance
3. Growth Analysis
4. Revenue & Total Orders Relationship
5. Revenue & Marketplace GOV Relationship
6. Revenue & Adjusted EBITDA Relationship
7. Data Model Overview
8. Data Model & Relationships
9. AI & Prediction Overview
10. Forecast Results
11. Model Evaluation
12. AI Prediction Insights

Dashb
