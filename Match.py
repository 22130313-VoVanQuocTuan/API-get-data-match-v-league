import cloudscraper
import csv
from datetime import datetime

url = "https://bs-api.baomoi.com/v1/match/get/list?listType=byTournament&seasonId=2026&listId=13"
scraper = cloudscraper.create_scraper()
data = scraper.get(url).json()

# Tên file CSV staging
filename = f"matches_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Lấy toàn bộ items 
items = data.get("data", {}).get("items", [])

# Lấy danh sách tất cả key của level 1 để làm header CSV 
fieldnames = set()
for m in items:
    fieldnames.update(m.keys())
fieldnames = list(fieldnames)

# Ghi dữ liệu ra CSV
with open(filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for m in items:
        writer.writerow(m)

print("Đã lưu:", filename)
