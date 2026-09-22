#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse Phụ lục I Thông tư 75/2025/TT-BNNMT ra JSON.

Vì sao dùng find_tables() của PyMuPDF chứ không tự dò hàng:
Bản đầu tôi tự xếp từ theo toạ độ. Cột thì đúng, nhưng RANH GIỚI HÀNG thì
sai — tên thuốc xuống dòng (ví dụ "Abakill" rồi dòng sau "3.6EC, 10WP")
bị dính vào bản ghi trước, làm hỏng 1.279/6.294 bản ghi. find_tables()
đọc đường kẻ của bảng nên gộp ô nhiều dòng đúng.

Bảng có 5 cột: TT | hoạt chất | tên thương phẩm | đối tượng phòng trừ | công ty.
Trang tiếp nối thường thiếu hai cột đầu, nên phải ánh xạ cột theo TOẠ ĐỘ x
chứ không theo thứ tự, và nhớ hoạt chất của hàng trước.

Chạy:  python parse-danh-muc.py thong-tu-75-2025-phu-luc-1.pdf
Ra:    danh-muc-thuoc.json  +  bao-cao-parse.txt
"""
import sys, os, re, json, io, collections

try:
    import fitz  # PyMuPDF >= 1.23
except ImportError:
    sys.exit("Thiếu PyMuPDF. Cài bằng: pip install pymupdf")

# Ranh giới cột đo từ phân bố x trên 57 trang (khổ ngang 842pt)
COT = [90, 245, 375, 642]
SO_COT = len(COT) + 1

RE_NHOM = re.compile(r'^\s*\d{1,2}\s*\.\s*(Thuốc[^:\n]{0,40})\s*:?\s*$')
RE_PHAN = re.compile(r'^\s*(I{1,3}|IV|V|VI|VII|VIII)\s*\.\s*(THUỐC[^:\n]{0,60})\s*[:.]?\s*$')
# Dòng tiêu đề bảng lặp lại ở mỗi trang — phải bỏ, nếu không thành bản ghi rác
RE_TIEUDE = re.compile(r'(TRADE NAME|COMMON NAME|PEST\s*/\s*CROP|APPLICANT|HOẠT CHẤT)', re.I)

# Mã dạng thuốc đứng đầu chuỗi (100SP, 3.6EC) hoặc chuỗi còn dấu hai chấm.
# Một sản phẩm nhiều dạng thì nguồn ghi "100SP: sâu cuốn lá/ lúa; 200WP: …",
# tách ra có lúc lọt nguyên mã sang cột cây trồng. Không lọc thì Excel hiện
# "100SP" như một loại cây.
RE_RAC = re.compile(r'^\s*\d+(?:[.,]\d+)?\s?[A-Z]{2,4}\b\s*:?\s*$', re.I)
# Mã dạng thuốc nằm GIỮA chuỗi: "ngô 600FS: xử lý hạt giống trừ …".
# Phần TRƯỚC mã mới là tên cây, nên cắt lấy phần đó chứ không vứt cả dòng.
RE_CAT = re.compile(r'^(.*?)\s*\d+(?:[.,]\d+)?\s?[A-Z]{2,4}\s*:.*$', re.I)


def go_ma_dang(x):
    """'ngô 600FS: xử lý hạt giống' -> 'ngô'; '100SP' -> '' (bỏ)"""
    x = (x or '').strip()
    m = RE_CAT.match(x)
    if m:
        x = m.group(1).strip(' ,;')
    return '' if (not x or RE_RAC.match(x)) else x


def cot_cua(x):
    for i, m in enumerate(COT):
        if x < m:
            return i
    return len(COT)


def sach(s):
    #   la khoang trang khong ngat, PDF dung nhieu -> doi tuong minh truoc
    return re.sub(r'\s+', ' ', (s or '').replace(' ', ' ')).strip(' .;')


def tach_doi_tuong(s):
    """
    'sâu đục thân, sâu cuốn lá/ lúa; bọ cánh tơ/ chè'
      -> [{'dich_hai': [...], 'cay_trong': ['lúa']}, ...]

    Nguồn dùng ';' ngăn các nhóm, '/' ngăn dịch hại với cây trồng, ',' ngăn
    các mục trong cùng nhóm. Bỏ tiền tố dạng thuốc kiểu '36EC:' vì nó chỉ
    nói liều nào dùng cho nhóm nào, không phải tên cây.
    """
    kq = []
    if not s:
        return kq
    s = s.replace('\n', ' ')
    for doan in re.split(r';', s):
        doan = sach(doan)
        if not doan or '/' not in doan:
            continue
        doan = re.sub(r'^[\d.,\s]*[A-Z]{2,4}\s*:\s*', '', doan)
        trai, phai = doan.split('/', 1)
        # Nếu vế phải còn '/' thì nguồn thiếu dấu ';' — cắt tại khoảng trắng
        # cuối cùng trước dấu '/' đó, phần sau xử lý như một nhóm mới.
        du = None
        if '/' in phai:
            vt = phai.index('/')
            cat = phai.rfind(' ', 0, vt)
            if cat > 0:
                du, phai = phai[cat:].strip(), phai[:cat]
        dh = [sach(t) for t in trai.split(',') if sach(t)]
        ct = [sach(t) for t in phai.split(',') if sach(t)]
        # Lọc rác: mã dạng thuốc (100SP, 3.6EC, "105SG: nhện") lọt sang cột
        # cây trồng khi một sản phẩm có nhiều dạng, mỗi dạng một đối tượng.
        # Không lọc thì Excel hiện "100SP" như một loại cây.
        ct = [y for y in (go_ma_dang(c) for c in ct) if y]
        dh = [y for y in (go_ma_dang(d) for d in dh) if y]
        if ct:
            kq.append({"dich_hai": dh, "cay_trong": ct})
        if du:
            kq.extend(tach_doi_tuong(du))
    return kq


def parse(duong_dan, moi_trang=None):
    d = fitz.open(duong_dan)
    ban_ghi = []
    phan = nhom = hoat_chat = None

    for i in range(d.page_count):
        trang = d[i]
        if moi_trang:
            moi_trang(i + 1, d.page_count)

        # Tiêu đề phân nhóm nằm NGOÀI bảng, phải đọc riêng từ text
        for line in trang.get_text().split('\n'):
            m = RE_PHAN.match(line.strip())
            if m:
                phan, nhom = m.group(2).strip().title(), None
            m = RE_NHOM.match(line.strip())
            if m:
                nhom = m.group(1).strip()

        for bang in trang.find_tables().tables:
            # Ánh xạ cột MỘT LẦN cho cả bảng thay vì gọi get_textbox từng ô
            # (get_textbox tốn ~1s/trang, extract() gần như tức thì).
            # Trang tiếp nối thiếu hai cột đầu nên phải map theo toạ độ x.
            anh_xa = None
            for hang in bang.rows:
                if hang.cells and any(hang.cells):
                    anh_xa = [cot_cua(b[0]) if b else None for b in hang.cells]
                    break
            if not anh_xa:
                continue

            for hang_txt in bang.extract():
                o = [''] * SO_COT
                for j, val in enumerate(hang_txt):
                    if val and j < len(anh_xa) and anh_xa[j] is not None:
                        k = anh_xa[j]
                        o[k] = (o[k] + ' ' + val).strip()

                tt, hc, tp, dt, ct = [sach(x) for x in o]
                if RE_TIEUDE.search(' '.join(o)):      # bỏ dòng tiêu đề lặp
                    continue
                if hc:
                    hoat_chat = hc                      # hoạt chất mới
                if not tp:
                    continue                            # không có tên thương phẩm thì không phải bản ghi

                dsdt = tach_doi_tuong(dt)
                ban_ghi.append({
                    "phan": phan,
                    "nhom": nhom,
                    "hoat_chat": hoat_chat,
                    "ten_thuong_pham": tp,
                    "cong_ty": ct,
                    "doi_tuong": dsdt,
                    "cay_trong": sorted({c for x in dsdt for c in x["cay_trong"]}),
                    "dich_hai": sorted({h for x in dsdt for h in x["dich_hai"]}),
                })
    return ban_ghi


def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else "thong-tu-75-2025-phu-luc-1.pdf"
    if not os.path.exists(pdf):
        sys.exit("Không thấy file: " + pdf)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    def tien_do(i, n):
        if i % 25 == 0 or i == n:
            print("  trang %d/%d" % (i, n), flush=True)

    ban_ghi = parse(pdf, tien_do)

    json.dump({
        "nguon": "Phụ lục I Thông tư 75/2025/TT-BNNMT (hiệu lực 10/02/2026)",
        "tai_tu": "https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/12/75-bnnmt-pl1.pdf",
        "luu_y": "Danh mục KHÔNG chứa thời gian cách ly (PHI) — PHI in trên nhãn từng thuốc.",
        "so_ban_ghi": len(ban_ghi),
        "thuoc": ban_ghi,
    }, io.open("danh-muc-thuoc.json", "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)

    # Báo cáo để kiểm được chất lượng, không phải tin suông
    cay = collections.Counter(c for b in ban_ghi for c in b["cay_trong"])
    nhom = collections.Counter(b["nhom"] or "(không rõ)" for b in ban_ghi)
    khong_cay = [b for b in ban_ghi if not b["cay_trong"]]
    con_gach = [b for b in ban_ghi if any('/' in c for c in b["cay_trong"])]

    r = io.open("bao-cao-parse.txt", "w", encoding="utf-8")
    r.write("TỔNG SỐ BẢN GHI: %d\n" % len(ban_ghi))
    r.write("Không tách được cây trồng: %d (%.1f%%)\n" % (
        len(khong_cay), 100.0 * len(khong_cay) / max(1, len(ban_ghi))))
    r.write("Tên cây còn dính dấu '/': %d (%.1f%%)\n\n" % (
        len(con_gach), 100.0 * len(con_gach) / max(1, len(ban_ghi))))
    r.write("--- THEO NHÓM ---\n")
    for k, v in nhom.most_common():
        r.write("%-34s %5d\n" % (k, v))
    r.write("\n--- 80 CÂY TRỒNG NHIỀU SẢN PHẨM NHẤT ---\n")
    for k, v in cay.most_common(80):
        r.write("%-30s %5d\n" % (k, v))
    r.write("\n--- TỔNG SỐ TÊN CÂY KHÁC NHAU: %d ---\n" % len(cay))
    r.write("\n--- 25 BẢN GHI KHÔNG RA CÂY (để soi lỗi) ---\n")
    for b in khong_cay[:25]:
        r.write("  %s | %s\n" % (b["ten_thuong_pham"][:40], (b["nhom"] or "")[:28]))
    r.close()
    print("Xong: %d ban ghi -> danh-muc-thuoc.json + bao-cao-parse.txt" % len(ban_ghi))


if __name__ == "__main__":
    main()
