import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


# =========================
# SEC 設定
# =========================

headers = {
    "User-Agent": "DoorDash Analysis student@example.com"
}


# =========================
# DoorDash SEC submissions
# =========================

url = (
    "https://data.sec.gov/submissions/"
    "CIK0001792789.json"
)

response = requests.get(
    url,
    headers=headers
)

print("HTTP Status:", response.status_code)

if response.status_code != 200:
    print("取得 SEC submissions 失敗")
    exit()

data = response.json()

print("成功取得 DoorDash SEC submissions！")


# =========================
# 取得近期財報
# =========================

recent = data["filings"]["recent"]

df = pd.DataFrame(recent)


# =========================
# 只保留 10-Q / 10-K
# =========================

df = df[
    df["form"].isin(["10-Q", "10-K"])
].copy()


# =========================
# 只保留 2023～2026
# =========================

df["filingDate"] = pd.to_datetime(
    df["filingDate"]
)

df = df[
    (df["filingDate"] >= "2023-01-01") &
    (df["filingDate"] <= "2026-12-31")
].copy()


# =========================
# 只保留需要的欄位
# =========================

df = df[
    [
        "filingDate",
        "form",
        "accessionNumber",
        "primaryDocument"
    ]
].copy()


# =========================
# 排序
# =========================

df = df.sort_values(
    "filingDate"
).reset_index(drop=True)


# =========================
# 建立 SEC 財報網址
# =========================

def create_filing_url(accession_number, primary_document):

    accession_no_dash = accession_number.replace("-", "")

    url = (
        "https://www.sec.gov/Archives/edgar/data/"
        "1792789/"
        f"{accession_no_dash}/"
        f"{primary_document}"
    )

    return url


df["filing_url"] = df.apply(
    lambda row: create_filing_url(
        row["accessionNumber"],
        row["primaryDocument"]
    ),
    axis=1
)


# =========================
# 解析 Operating Metrics
# =========================

def extract_operating_metrics(text):

    pattern = (
        r"Total Orders\s+([\d,]+)\s+([\d,]+)"
        r".{0,500}"
        r"Marketplace GOV\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
        r".{0,500}"
        r"Revenue\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
        r".{0,1500}"
        r"Adjusted EBITDA\s+\(1\)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
    )

    match = re.search(
        pattern,
        text,
        re.DOTALL
    )

    if not match:
        return None

    return match


# =========================
# 自動擷取所有財報的 Operating Metrics
# =========================

results = []


for index, row in df.iterrows():

    filing_url = row["filing_url"]

    print("\n==============================")
    print("第", index + 1, "份")
    print("==============================")

    print("日期：", row["filingDate"])
    print("類型：", row["form"])
    print("文件：", row["primaryDocument"])


    # -------------------------
    # 下載
    # -------------------------

    try:
        response = requests.get(
        filing_url,
        headers=headers,
        timeout=30
     )
    except requests.exceptions.RequestException as e:
        print("下載失敗：", e)
        continue

    print("HTTP Status:", response.status_code)

    if response.status_code != 200:
        print("下載失敗！")
        continue


    # -------------------------
    # HTML → 純文字
    # -------------------------

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    print("HTML 字數：", len(response.text))
    print("純文字字數：", len(text))

    

    # -------------------------
    # 擷取 Metrics
    # -------------------------

    match = extract_operating_metrics(text)

        # 2023 Q1 特殊格式
    if match is None and row["primaryDocument"] == "dash-20230331.htm":

            print("使用 2023 Q1 專用格式擷取...")

            q1_pattern = (
                r"Total Orders\s+([\d,]+)\s+([\d,]+)"
                r"\s+Total Orders Y/Y growth"
                r".{0,300}"
                r"Marketplace GOV\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
                r".{0,300}"
                r"Revenue\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
                r".{0,500}"
                r"Adjusted EBITDA\(1\)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)"
            )

            match = re.search(
                q1_pattern,
                text,
                re.DOTALL
            )

            if match:
                print("2023 Q1 Operating Metrics 擷取成功!")

    if match is None:
            print("找不到 Operating Metrics")
            continue


    print("成功找到 Operating Metrics！")


    # =========================
    # 取得兩年度資料
    # =========================

    values = match.groups()

    print("Match:", values)


    total_orders_old = int(
        values[0].replace(",", "")
    )

    total_orders_new = int(
        values[1].replace(",", "")
    )


    marketplace_gov_old = int(
        values[2].replace(",", "")
    )

    marketplace_gov_new = int(
        values[3].replace(",", "")
    )


    revenue_old = int(
        values[4].replace(",", "")
    )

    revenue_new = int(
        values[5].replace(",", "")
    )


    adjusted_ebitda_old = int(
        values[6].replace(",", "")
    )

    adjusted_ebitda_new = int(
        values[7].replace(",", "")
    )


    # =========================
    # 顯示當期資料
    # =========================

    print("\n當期資料：")

    print(
        "Total Orders:",
        total_orders_new
    )

    print(
        "Marketplace GOV:",
        marketplace_gov_new
    )

    print(
        "Revenue:",
        revenue_new
    )

    print(
        "Adjusted EBITDA:",
        adjusted_ebitda_new
    )


    # =========================
    # 儲存結果
    # =========================

    results.append({
        "filing_date": row["filingDate"],
        "form": row["form"],
        "document": row["primaryDocument"],

        "total_orders": total_orders_new,
        "marketplace_gov": marketplace_gov_new,
        "revenue": revenue_new,
        "adjusted_ebitda": adjusted_ebitda_new
    })


# =========================
# 建立 Operating Metrics DataFrame
# =========================

metrics_df = pd.DataFrame(results)


# =========================
# 顯示結果
# =========================

print("\n==============================")
print("Operating Metrics 結果")
print("==============================")

print(
    metrics_df.to_string(index=False)
)


print(
    "\n成功擷取資料筆數：",
    len(metrics_df)
)


# =========================
# 儲存 CSV
# =========================

metrics_df.to_csv(
    "data/raw/doordash_operating_metrics.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nOperating Metrics CSV 儲存成功！"
)


# =========================
# 顯示 SEC 財報 URL
# =========================

print("\n==============================")
print("SEC 財報 URL")
print("==============================")


print(
    df[
        [
            "filingDate",
            "form",
            "primaryDocument",
            "filing_url"
        ]
    ].to_string(index=False)
)


# =========================
# 顯示所有財報
# =========================

print("\n==============================")
print("DoorDash 10-Q / 10-K")
print("==============================")


print(
    df.to_string(index=False)
)


print(
    "\n財報資料筆數：",
    len(df)
)