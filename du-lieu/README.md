# Dữ liệu danh mục thuốc BVTV

## Nguồn

**Phụ lục I Thông tư 75/2025/TT-BNNMT** — Danh mục thuốc bảo vệ thực vật được
phép sử dụng tại Việt Nam. Hiệu lực 10/02/2026.

Tải từ: https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/12/75-bnnmt-pl1.pdf
(355 trang, 6,77 MB)

Đã sửa đổi bởi **Thông tư 28/2026/TT-BNNMT** (hiệu lực 15/08/2026) — **chưa gộp
vào đây**, còn phải làm.

## File

| File | Nội dung |
|---|---|
| `parse-danh-muc.py` | Bộ parse PDF → JSON |
| `danh-muc-thuoc.json` | Kết quả, 5.651 bản ghi |
| `bao-cao-parse.txt` | Báo cáo chất lượng, sinh cùng lúc |
| `*.pdf`, `*.txt` | File gốc — không commit, tải lại được |

Chạy lại: `pip install pymupdf` rồi `python parse-danh-muc.py <file.pdf>`

## Cấu trúc một bản ghi

```json
{
  "phan": "Thuốc Sử Dụng Trong Nông Nghiệp",
  "nhom": "Thuốc trừ sâu",
  "hoat_chat": "Abamectin (min 90%)",
  "ten_thuong_pham": "Tervigo 020SC",
  "cong_ty": "Công ty TNHH Syngenta Việt Nam",
  "doi_tuong": [{"dich_hai": ["tuyến trùng"],
                 "cay_trong": ["cà phê", "hồ tiêu", "sầu riêng"]}],
  "cay_trong": ["cam", "cà phê", "hồ tiêu", "khoai tây", "sầu riêng", "thanh long"],
  "dich_hai": ["tuyến trùng"]
}
```

`doi_tuong` giữ đúng cặp dịch hại–cây trồng như văn bản gốc. `cay_trong` và
`dich_hai` là bản gộp phẳng để tra nhanh.

## Quy mô

5.651 tên thương phẩm · 2.181 hoạt chất · 657 công ty đăng ký

| Nhóm | Số sản phẩm |
|---|---|
| Thuốc trừ sâu | 2.200 |
| Thuốc trừ bệnh | 1.968 |
| Thuốc trừ cỏ | 1.012 |
| Thuốc điều hoà sinh trưởng | 222 |
| Thuốc trừ ốc | 166 |
| Thuốc trừ chuột | 39 |

## Chất lượng

- Không tách được cây trồng: **15 bản ghi (0,3%)**
- Tên cây còn dính lỗi cú pháp: **0**

Còn khoảng 1–2% nhiễu: vài từ chỉ dịch hại ("rệp", "sâu", "bọ") lọt sang danh
sách cây trồng, do văn bản gốc có chỗ thiếu dấu `;` ngăn nhóm. Nhận ra được vì
chúng không phải tên cây.

Bản parse đầu tiên tự dò ranh giới hàng theo toạ độ, hỏng 1.279/6.294 bản ghi vì
tên thuốc xuống dòng bị dính vào bản ghi trước. Bản hiện tại dùng `find_tables()`
đọc đường kẻ của bảng nên gộp ô nhiều dòng đúng.

## HAI THỨ KHÔNG CÓ TRONG DỮ LIỆU NÀY

**1. Thời gian cách ly (PHI).** Không nằm trong Thông tư — in trên nhãn từng
thuốc. Phải gom riêng. Đây vẫn là việc chặn cứng của dự án.

**2. Phân bón.** Do hệ thống khác quản lý, theo Thông tư 07/2026/TT-BNNMT
(hiệu lực 23/01/2026). Tra ở https://www.masophanbon.com/

## Đã gộp sửa đổi 2026

`gop-sua-doi.py` gộp thêm hai nguồn:

**Phụ lục II Thông tư 75/2025 — DANH MỤC CẤM** → `danh-muc-cam.json`
33 hoạt chất bị cấm (25 trừ sâu/bảo quản lâm sản, 6 trừ bệnh, 1 trừ chuột,
1 trừ cỏ). App phải chặn, không được im lặng bỏ qua.

**Phụ lục Thông tư 28/2026** (hiệu lực 15/08/2026) → `danh-muc-thuoc-2026.json`

| Mục | Đọc được | Áp được |
|---|---|---|
| Đổi tổ chức đăng ký | 20 | **19** |
| Đổi thông tin hoạt chất | 2 | 1 |
| Tự nguyện rút khỏi danh mục | 5 | 4 |
| Bổ sung mới | 345 | 282 |

Con số 19 khớp đúng bản tóm tắt chính thức của Thông tư. Phần đọc được nhiều
hơn áp được là do tên thương phẩm không khớp bản ghi nào trong danh mục gốc,
hoặc trùng tên đã có.

**Tổng sau khi gộp: 5.929 bản ghi**, 15 bản (0,25%) không tách được cây trồng.

Hai lỗi đã sửa trong lúc làm, ghi lại để khỏi lặp:
1. Mốc cột của Thông tư 28 tôi *đoán* thay vì *đo* → lệch đúng một cột, khớp
   được 0 bản ghi. Phải đo phân bố x của chính file đó.
2. Gán mục theo TRANG → trang 2 chứa cả tiêu đề mục 2 lẫn mục 3, nên các thuốc
   *đổi hoạt chất* bị tính nhầm thành *đã rút khỏi danh mục*. Rút nghĩa là xoá,
   nên lỗi này nguy hiểm. Phải gán theo vị trí dọc của từng hàng.

## Việc còn lại

- [ ] Chuẩn hoá tên cây trồng ("cải bắp" vs "bắp cải", "lúa" vs "lúa gieo thẳng")
- [ ] Lọc bỏ ~1% từ chỉ dịch hại lọt sang cột cây trồng
- [ ] Gom PHI cho nhóm thuốc phổ biến nhất
