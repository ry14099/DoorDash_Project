import pandas as pd
import matplotlib.pyplot as plt
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
# 2. 選擇分析欄位
# =========================

columns = [
    "total_orders",
    "marketplace_gov",
    "revenue",
    "adjusted_ebitda"
]

correlation_df = df[columns].corr()


# =========================
# 3. 顯示相關係數
# =========================

print("\n相關係數矩陣：")

print(
    correlation_df.round(2)
)


# =========================
# 4. 儲存相關係數
# =========================

output_file = Path(
    "data/processed/doordash_correlation.csv"
)

correlation_df.to_csv(
    output_file
)

print(
    f"\n相關係數已儲存：{output_file}"
)


# =========================
# 5. 建立相關性熱圖
# =========================

plt.figure(figsize=(8, 6))

plt.imshow(
    correlation_df,
    aspect="auto"
)

plt.colorbar(
    label="Correlation"
)

plt.xticks(
    range(len(columns)),
    [
        "Total Orders",
        "Marketplace GOV",
        "Revenue",
        "Adjusted EBITDA"
    ],
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(columns)),
    [
        "Total Orders",
        "Marketplace GOV",
        "Revenue",
        "Adjusted EBITDA"
    ]
)

plt.title(
    "DoorDash Operating Metrics Correlation"
)

plt.tight_layout()

plt.savefig(
    "data/processed/doordash_correlation_heatmap.png"
)

plt.show()


print("\n相關性分析完成！")
print(
    "圖表：data/processed/"
    "doordash_correlation_heatmap.png"
)