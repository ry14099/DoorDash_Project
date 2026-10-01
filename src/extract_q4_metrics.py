import requests
from bs4 import BeautifulSoup
import re


# =========================
# SEC 設定
# =========================

headers = {
    "User-Agent": "DoorDash Analysis student@example.com"
}


# =========================
# 需要檢查的 10-K
# =========================

filings = [
    {
        "year": 2023,
        "accession": "0001792789-23-000014",
        "document": "dash-20221231.htm"
    },
    {
        "year": 2024,
        "accession": "0001792789-24-000012",
        "document": "dash-20231231.htm"
    },
    {
        "year": 2025,
        "accession": "0001628280-25-005715",
        "document": "dash-20241231.htm"
    }
]


# =========================
# 逐份檢查
# =========================

for filing in filings:

    accession = filing["accession"].replace("-", "")
    
    url = (
        "https://www.sec.gov/Archives/edgar/data/1792789/"
        + accession
        + "/"
        + filing["document"]
    )

    print("\n================================")
    print("年度：", filing["year"])
    print("文件：", filing["document"])
    print("================================")

    try:
        response = requests.get(
            url,
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


    # =========================
    # HTML → 純文字
    # =========================

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

    print("純文字字數：", len(text))


    # =========================
    # 找所有 Total Orders
    # =========================

    positions = [
        m.start()
        for m in re.finditer(
            "Total Orders",
            text
        )
    ]

    print("Total Orders 出現次數：", len(positions))


    # =========================
    # 顯示每一個位置附近的內容
    # =========================

    for i, pos in enumerate(positions):

        print("\n--------------------------------")
        print("第", i + 1, "個 Total Orders")
        print("--------------------------------")

        print(
            text[pos:pos + 1500]
        )