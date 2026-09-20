#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gộp hai nguồn còn thiếu vào bộ dữ liệu:

1. Phụ lục II Thông tư 75/2025 — DANH MỤC CẤM (hoạt chất bị cấm dùng)
   -> danh-muc-cam.json
   App phải chặn: nếu người dùng nhập một thuốc có hoạt chất trong danh sách
   này thì cảnh báo, chứ không chỉ im lặng bỏ qua.

2. Phụ lục Thông tư 28/2026 — SỬA ĐỔI Thông tư 75/2025 (hiệu lực 15/08/2026)
   Gồm 4 mục:
     I.1  đổi tổ chức/cá nhân đăng ký      -> cập nhật cong_ty
     I.2  đổi thông tin hoạt chất           -> cập nhật hoat_chat
     I.3  tự nguyện rút khỏi danh mục       -> XOÁ khỏi danh mục
     II   bổ sung thuốc mới                 -> THÊM vào danh mục
   -> danh-muc-thuoc-2026.json

Chạy: python gop-sua-doi.py
"""
import sys, os, re, json, io, collections

try:
    import fitz
except ImportError:
    sys.exit("Thiếu PyMuPDF. Cài bằng: pip install pymupdf")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GOC   = "danh-muc-thuoc.json"
PL2   = "thong-tu-75-2025-phu-luc-2.pdf"
TT28  = "thong-tu-28-2026-phu-luc.pdf"


def sach(s):
    return re.sub(r'\s+', ' ', (s or '').replace(' ', ' ')).strip(' .;')


def chuan(s):
    """Khoá so khớp tên thương phẩm: bỏ khoảng trắng, bỏ dấu, thường hoá.
    Cần vì nguồn viết 'Miktin 3.6 EC' chỗ này, 'Miktin 3.6EC' chỗ kia."""
    return re.sub(r'[^0-9a-zA-ZÀ-ỹ]', '', (s or '')).lower()


# ---------------------------------------------------------------- DANH MỤC CẤM
def doc_danh_muc_cam(path):
    d = fitz.open(path)
    txt = "\n".join(p.get_text() for p in d)
    nhom, kq = None, []
    for line in txt.split("\n"):
        s = sach(line)
        if not s:
            continue
        if re.match(r'^Thuốc (trừ|bảo quản)', s) and len(s) < 60:
            nhom = s
            continue
        # Dòng dữ liệu: "1  Aldrin" hoặc chỉ "Aldrin" (số nằm dòng riêng)
        m = re.match(r'^\d{1,3}\s+(.{2,80})$', s)
        ten = m.group(1) if m else (s if nhom and not s.isdigit() and
                                    not s.startswith(("Phụ lục", "DANH MỤC", "(Ban hành",
                                                      "TT", "HOẠT CHẤT", "của Bộ")) else None)
        if ten and nhom:
            ten = sach(ten)
            if ten and not ten.isdigit() and len(ten) > 1:
                kq.append({"nhom": nhom, "hoat_chat": ten})
    return kq


# ------------------------------------------------------------ THÔNG TƯ 28/2026
# Mốc cột ĐO từ phân bố x của chính file này, không suy từ file kia sang.
# Lần trước tôi đoán nên lệch đúng một cột: ô "hoạt chất" thật ra là tên
# thương phẩm, và không khớp được bản ghi nào.
# Bốn khoảng trống đo được: 50→80, 220→255, 345→400, 580→615
COT_SUA = [65, 235, 375, 600]       # TT | hoạt chất | tên TP | nội dung cũ | nội dung mới
COT_MOI = [65, 235, 375, 600]       # TT | hoạt chất | tên TP | đối tượng | công ty


def cot_cua(x, moc):
    for i, m in enumerate(moc):
        if x < m:
            return i
    return len(moc)


def doc_bang(trang, moc):
    """Trả các hàng của mọi bảng trên trang kèm toạ độ y, đã ánh xạ cột theo x."""
    ra = []
    for bang in trang.find_tables().tables:
        anh_xa = None
        for h in bang.rows:
            if h.cells and any(h.cells):
                anh_xa = [cot_cua(b[0], moc) if b else None for b in h.cells]
                break
        if not anh_xa:
            continue
        ys = [min((b[1] for b in h.cells if b), default=0.0) for h in bang.rows]
        for idx, hang in enumerate(bang.extract()):
            o = [''] * (len(moc) + 1)
            for j, v in enumerate(hang):
                if v and j < len(anh_xa) and anh_xa[j] is not None:
                    k = anh_xa[j]
                    o[k] = (o[k] + ' ' + v).strip()
            ra.append((ys[idx] if idx < len(ys) else 0.0, [sach(x) for x in o]))
    return ra


# Tiêu đề mục và mẫu nhận dạng
MUC = [("cty",  r'1\.\s*Các thuốc bảo vệ thực vật thay đổi thông tin liên quan đến tổ chức'),
       ("hc",   r'2\.\s*Các thuốc bảo vệ thực vật thay đổi thông tin liên quan đến hoạt chất'),
       ("rut",  r'3\.\s*Các thuốc bảo vệ thực.{0,60}tự nguyện rút'),
       ("them", r'Phụ lục II')]


def doc_tt28(path):
    """
    Tách 4 mục của Thông tư 28.

    Gán mục theo VỊ TRÍ DỌC của từng hàng, không theo trang: trang 2 chứa cả
    tiêu đề mục 2 lẫn mục 3, nếu gán theo trang thì các hàng đổi hoạt chất bị
    tính nhầm thành hàng đã rút khỏi danh mục — sai nguy hiểm, vì rút nghĩa là
    xoá khỏi danh mục.
    """
    d = fitz.open(path)
    muc = None
    doi_cty, doi_hc, rut, them = [], [], [], []

    for i in range(d.page_count):
        trang = d[i]
        # Vị trí y của các tiêu đề mục trên trang này
        moc_muc = []
        for ten, mau in MUC:
            for kh in re.finditer(mau, trang.get_text()):
                for r in trang.search_for(trang.get_text()[kh.start():kh.start() + 40]) or []:
                    moc_muc.append((r.y0, ten))
                    break
        moc_muc.sort()

        for y, o in doc_bang(trang, COT_SUA):
            for ymuc, ten in moc_muc:              # mục gần nhất PHÍA TRÊN hàng
                if ymuc <= y + 2:
                    muc = ten
            if muc is None:
                continue

            tt, hc, tp, c4, c5 = o
            ca_dong = ' '.join(o)
            if not tp or re.search(r'(Trade name|Common name|Tên thương phẩm|Nội dung)', ca_dong, re.I):
                continue

            if muc == "them":
                them.append({"hoat_chat": hc, "ten_thuong_pham": tp,
                             "doi_tuong_raw": c4, "cong_ty": c5})
            else:
                r = {"hoat_chat": hc, "ten_thuong_pham": tp, "cu": c4, "moi": c5}
                (doi_cty if muc == "cty" else doi_hc if muc == "hc" else rut).append(r)
    return doi_cty, doi_hc, rut, them


# ------------------------------------------------------------------------ MAIN
def main():
    for f in (GOC, PL2, TT28):
        if not os.path.exists(f):
            sys.exit("Thiếu file: " + f)

    # 1. Danh mục cấm
    cam = doc_danh_muc_cam(PL2)
    json.dump({
        "nguon": "Phụ lục II Thông tư 75/2025/TT-BNNMT",
        "mo_ta": "Hoạt chất CẤM sử dụng tại Việt Nam",
        "so_hoat_chat": len(cam), "hoat_chat": cam,
    }, io.open("danh-muc-cam.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # 2. Sửa đổi 2026
    doi_cty, doi_hc, rut, them = doc_tt28(TT28)

    goc = json.load(io.open(GOC, encoding="utf-8"))
    thuoc = goc["thuoc"]
    chi_so = collections.defaultdict(list)
    for b in thuoc:
        chi_so[chuan(b["ten_thuong_pham"])].append(b)

    dem = collections.Counter()

    for r in doi_cty:
        for b in chi_so.get(chuan(r["ten_thuong_pham"]), []):
            b["cong_ty"] = r["moi"] or b["cong_ty"]
            b["sua_doi"] = "TT28/2026: đổi tổ chức đăng ký"
            dem["doi_cty"] += 1
    for r in doi_hc:
        for b in chi_so.get(chuan(r["ten_thuong_pham"]), []):
            b["hoat_chat"] = r["moi"] or b["hoat_chat"]
            b["sua_doi"] = "TT28/2026: đổi thông tin hoạt chất"
            dem["doi_hc"] += 1

    bo = {chuan(r["ten_thuong_pham"]) for r in rut}
    truoc = len(thuoc)
    thuoc = [b for b in thuoc if chuan(b["ten_thuong_pham"]) not in bo]
    dem["da_rut"] = truoc - len(thuoc)

    # Dùng lại đúng bộ tách "đối tượng phòng trừ" của parse-danh-muc.py, nếu
    # không thì 282 thuốc mới sẽ không có cay_trong và biến mất khỏi bộ lọc
    # theo cây — lỗi im lặng, khó phát hiện.
    import importlib.util
    _s = importlib.util.spec_from_file_location("pdm", "parse-danh-muc.py")
    _m = importlib.util.module_from_spec(_s)
    _s.loader.exec_module(_m)
    tach = _m.tach_doi_tuong

    co = {chuan(b["ten_thuong_pham"]) for b in thuoc}
    for r in them:
        if chuan(r["ten_thuong_pham"]) in co:
            continue
        dsdt = tach(r["doi_tuong_raw"])
        thuoc.append({
            "phan": "Thuốc Sử Dụng Trong Nông Nghiệp", "nhom": None,
            "hoat_chat": r["hoat_chat"], "ten_thuong_pham": r["ten_thuong_pham"],
            "cong_ty": r["cong_ty"],
            "doi_tuong": dsdt,
            "cay_trong": sorted({c for x in dsdt for c in x["cay_trong"]}),
            "dich_hai": sorted({h for x in dsdt for h in x["dich_hai"]}),
            "sua_doi": "TT28/2026: bổ sung mới",
        })
        dem["them_moi"] += 1

    json.dump({
        "nguon": "Phụ lục I Thông tư 75/2025/TT-BNNMT, đã gộp sửa đổi của Thông tư 28/2026/TT-BNNMT",
        "hieu_luc": "Thông tư 75/2025 từ 10/02/2026; sửa đổi 28/2026 từ 15/08/2026",
        "luu_y": "Vẫn KHÔNG có thời gian cách ly (PHI) — PHI in trên nhãn từng thuốc.",
        "so_ban_ghi": len(thuoc), "thuoc": thuoc,
    }, io.open("danh-muc-thuoc-2026.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    r = io.open("bao-cao-gop.txt", "w", encoding="utf-8")
    r.write("DANH MỤC CẤM: %d hoạt chất\n" % len(cam))
    for n, v in collections.Counter(c["nhom"] for c in cam).most_common():
        r.write("  %-42s %3d\n" % (n, v))
    r.write("\nSỬA ĐỔI THEO THÔNG TƯ 28/2026\n")
    r.write("  Đọc được từ văn bản: %d đổi tổ chức, %d đổi hoạt chất, %d rút, %d bổ sung\n"
            % (len(doi_cty), len(doi_hc), len(rut), len(them)))
    r.write("  Áp được vào danh mục: %d đổi tổ chức, %d đổi hoạt chất, %d đã xoá, %d thêm mới\n"
            % (dem["doi_cty"], dem["doi_hc"], dem["da_rut"], dem["them_moi"]))
    r.write("\nTỔNG SỐ BẢN GHI SAU KHI GỘP: %d (trước %d)\n" % (len(thuoc), truoc))
    r.close()
    print("Xong. Xem bao-cao-gop.txt")


if __name__ == "__main__":
    main()
