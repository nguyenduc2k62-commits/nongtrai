#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng bộ dữ liệu gọn cho app từ các file đã parse.

Vì sao không nạp thẳng file gốc: danh-muc-thuoc-2026.json 3,5 MB +
mrl.json 1,2 MB, mà app chỉ cần một phần. Ở đây gom lại, bỏ trường không
dùng, và GOM CHUỖI LẶP thành bảng tra (tên công ty, tên cây, tên dịch hại
lặp hàng nghìn lần).

Ra: ../du-lieu-app.json  (app nạp file này lúc chạy)
"""
import json, io, re, sys, collections, os, gzip

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Nhóm hoạt chất dùng cho cảnh báo pha chung bình.
# ĐÂY LÀ PHÂN LOẠI SUY RA TỪ TÊN HOẠT CHẤT, không phải dữ liệu chính thức.
# App phải ghi rõ điều đó chứ không trình bày như quy định.
NHOM_HC = [
    ("dong",      r'\b(đồng|copper|cuprous|cupric|oxychloride|hydroxide\s*đồng)\b'),
    ("visinh",    r'\b(bacillus|trichoderma|streptomyces|metarhizium|beauveria|'
                  r'validamycin|paecilomyces|chaetomium|pseudomonas|saccharomyces|'
                  r'nucleopolyhedro|granulosis|abamectin|emamectin|spinosad|'
                  r'azadirachtin|matrine|rotenone|saponin)\b'),
    ("khangsinh", r'\b(kasugamycin|streptomycin|oxytetracycline|ningnanmycin|'
                  r'polyoxin|gentamycin|zhongshengmycin)\b'),
    ("dau",       r'\b(dầu khoáng|petroleum oil|paraffinic|mineral oil)\b'),
    ("luuhuynh",  r'\b(sulfur|lưu huỳnh)\b'),
]


def nhom_hoat_chat(hc):
    s = (hc or "").lower()
    ra = [ten for ten, mau in NHOM_HC if re.search(mau, s)]
    return ra or ["hoahoc"]


def chuan_hc(s):
    if not s:
        return ""
    s = re.sub(r'\([^)]*\)', ' ', s)
    s = re.sub(r'\d+(?:[.,]\d+)?\s*%', ' ', s)
    return re.sub(r'[^0-9a-z]', '', s.lower())


def tach_hc(s):
    return [k for k in (chuan_hc(p) for p in re.split(r'[+]', s or "")) if len(k) > 2]


class Bang:
    """Bảng tra chuỗi: trả về chỉ số thay vì lặp lại chuỗi."""
    def __init__(self):
        self.ds, self.chi = [], {}

    def __call__(self, s):
        if s is None:
            return None
        if s not in self.chi:
            self.chi[s] = len(self.ds)
            self.ds.append(s)
        return self.chi[s]


def main():
    thuoc = json.load(io.open("danh-muc-thuoc-2026.json", encoding="utf-8"))["thuoc"]
    cam = json.load(io.open("danh-muc-cam.json", encoding="utf-8"))["hoat_chat"]
    mrl_hc = json.load(io.open("mrl-theo-hoat-chat.json", encoding="utf-8"))["hoat_chat"]
    anhxa = json.load(io.open("anh-xa-cay-thuc-pham.json", encoding="utf-8"))["anh_xa"]

    CAY, DH, CTY, HC = Bang(), Bang(), Bang(), Bang()
    NHOM = {"Thuốc trừ sâu": 0, "Thuốc trừ bệnh": 1, "Thuốc trừ cỏ": 2,
            "Thuốc điều hoà sinh trưởng": 3, "Thuốc trừ ốc": 4, "Thuốc trừ chuột": 5}

    ra = []
    for t in thuoc:
        if not t["cay_trong"]:
            continue                                  # không có cây thì app không dùng được
        # cặp (dịch hại, cây) giữ đúng như văn bản gốc — quan trọng vì một
        # thuốc đăng ký trị sâu A trên cây X, không có nghĩa trị được trên cây Y
        cap = []
        for o in t["doi_tuong"]:
            for c in o["cay_trong"]:
                for h in o["dich_hai"]:
                    cap.append([DH(h), CAY(c)])
        ra.append({
            "t": t["ten_thuong_pham"],
            "h": HC(t["hoat_chat"]),
            "n": NHOM.get(t["nhom"]),
            "y": CTY(t["cong_ty"]),
            "c": sorted({CAY(c) for c in t["cay_trong"]}),
            "p": cap,
            "g": nhom_hoat_chat(t["hoat_chat"]),
        })

    # MRL: chỉ giữ hoạt chất thực sự có trong danh mục
    dung = set()
    for t in thuoc:
        dung.update(tach_hc(t["hoat_chat"]))
    mrl = {k: {"ten": v["ten"],
               "muc": [[m["thuc_pham"], m["mrl_mg_kg"]] for m in v["muc"]
                       if m["mrl_mg_kg"] is not None]}
           for k, v in mrl_hc.items() if k in dung}

    out = {
        "nguon": {
            "thuoc": "Phụ lục I Thông tư 75/2025/TT-BNNMT + sửa đổi 28/2026/TT-BNNMT",
            "cam": "Phụ lục II Thông tư 75/2025/TT-BNNMT",
            "mrl": "Thông tư 50/2016/TT-BYT (tham chiếu CODEX/ASEAN 2016)",
        },
        "canh_bao": {
            "phi": "Dữ liệu KHÔNG có thời gian cách ly. PHI in trên nhãn từng thuốc — người dùng phải tự đọc và nhập.",
            "nhom_pha": "Nhóm hoạt chất dùng cho cảnh báo pha chung là SUY RA TỪ TÊN, không phải quy định chính thức.",
            "mrl": "Chỉ 26% số thuốc có ngưỡng MRL. Không có ngưỡng thì phải báo 'chưa có', không được đoán.",
        },
        "bang": {"cay": CAY.ds, "dich_hai": DH.ds, "cong_ty": CTY.ds, "hoat_chat": HC.ds},
        "nhom": list(NHOM.keys()),
        "thuoc": ra,
        "cam": [c["hoat_chat"] for c in cam],
        "mrl": mrl,
        "anh_xa_cay_thuc_pham": anhxa,
    }

    p = os.path.join("..", "du-lieu-app.json")
    json.dump(out, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    n = os.path.getsize(p)
    nz = len(gzip.compress(io.open(p, "rb").read()))

    dem = collections.Counter()
    for t in ra:
        for c in t["c"]:
            dem[CAY.ds[c]] += 1
    print("Thuốc: %d | cây: %d | dịch hại: %d | công ty: %d"
          % (len(ra), len(CAY.ds), len(DH.ds), len(CTY.ds)))
    print("Hoạt chất có MRL dùng được: %d | hoạt chất cấm: %d" % (len(mrl), len(cam)))
    print("Kích thước: %.1f KB (nén gzip %.1f KB)" % (n / 1024, nz / 1024))
    print("10 cây nhiều thuốc nhất:", ", ".join("%s %d" % kv for kv in dem.most_common(10)))


if __name__ == "__main__":
    main()
