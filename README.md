# DoorDash 美國外送平台分析與預測

本專題以 **DoorDash** 為研究對象，使用 SEC 公開財務資料，透過 Python 進行資料擷取、整理、探索性資料分析與時間序列預測，並使用 Power BI 建立互動式商業分析與預測儀表板。

## Project Overview

本專題主要分析 DoorDash 的季度營運與財務表現，並比較不同時間序列模型的預測結果。

### Analysis Metrics

* Total Orders 總訂單量
* Marketplace GOV 平台市場總交易額
* Revenue 營業收入
* Adjusted EBITDA 稅前息前折舊攤銷前獲利

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

1. Executive Overview 精簡概述
2. Business Performance 經營績效
3. Growth Analysis 成長曲線分析
4. Revenue & Total Orders Relationship 營收與總訂單量之關聯
5. Revenue & Marketplace GOV Relationship 營收與平台市場總交易額之關聯
6. Revenue & Adjusted EBITDA Relationship 營收與稅前息前折舊攤銷前獲利之關聯
7. Data Model Overview 資料模型概覽
8. Data Model & Relationships 資料模型之關聯
9. AI & Prediction Overview 預測式AI概覽
10. Forecast Results 預測結果
11. Model Evaluation 模型評估
12. AI Prediction Insights AI預測洞察

Dashboard 主要呈現：

* Quarterly business performance 季度業務績效
* QoQ / YoY growth 季增率/年增率
* Correlation relationships 相關關係
* Forecast results 預測結果
* Model evaluation 模型評估
* AI prediction insights AI預測洞察

## Time Series Forecasting

本專題比較兩種時間序列模型：

### ARIMA

使用 ARIMA(1,1,0) 分別預測：

* Total Orders 總訂單量
* Marketplace GOV 平台市場總交易額
* Revenue 營業收入
* Adjusted EBITDA 稅前息前折舊攤銷前獲利

### Prophet

使用 Prophet 進行相同四項指標的時間序列預測。

模型評估採用：

* MAE
* RMSE

並使用最後 **4 季資料作為測試集**。

## Model Evaluation

模型比較結果顯示，不同營運指標的最佳模型並不完全相同。

* Revenue：ARIMA 的 MAE / RMSE 較低
* Total Orders：Prophet 的 MAE / RMSE 較低
* Marketplace GOV：Prophet 的 MAE / RMSE 較低
* Adjusted EBITDA：Prophet 的 MAE / RMSE 較低

由於本研究僅使用 14 季資料，模型評估結果主要反映目前資料期間與模型設定下的表現，因此預測結果應作為趨勢分析與決策參考，而非確定性的未來結果。

## Project Structure

```text
DoorDash_Project/
│
├── .gitignore
├── README.md
├── DoorDash_Dashboard.pbix
│
└── src/
    ├── get_filings.py
    ├── prepare_quarterly_data.py
    ├── growth_analysis.py
    ├── correlation_analysis.py
    ├── analyze_data.py
    ├── prediction.py
    ├── extract_q4_metrics.py
    └── data_collection.py
```

## Tools & Technologies

| Category              | Tools                     |
| --------------------- | ------------------------- |
| Programming           | Python                    |
| Data Collection       | SEC EDGAR                 |
| Data Processing       | pandas, NumPy             |
| Statistical Analysis  | statsmodels, scikit-learn |
| Forecasting           | ARIMA, Prophet            |
| Visualization         | matplotlib                |
| Business Intelligence | Power BI                  |
| Version Control       | Git / GitHub              |

## Project Objective

本專題希望透過公開企業資料，建立一套從 **資料擷取 → 資料分析 → 商業視覺化 → 時間序列預測 → 模型評估** 的完整分析流程，了解 DoorDash 的營運表現與未來趨勢。
