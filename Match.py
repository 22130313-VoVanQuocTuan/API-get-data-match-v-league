import cloudscraper
import csv
import os
from datetime import datetime

url = "https://bs-api.baomoi.com/v1/match/get/list?listType=byTournament&seasonId=2026&listId=13"
scraper = cloudscraper.create_scraper()
data = scraper.get(url).json()

items = data.get("data", {}).get("items", [])

# File CSV staging cố định
filename = "matches_staging.csv"

# Thứ tự cột cố định, thêm last_update
fieldnames = [
    "startTime", "away", "displayOnlyDate", "status", "path", "home", "id",
    "hasPenShootout", "isSpecial", "round", "minute", "minuteLabel",
    "hasExtraTime", "htScore", "result", "seasonId", "last_update"
]

# Đọc dữ liệu cũ nếu file tồn tại
existing_data = {}
if os.path.exists(filename):
    with open(filename, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_data[row["id"]] = row

# Cập nhật dữ liệu mới vào existing_data
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for m in items:
    row = {}
    for col in fieldnames:
        if col == "last_update":
            continue  # Bỏ qua last_update vì sẽ xử lý riêng
        if col in m:
            if isinstance(m[col], dict):
                row[col] = str(m[col])
            else:
                row[col] = str(m[col]) if m[col] is not None else ""
        else:
            row[col] = ""  # Nếu cột không có trong API

    # So sánh với dữ liệu cũ
    match_id = str(m["id"])
    if match_id in existing_data:
        old_row = existing_data[match_id]
        # Kiểm tra xem có sự thay đổi nào không
        has_changes = False
        for col in fieldnames:
            if col == "last_update":
                continue
            if row.get(col, "") != old_row.get(col, ""):
                has_changes = True
                break
        # Nếu có thay đổi, cập nhật last_update
        if has_changes:
            row["last_update"] = current_time
        else:
            # Giữ nguyên last_update cũ nếu không có thay đổi
            row["last_update"] = old_row.get("last_update", "")
    else:
        # Nếu là bản ghi mới, gán last_update là thời gian hiện tại
        row["last_update"] = current_time

    existing_data[match_id] = row

# Ghi toàn bộ dữ liệu ra CSV với thứ tự cố định
with open(filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in existing_data.values():
        writer.writerow(row)

print("Đã cập nhật:", filename)