#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse Thông tư 50/2016/TT-BYT — Giới hạn tối đa dư lượng thuốc BVTV trong
thực phẩm (MRL) — ra JSON, rồi NỐI với danh mục thuốc BVTV đã có.

MRL là ngưỡng thật quyết định lô hàng bị trả về hay không (mg/kg). PHI chỉ
là cách vận hành để dư lượng tụt xuống dưới ngưỡng đó.

Bảng 8 cột, xác nhận bằng cách soi hàng có hoạt chất mới:
  0 TT | 1 mã Codex | 2 hoạt chất | 3 ADI | 4 định nghĩa dư lượng
  5 thực phẩm | 6 MRL (mg/kg) | 7 ghi chú
Bốn cột đầu chỉ xuất hiện ở hàng đầu của mỗi hoạt chất, các hàng sau để
trống — nên phải nhớ giá trị của hàng trước.

Chạy: python parse-mrl.py
Ra:   mrl.json · mrl-theo-hoat-chat.json · bao-cao-mrl.txt
"""
import sys, os, re, json, io, collections

try:
    import fitz
except ImportError:
    sys.exit("Thiếu PyMuPDF. Cài bằng: pip install pymupdf")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PDF = "thong-tu-50-2016-mrl.pdf"
DANH_MUC = "danh-muc-thuoc-2026.json"


def noi_thuong(s):
    """Nối các dòng bằng khoảng trắng. Dùng cho MỌI cột tiếng Việt."""
    return re.sub(r'\s+', ' ', (s or '').replace('\n', ' ')).strip()


def noi_hoat_chat(s):
    """
    Riêng cột tên hoạt chất: PDF ngắt dòng GIỮA TỪ ("Aminocyclopyrac" +
    "hlor"). Nối bằng khoảng trắng thì thành "Aminocyclopyrac hlor" — sai
    tên, không khớp được với gì. Hai bên đều là chữ thường thì nối liền.

    CHỈ dùng cho cột này. Áp cho cột tiếng Việt thì hỏng: tiếng Việt ngắt
    dòng ở ranh giới TỪ, nên "Sữa nguyên liệu" sẽ thành "Sữanguyênliệu".
    """
    if not s:
        return ""
    phan = [p.strip() for p in s.split("\n") if p.strip()]
    if not phan:
        return ""
    ra = phan[0]
    for p in phan[1:]:
        # chỉ nối liền khi cả hai bên là chữ Latin không dấu viết thường
        if ra and re.match(r'[a-z]', ra[-1]) and re.match(r'[a-z]', p[0]):
            ra += p
        else:
            ra += " " + p
    return re.sub(r'\s+', ' ', ra).strip()


def so(s):
    """'0,3' -> 0.3 ; '0,01 (*)' -> 0.01 ; không đọc được -> None"""
    if not s:
        return None
    m = re.search(r'(\d+(?:[.,]\d+)?)', s)
    return float(m.group(1).replace(',', '.')) if m else None


def chuan_hc(s):
    """
    Khoá so khớp hoạt chất giữa hai văn bản.
    Danh mục BVTV ghi 'Abamectin (min 90%)', Thông tư 50 ghi 'Abamectin'.
    Bỏ phần trong ngoặc, bỏ hàm lượng, thường hoá, bỏ ký tự không phải chữ số.
    """
    if not s:
        return ""
    s = re.sub(r'\([^)]*\)', ' ', s)          # bỏ (min 90%), (Cd)...
    s = re.sub(r'\d+(?:[.,]\d+)?\s*%', ' ', s)  # bỏ 30%
    return re.sub(r'[^0-9a-z]', '', s.lower())


def tach_hoat_chat(s):
    """'Abamectin 2% + Chlorantraniliprole 8%' -> ['abamectin','chlorantraniliprole']"""
    if not s:
        return []
    return [k for k in (chuan_hc(p) for p in re.split(r'[+]', s)) if len(k) > 2]


# --------------------------------------------------------------------- PARSE
def parse_mrl(path):
    d = fitz.open(path)
    ban_ghi = []
    tt = ma = hc = adi = dn = None

    for i in range(d.page_count):
        for bang in d[i].find_tables().tables:
            for hang in bang.extract():
                c = [(x or "") for x in hang]
                if len(c) < 8:
                    c += [""] * (8 - len(c))
                # Cột 2 là tên hoá chất Latin, xử lý riêng; còn lại là tiếng Việt
                c = [(noi_hoat_chat(x) if j == 2 else noi_thuong(x))
                     for j, x in enumerate(c[:8])]

                if re.search(r'(Thực phẩm|Hoạt chất|MRL|Ghi chú|ADI)', " ".join(c), re.I):
                    continue                    # dòng tiêu đề lặp mỗi trang

                if c[2]:                        # hoạt chất mới
                    tt, ma, hc, adi, dn = c[0], c[1], c[2], c[3], c[4]

                if not hc or not c[5]:
                    continue

                ban_ghi.append({
                    "hoat_chat": hc,
                    "ma_codex": ma or None,
                    "adi": adi or None,
                    "dinh_nghia_du_luong": dn or None,
                    "thuc_pham": c[5],
                    "mrl_mg_kg": so(c[6]),
                    "mrl_goc": c[6] or None,
                    "ghi_chu": c[7] or None,
                })
    return ban_ghi


# ---------------------------------------------------------------------- MAIN
def main():
    if not os.path.exists(PDF):
        sys.exit("Thiếu file: " + PDF)

    print("Đang đọc %s ..." % PDF, flush=True)
    bg = parse_mrl(PDF)

    json.dump({
        "nguon": "Thông tư 50/2016/TT-BYT — Giới hạn tối đa dư lượng thuốc BVTV trong thực phẩm",
        "don_vi": "mg/kg thực phẩm",
        "tham_chieu": "Giá trị MRL tham chiếu từ CODEX và ASEAN tại thời điểm 2016",
        "canh_bao": "Hàng xuất khẩu phải theo ngưỡng của nước nhập, EU/Nhật/Trung Quốc mỗi nơi một khác.",
        "so_ban_ghi": len(bg), "mrl": bg,
    }, io.open("mrl.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # Gom theo hoạt chất để app tra nhanh
    theo_hc = collections.defaultdict(list)
    for b in bg:
        theo_hc[chuan_hc(b["hoat_chat"])].append(
            {"thuc_pham": b["thuc_pham"], "mrl_mg_kg": b["mrl_mg_kg"], "ghi_chu": b["ghi_chu"]})
    ten_hc = {}
    for b in bg:
        ten_hc.setdefault(chuan_hc(b["hoat_chat"]), b["hoat_chat"])

    json.dump({
        "mo_ta": "MRL gom theo khoá hoạt chất đã chuẩn hoá, để nối với danh mục thuốc BVTV",
        "so_hoat_chat": len(theo_hc),
        "hoat_chat": {k: {"ten": ten_hc[k], "muc": v} for k, v in theo_hc.items()},
    }, io.open("mrl-theo-hoat-chat.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # Nối thử với danh mục thuốc: bao nhiêu thuốc tra được MRL?
    khop = thieu = 0
    vi_du = []
    if os.path.exists(DANH_MUC):
        thuoc = json.load(io.open(DANH_MUC, encoding="utf-8"))["thuoc"]
        for t in thuoc:
            ks = tach_hoat_chat(t["hoat_chat"])
            co = [k for k in ks if k in theo_hc]
            if co:
                khop += 1
                if len(vi_du) < 5 and t["cay_trong"]:
                    vi_du.append((t["ten_thuong_pham"], ten_hc[co[0]],
                                  t["cay_trong"][:3], len(theo_hc[co[0]])))
            else:
                thieu += 1

    r = io.open("bao-cao-mrl.txt", "w", encoding="utf-8")
    r.write("TỔNG SỐ DÒNG MRL: %d\n" % len(bg))
    r.write("Số hoạt chất có MRL: %d\n" % len(theo_hc))
    r.write("Dòng không đọc được trị số MRL: %d\n\n" % sum(1 for b in bg if b["mrl_mg_kg"] is None))

    tp = collections.Counter(b["thuc_pham"] for b in bg)
    r.write("--- 30 THỰC PHẨM CÓ NHIỀU NGƯỠNG NHẤT ---\n")
    for k, v in tp.most_common(30):
        r.write("%-44s %4d\n" % (k[:44], v))
    r.write("\nTổng số loại thực phẩm khác nhau: %d\n" % len(tp))

    if khop or thieu:
        r.write("\n--- NỐI VỚI DANH MỤC THUỐC BVTV ---\n")
        r.write("Thuốc tra được MRL:      %5d\n" % khop)
        r.write("Thuốc CHƯA tra được MRL: %5d\n" % thieu)
        r.write("Tỉ lệ phủ: %.1f%%\n\n" % (100.0 * khop / max(1, khop + thieu)))
        for tp_, hc_, cay, n in vi_du:
            r.write("  %s (%s) — cây: %s — %d ngưỡng MRL\n"
                    % (tp_[:28], hc_[:22], ", ".join(cay), n))
    r.close()
    print("Xong: %d dong MRL, %d hoat chat. Xem bao-cao-mrl.txt" % (len(bg), len(theo_hc)))


if __name__ == "__main__":
    main()
