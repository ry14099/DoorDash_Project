import pandas as pd
from pathlib import Path


# =========================
# 1. 讀取季度資料
# =========================

input_file = Path(
    "data/processed/doordash_quarterly_metrics.csv"
)

df = pd.read_csv(input_file)

print("季度資料讀取成功！")
print(f"共有 {len(df)} 個季度")


# =========================
# 2. 計算 QoQ
# =========================

metrics = [
    "total_orders",
    "marketplace_gov",
    "revenue",
    "adjusted_ebitda"
]

for column in metrics:
    df[f"{column}_qoq"] = df[column].pct_change()


# =========================
# 3. 計算 YoY
# =========================

for column in metrics:
    df[f"{column}_yoy"] = df[column].pct_change(4)


# =========================
# 4. 四捨五入
# =========================

growth_columns = []

for column in metrics:
    growth_columns.append(f"{column}_qoq")
    growth_columns.append(f"{column}_yoy")

df[growth_columns] = df[growth_columns].round(2)


# =========================
# 5. 顯示結果
# =========================

print("\n季度成長率：")

print(
    df[
        [
            "period",

            "total_orders_qoq",
            "total_orders_yoy",

            "marketplace_gov_qoq",
            "marketplace_gov_yoy",

            "revenue_qoq",
            "revenue_yoy",

            "adjusted_ebitda_qoq",
            "adjusted_ebitda_yoy"
        ]
    ].to_string(index=False)
)


# =========================
# 6. 儲存分析結果
# =========================

output_file = Path(
    "data/processed/doordash_growth_analysis.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\n成長率分析完成！")
print(f"儲存位置：{output_file}")