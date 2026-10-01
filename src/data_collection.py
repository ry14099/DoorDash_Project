import requests
import pandas as pd

from bs4 import BeautifulSoup

# =========================
# SEC 設定
# =========================

url = "https://data.sec.gov/api/xbrl/companyfacts/CIK0001792789.json"

headers = {
    "User-Agent": "DoorDash Analysis student@example.com"
}


# =========================
# 取得 SEC XBRL 資料
# =========================

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("取得 SEC XBRL 資料失敗")
    exit()

data = response.json()

print("成功取得 DoorDash XBRL 資料！")


# =========================
# 取得 Revenue
# =========================

revenue_data = data["facts"]["us-gaap"][
    "RevenueFromContractWithCustomerExcludingAssessedTax"
]

units = revenue_data["units"]["USD"]

df = pd.DataFrame(units)


# =========================
# 日期處理
# =========================

df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])


# =========================
# 只保留 2023～2026
# =========================

df = df[
    (df["end"] >= "2023-01-01") &
    (df["end"] <= "2026-06-30")
].copy()


# =========================
# 找出真正的單季 Revenue
# =========================

quarterly = df[
    (df["end"] - df["start"]).dt.days.between(80, 100)
].copy()


# =========================
# 去除重複資料
# =========================

quarterly = quarterly.drop_duplicates(
    subset=["start", "end", "val"]
)


# =========================
# 建立 Year / Quarter
# =========================

quarterly["year"] = quarterly["end"].dt.year

quarterly["quarter"] = (
    "Q" + quarterly["end"].dt.quarter.astype(str)
)


# =========================
# 只保留需要的欄位
# =========================

quarterly = quarterly[
    ["end", "year", "quarter", "val"]
].copy()

quarterly = quarterly.rename(
    columns={
        "end": "date",
        "val": "revenue"
    }
)


# =========================
# 取得年度 Revenue
# =========================

annual = df[
    (df["form"] == "10-K") &
    (df["start"].dt.month == 1) &
    (df["start"].dt.day == 1) &
    (df["end"].dt.month == 12) &
    (df["end"].dt.day == 31)
].copy()


# =========================
# 去除年度重複資料
# =========================

annual = annual.drop_duplicates(
    subset=["start", "end", "val"]
)


# =========================
# 計算 Q4
# =========================

q4_rows = []

for _, row in annual.iterrows():

    year = row["end"].year
    annual_revenue = row["val"]

    q1 = quarterly[
        (quarterly["year"] == year) &
        (quarterly["quarter"] == "Q1")
    ]["revenue"].sum()

    q2 = quarterly[
        (quarterly["year"] == year) &
        (quarterly["quarter"] == "Q2")
    ]["revenue"].sum()

    q3 = quarterly[
        (quarterly["year"] == year) &
        (quarterly["quarter"] == "Q3")
    ]["revenue"].sum()

    # 確認前三季都有資料
    if q1 > 0 and q2 > 0 and q3 > 0:

        q4_revenue = annual_revenue - q1 - q2 - q3

        q4_rows.append({
            "date": pd.Timestamp(f"{year}-12-31"),
            "year": year,
            "quarter": "Q4",
            "revenue": q4_revenue
        })


# =========================
# 加入 Q4
# =========================

q4_df = pd.DataFrame(q4_rows)

quarterly = pd.concat(
    [quarterly, q4_df],
    ignore_index=True
)


# =========================
# 排序
# =========================

quarterly = quarterly.sort_values(
    "date"
).reset_index(drop=True)


# =========================
# 儲存 CSV
# =========================

quarterly.to_csv(
    "data/raw/doordash_financial.csv",
    index=False
)


# =========================
# 顯示結果
# =========================

print("\nDoorDash 季度 Revenue：")

print(
    quarterly.to_string(index=False)
)

print("\n資料筆數：", len(quarterly))

print("\nCSV 已建立：")
print("data/raw/doordash_financial.csv")

# =========================
# 尋找 DoorDash 自訂指標
# =========================

print("\nSEC 自訂 Taxonomy：")

for namespace in data["facts"]:

    print(namespace)


 # =========================
# 取得 DoorDash 2026 Q2 10-Q
# =========================

filing_url = (
    "https://www.sec.gov/Archives/edgar/data/"
    "1792789/000179278926000050/"
    "dash-20260630.htm"
)

response = requests.get(
    filing_url,
    headers=headers
)

print("\n10-Q HTTP Status:", response.status_code)

if response.status_code == 200:

    print("成功取得 DoorDash 2026 Q2 10-Q！")

    # HTML → BeautifulSoup
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # 移除不需要的內容
    for tag in soup(["script", "style"]):
        tag.decompose()

    # HTML → 純文字
    text = soup.get_text(
        separator=" ",
        strip=True
    )

    print("純文字字數：", len(text))



import re

# =========================
# 擷取 Operating Metrics
# =========================

pattern = (
    r"Three Months Ended June 30,"
    r".{0,500}"
    r"Total Orders\s+([\d,]+)\s+([\d,]+)"
    r".{0,300}"
    r"Marketplace GOV\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
    r".{0,300}"
    r"Revenue\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
    r".{0,1000}"
    r"Adjusted EBITDA\s+\(1\)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
)

match = re.search(
    pattern,
    text,
    re.DOTALL
)

if match:

    # 2025 Q2
    total_orders_2025 = int(
        match.group(1).replace(",", "")
    )

    marketplace_gov_2025 = int(
        match.group(3).replace(",", "")
    )

    revenue_2025 = int(
        match.group(5).replace(",", "")
    )

    adjusted_ebitda_2025 = int(
        match.group(7).replace(",", "")
    )

    # 2026 Q2
    total_orders_2026 = int(
        match.group(2).replace(",", "")
    )

    marketplace_gov_2026 = int(
        match.group(4).replace(",", "")
    )

    revenue_2026 = int(
        match.group(6).replace(",", "")
    )

    adjusted_ebitda_2026 = int(
        match.group(8).replace(",", "")
    )

    print("\n成功擷取 Operating Metrics")

    print("\n2025 Q2")
    print("Total Orders:", total_orders_2025)
    print("Marketplace GOV:", marketplace_gov_2025)
    print("Revenue:", revenue_2025)
    print("Adjusted EBITDA:", adjusted_ebitda_2025)

    print("\n2026 Q2")
    print("Total Orders:", total_orders_2026)
    print("Marketplace GOV:", marketplace_gov_2026)
    print("Revenue:", revenue_2026)
    print("Adjusted EBITDA:", adjusted_ebitda_2026)

else:

    print("\n找不到 Operating Metrics")
