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

print("資料讀取成功！")
print(f"共有 {len(df)} 個季度")
print()

print("資料內容：")
print(df.to_string(index=False))


# =========================
# 2. 基本資料檢查
# =========================

print("\n資料型態：")
print(df.dtypes)

print("\n缺失值：")
print(df.isnull().sum())

print("\n基本統計：")
print(
    df[
        [
            "total_orders",
            "marketplace_gov",
            "revenue",
            "adjusted_ebitda",
        ]
    ].describe()
)


# =========================
# 3. 設定圖表 X 軸
# =========================

x = df["period"]


# =========================
# 4. Total Orders 趨勢圖
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    x,
    df["total_orders"],
    marker="o"
)

plt.title("DoorDash Total Orders by Quarter")

plt.xlabel("Quarter")

plt.ylabel("Total Orders (Million)")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "data/processed/total_orders_trend.png"
)

plt.show()


# =========================
# 5. Marketplace GOV 趨勢圖
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    x,
    df["marketplace_gov"],
    marker="o"
)

plt.title("DoorDash Marketplace GOV by Quarter")

plt.xlabel("Quarter")

plt.ylabel("Marketplace GOV (Million USD)")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "data/processed/marketplace_gov_trend.png"
)

plt.show()


# =========================
# 6. Revenue 趨勢圖
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    x,
    df["revenue"],
    marker="o"
)

plt.title("DoorDash Revenue by Quarter")

plt.xlabel("Quarter")

plt.ylabel("Revenue (Million USD)")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "data/processed/revenue_trend.png"
)

plt.show()


# =========================
# 7. Adjusted EBITDA 趨勢圖
# =========================

plt.figure(figsize=(12, 6))

plt.plot(
    x,
    df["adjusted_ebitda"],
    marker="o"
)

plt.title("DoorDash Adjusted EBITDA by Quarter")

plt.xlabel("Quarter")

plt.ylabel("Adjusted EBITDA (Million USD)")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "data/processed/adjusted_ebitda_trend.png"
)

plt.show()


print("\n視覺化完成！")

print("\n產生的圖表：")
print("1. data/processed/total_orders_trend.png")
print("2. data/processed/marketplace_gov_trend.png")
print("3. data/processed/revenue_trend.png")
print("4. data/processed/adjusted_ebitda_trend.png")