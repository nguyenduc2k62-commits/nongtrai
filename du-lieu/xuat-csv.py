#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xuất dữ liệu ra CSV để mở bằng Excel.

Ghi kèm BOM (utf-8-sig): không có BOM thì Excel trên Windows đọc file UTF-8
thành mã lỗi, tên thuốc và tên cây tiếng Việt biến thành ký tự rác.

Chạy: python xuat-csv.py   →   thư mục csv/
"""
import json, io, os, csv, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.makedirs("csv", exist_ok=True)


def J(f):
    return json.load(io.open(f, encoding="utf-8"))


def ghi(ten, cot, hang):
    p = os.path.join("csv", ten)
    with io.open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(cot)
        w.writerows(hang)
    print("  %-34s %6d dòng" % (ten, len(hang)))


thuoc = J("danh-muc-thuoc-2026.json")["thuoc"]

# 1) Một dòng một thuốc — để tra nhanh
ghi("thuoc.csv",
    ["Tên thương phẩm", "Hoạt chất", "Nhóm", "Công ty đăng ký",
     "Cây trồng", "Dịch hại", "Ghi chú sửa đổi"],
    [[b["ten_thuong_pham"], b["hoat_chat"] or "", b["nhom"] or "", b["cong_ty"] or "",
      "; ".join(b["cay_trong"]), "; ".join(b["dich_hai"]), b.get("sua_doi", "")]
     for b in thuoc])

# 2) Một dòng một cặp (thuốc, cây, dịch hại) — dạng dài, lọc bằng Excel tiện nhất.
#    Đây mới là bảng trả lời được câu "cây X bị Y thì dùng thuốc nào".
dai = []
for b in thuoc:
    for o in b["doi_tuong"]:
        for cay in o["cay_trong"]:
            for dh in o["dich_hai"]:
                dai.append([cay, dh, b["ten_thuong_pham"], b["hoat_chat"] or "",
                            b["nhom"] or "", b["cong_ty"] or ""])
dai.sort(key=lambda r: (r[0], r[1], r[2]))
ghi("thuoc-theo-cay-va-dich-hai.csv",
    ["Cây trồng", "Dịch hại", "Tên thương phẩm", "Hoạt chất", "Nhóm", "Công ty"], dai)

# 3) Danh mục cấm
ghi("hoat-chat-cam.csv", ["Hoạt chất", "Nhóm"],
    [[c["hoat_chat"], c["nhom"]] for c in J("danh-muc-cam.json")["hoat_chat"]])

# 4) Ngưỡng dư lượng
ghi("mrl.csv",
    ["Hoạt chất", "Thực phẩm", "MRL (mg/kg)", "ADI", "Mã Codex", "Ghi chú"],
    [[m["hoat_chat"], m["thuc_pham"],
      "" if m["mrl_mg_kg"] is None else m["mrl_mg_kg"],
      m["adi"] or "", m["ma_codex"] or "", m["ghi_chu"] or ""]
     for m in J("mrl.json")["mrl"]])

# 5) Đếm số thuốc theo cây — để biết cây nào dữ liệu dày, cây nào mỏng
dem = {}
for b in thuoc:
    for c in b["cay_trong"]:
        dem[c] = dem.get(c, 0) + 1
ghi("so-thuoc-theo-cay.csv", ["Cây trồng", "Số thuốc đăng ký"],
    sorted(dem.items(), key=lambda x: -x[1]))

print("\nXong. Mo thu muc csv/ bang Excel.")
