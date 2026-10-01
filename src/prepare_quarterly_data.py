import pandas as pd
from pathlib import Path


# ==============================
# 1. 讀取原始 SEC 資料
# ==============================

input_file = Path("data/raw/doordash_operating_metrics.csv")

df = pd.read_csv(input_file)

print("原始資料：")
print(df)


# ==============================
# 2. 只保留 10-Q 季度資料
# ==============================

quarterly_df = df[df["form"] == "10-Q"].copy()


# ==============================
# 3. 根據 document 判斷季度
# ==============================

def get_quarter(document):
    if "0331" in document:
        return "Q1"
    elif "0630" in document:
        return "Q2"
    elif "0930" in document:
        return "Q3"
    else:
        return None


quarterly_df["quarter"] = quarterly_df["document"].apply(
    get_quarter
)

quarterly_df["year"] = pd.to_datetime(
    quarterly_df["document"].str.extract(r"(\d{4})")[0]
).dt.year


# ==============================
# 4. 建立季度標籤
# ==============================

quarterly_df["period"] = (
    quarterly_df["year"].astype(str)
    + quarterly_df["quarter"]
)


# ==============================
# 5. Q4 年度資料
#
# SEC 10-K 的年度數字
# Q4 = 全年 - Q1 - Q2 - Q3
# ==============================

annual_data = {
    2023: {
        "total_orders": 2161,
        "marketplace_gov": 66771,
        "revenue": 8635,
        "adjusted_ebitda": 1190
    },

    2024: {
        "total_orders": 2583,
        "marketplace_gov": 80231,
        "revenue": 10722,
        "adjusted_ebitda": 1900
    },

    2025: {
        "total_orders": 3172,
        "marketplace_gov": 102018,
        "revenue": 13717,
        "adjusted_ebitda": 2779
    }
}


# ==============================
# 6. 計算 Q4
# ==============================

q4_rows = []

for year, annual in annual_data.items():

    year_data = quarterly_df[
        quarterly_df["year"] == year
    ]

    q4_row = {
        "period": f"{year}Q4",
        "year": year,
        "quarter": "Q4",
        "filing_date": "",
        "form": "Calculated",
        "document": f"{year}_10K_Q4_calculated",

        "total_orders": (
            annual["total_orders"]
            - year_data["total_orders"].sum()
        ),

        "marketplace_gov": (
            annual["marketplace_gov"]
            - year_data["marketplace_gov"].sum()
        ),

        "revenue": (
            annual["revenue"]
            - year_data["revenue"].sum()
        ),

        "adjusted_ebitda": (
            annual["adjusted_ebitda"]
            - year_data["adjusted_ebitda"].sum()
        )
    }

    q4_rows.append(q4_row)


# ==============================
# 7. 將 Q4 加入季度資料
# ==============================

q4_df = pd.DataFrame(q4_rows)

quarterly_df = pd.concat(
    [quarterly_df, q4_df],
    ignore_index=True
)


# ==============================
# 8. 整理欄位順序
# ==============================

quarterly_df = quarterly_df[
    [
        "period",
        "year",
        "quarter",
        "filing_date",
        "form",
        "document",
        "total_orders",
        "marketplace_gov",
        "revenue",
        "adjusted_ebitda",
    ]
]


# ==============================
# 9. 排序
# ==============================

quarter_order = {
    "Q1": 1,
    "Q2": 2,
    "Q3": 3,
    "Q4": 4
}

quarterly_df["quarter_order"] = (
    quarterly_df["quarter"].map(quarter_order)
)

quarterly_df = quarterly_df.sort_values(
    ["year", "quarter_order"]
).reset_index(drop=True)

quarterly_df = quarterly_df.drop(
    columns=["quarter_order"]
)


# ==============================
# 10. 建立 processed 資料夾
# ==============================

output_dir = Path("data/processed")
output_dir.mkdir(
    parents=True,
    exist_ok=True
)


# ==============================
# 11. 儲存完整季度資料
# ==============================

output_file = (
    output_dir
    / "doordash_quarterly_metrics.csv"
)

quarterly_df.to_csv(
    output_file,
    index=False
)


# ==============================
# 12. 顯示結果
# ==============================

print("\n季度資料整理完成！")
print(f"共有 {len(quarterly_df)} 個季度")
print(f"儲存位置：{output_file}")

print("\n完整季度資料：")
print(
    quarterly_df.to_string(index=False)
)