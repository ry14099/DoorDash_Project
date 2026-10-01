import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ============================================================
# 1. 讀取季度資料
# ============================================================

df = pd.read_csv(
    "data/processed/doordash_quarterly_metrics.csv"
)

print("=== DoorDash Prediction ===")
print(df)

print(f"\n資料筆數：{len(df)}")
print(
    f"資料期間：{df['period'].iloc[0]} ~ "
    f"{df['period'].iloc[-1]}"
)


# ============================================================
# 2. 基本設定
# ============================================================

forecast_periods = [
    "2026Q3",
    "2026Q4",
    "2027Q1",
    "2027Q2"
]

targets = [
    "revenue",
    "total_orders",
    "marketplace_gov",
    "adjusted_ebitda"
]


# ============================================================
# 3. 模型評估函數
# ============================================================

def evaluate_forecast(actual, predicted):
    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    return mae, rmse


# ============================================================
# 4. ARIMA
# ============================================================

arima_results = []
arima_forecasts = {}


for target in targets:

    print("\n" + "=" * 60)
    print(f"ARIMA 預測：{target}")
    print("=" * 60)

    series = df[target].astype(float)

    # --------------------------------------------------------
    # 4-1. Holdout Evaluation
    # 前 10 季訓練，最後 4 季測試
    # --------------------------------------------------------

    train = series.iloc[:-4]
    test = series.iloc[-4:]

    model = ARIMA(
        train,
        order=(1, 1, 0)
    )

    fitted_model = model.fit()

    test_forecast = fitted_model.forecast(
        steps=4
    )

    mae, rmse = evaluate_forecast(
        test.values,
        test_forecast.values
    )

    print(f"MAE  = {mae:.2f}")
    print(f"RMSE = {rmse:.2f}")

    arima_results.append({
        "model": "ARIMA(1,1,0)",
        "target": target,
        "MAE": mae,
        "RMSE": rmse
    })

    # --------------------------------------------------------
    # 4-2. 使用全部資料重新訓練
    # --------------------------------------------------------

    full_model = ARIMA(
        series,
        order=(1, 1, 0)
    )

    full_fitted_model = full_model.fit()

    forecast = full_fitted_model.forecast(
        steps=4
    )

    forecast_df = pd.DataFrame({
        "period": forecast_periods,
        f"{target}_forecast": forecast.values
    })

    arima_forecasts[target] = forecast_df

    # --------------------------------------------------------
    # 4-3. 保留原本 Power BI 使用的檔名
    # --------------------------------------------------------

    if target == "total_orders":
        file_name = "orders_forecast.csv"

    elif target == "marketplace_gov":
        file_name = "gov_forecast.csv"

    elif target == "adjusted_ebitda":
        file_name = "ebitda_forecast.csv"

    else:
        file_name = "revenue_forecast.csv"

    forecast_df.to_csv(
        f"data/processed/{file_name}",
        index=False
    )

    print(
        f"\n已儲存：data/processed/{file_name}"
    )

    print(forecast_df)


# ============================================================
# 5. 合併 ARIMA Forecast
# ============================================================

doordash_forecast = pd.DataFrame({
    "period": forecast_periods
})


for target in targets:

    doordash_forecast = doordash_forecast.merge(
        arima_forecasts[target],
        on="period"
    )


doordash_forecast.to_csv(
    "data/processed/doordash_forecast.csv",
    index=False
)

print("\n=== ARIMA Forecast ===")
print(doordash_forecast)

print(
    "\n已儲存："
    "data/processed/doordash_forecast.csv"
)




# ============================================================
# 6. Prophet
# ============================================================

prophet_results = []
prophet_forecasts = {}


for target in targets:

    print("\n" + "=" * 60)
    print(f"Prophet 預測：{target}")
    print("=" * 60)

    # --------------------------------------------------------
    # 6-1. 建立 Prophet 資料
    # 保留原本的季度日期設定
    # --------------------------------------------------------

    prophet_df = pd.DataFrame({
        "ds": pd.PeriodIndex(
            df["period"],
            freq="Q"
        ).to_timestamp(),

        "y": df[target].astype(float)
    })

    # --------------------------------------------------------
    # 6-2. Holdout Evaluation
    # 前 10 季訓練，最後 4 季測試
    # --------------------------------------------------------

    train_prophet = prophet_df.iloc[:-4].copy()
    test_prophet = prophet_df.iloc[-4:].copy()

    # 保留原本 Prophet 模型設定
    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(
        train_prophet
    )

    future_test = model.make_future_dataframe(
        periods=4,
        freq="QS"
    )

    forecast_test = model.predict(
        future_test
    )

    predicted_test = (
        forecast_test["yhat"]
        .tail(4)
        .values
    )

    actual_test = (
        test_prophet["y"]
        .values
    )

    mae, rmse = evaluate_forecast(
        actual_test,
        predicted_test
    )

    print(f"MAE  = {mae:.2f}")
    print(f"RMSE = {rmse:.2f}")

    prophet_results.append({
        "model": "Prophet",
        "target": target,
        "MAE": mae,
        "RMSE": rmse
    })

    # --------------------------------------------------------
    # 6-3. 使用全部資料重新訓練
    # --------------------------------------------------------

    full_model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    full_model.fit(
        prophet_df
    )

    future = full_model.make_future_dataframe(
        periods=4,
        freq="QS"
    )

    forecast = full_model.predict(
        future
    )

    future_forecast = (
        forecast[
            ["ds", "yhat"]
        ]
        .tail(4)
        .copy()
    )

    future_forecast["period"] = forecast_periods

    future_forecast = future_forecast[
        ["period", "yhat"]
    ]

    future_forecast = future_forecast.rename(
        columns={
            "yhat": f"{target}_forecast"
        }
    )

    prophet_forecasts[target] = future_forecast

    # --------------------------------------------------------
    # 6-4. 保留原本 Power BI 使用的檔名
    # --------------------------------------------------------

    if target == "total_orders":
        file_name = "orders_prophet_forecast.csv"

    elif target == "marketplace_gov":
        file_name = "gov_prophet_forecast.csv"

    elif target == "adjusted_ebitda":
        file_name = "ebitda_prophet_forecast.csv"

    else:
        file_name = "revenue_prophet_forecast.csv"

    future_forecast.to_csv(
        f"data/processed/{file_name}",
        index=False
    )

    print(
        f"\n已儲存：data/processed/{file_name}"
    )

    print(future_forecast)


# ============================================================
# 7. 合併 Prophet Forecast
# ============================================================

doordash_prophet_forecast = pd.DataFrame({
    "period": forecast_periods
})


for target in targets:

    doordash_prophet_forecast = (
        doordash_prophet_forecast.merge(
            prophet_forecasts[target],
            on="period"
        )
    )


doordash_prophet_forecast.to_csv(
    "data/processed/doordash_prophet_forecast.csv",
    index=False
)

print("\n=== Prophet Forecast ===")
print(doordash_prophet_forecast)

print(
    "\n已儲存："
    "data/processed/doordash_prophet_forecast.csv"
)


# ============================================================
# 8. 合併模型評估結果
# ============================================================

model_evaluation = pd.DataFrame(
    arima_results + prophet_results
)

model_evaluation.to_csv(
    "data/processed/model_evaluation.csv",
    index=False
)

print("\n=== Model Evaluation ===")
print(model_evaluation)

print(
    "\n已儲存："
    "data/processed/model_evaluation.csv"
)


# ============================================================
# 9. 完成
# ============================================================

print("\n" + "=" * 60)
print("所有 ARIMA / Prophet 預測與模型評估完成！")
print("=" * 60)