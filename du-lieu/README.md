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

---

# Các nguồn dữ liệu khác

## ĐÃ TẢI — chưa parse

### Thông tư 50/2016/TT-BYT — Giới hạn dư lượng tối đa (MRL)

`thong-tu-50-2016-mrl.pdf` · 183 trang · tải từ cổng Sở NN Lào Cai
(datafiles.chinhphu.vn không có, congbao.chinhphu.vn trả về HTML)

**Đây là con số quyết định lô hàng bị trả về hay không**, đơn vị mg/kg.
PHI chỉ là cách vận hành để dư lượng tụt xuống dưới MRL — MRL mới là ngưỡng
thật. Giá trị tham chiếu từ CODEX và ASEAN tại thời điểm 2016.

Cấu trúc: hoạt chất | ADI | định nghĩa dư lượng | rồi lặp (thực phẩm | MRL |
ghi chú). Khổ dọc A4, cột hẹp, chữ xuống dòng nhiều — parse được nhưng khó
hơn danh mục BVTV.

## CHƯA LẤY — lấy được miễn phí

| Nguồn | Nội dung | Ghi chú |
|---|---|---|
| [Open-Meteo](https://open-meteo.com/) | Thời tiết, dự báo + lịch sử từ 1940 | Không cần khoá, 10.000 lượt/ngày miễn phí. Dùng để tính tích ôn → dự đoán giai đoạn cây, và cảnh báo nguy cơ bệnh theo độ ẩm |
| [SoilGrids](https://soilgrids.org) (ISRIC) | pH, hữu cơ, sét/cát/limon, CEC, đạm tổng — lưới 250m toàn cầu | **API REST đang tạm dừng**, phải tải raster về tự tra |
| [PlantDoc](https://github.com/pratikkayal/PlantDoc-Dataset) | 2.598 ảnh bệnh chụp ngoài đồng | CC BY 4.0 |
| [Bugwood](https://www.bugwood.org) | Ảnh sâu bệnh, nhãn do chuyên gia đặt | Free cho giáo dục |
| [Codex MRL](https://www.fao.org/fao-who-codexalimentarius/codex-texts/dbs/pestres/en) | MRL quốc tế | Cần cho hàng xuất khẩu — EU, Nhật, Trung Quốc mỗi nơi một ngưỡng |

## CHƯA LẤY — khó hoặc phải xin

| Nguồn | Vướng ở đâu |
|---|---|
| Danh mục phân bón | [masophanbon.com](https://www.masophanbon.com/) chỉ tra từng mã, không có bản tải hàng loạt, chứng chỉ SSL hết hạn. Đường đúng là gửi văn bản xin Cục Trồng trọt và BVTV |
| PHI (thời gian cách ly) | Không nằm trong Thông tư nào — in trên nhãn từng thuốc. Phải gom tay từ nhãn hoặc trang đại lý |
| Mã số vùng trồng (PUC) | Cục BVTV quản lý, cần cho hàng xuất khẩu |
| Bảng tương kỵ khi pha | Nhà sản xuất công bố rời rạc, chưa có nguồn gộp |
| Nhóm độc GHS/WHO, mã kháng thuốc FRAC/IRAC/HRAC | [danhmuc.thuocbvtv.com](https://danhmuc.thuocbvtv.com/) có, nhưng không có API |

## ĐÃ CÓ SẴN trong dữ liệu — dễ bỏ sót

Danh mục BVTV đã parse chứa **546 tên sâu bệnh tiếng Việt gắn với cây trồng**,
lấy được miễn phí, phủ mọi cây chứ không riêng lúa. Đây là bộ từ vựng nền cho
phần tra bệnh, không cần đi tìm ở đâu khác.

Ví dụ: sầu riêng 28 loại (xì mủ, thán thư, rệp sáp, thối quả, nứt thân xì mủ,
thối rễ…), hồ tiêu 54 loại (chết nhanh, chết chậm, tuyến trùng…), cà phê 68
loại (rỉ sắt, rệp sáp, nấm hồng…), cao su 29 loại (nấm hồng, loét sọc mặt cạo,
vàng rụng lá…).
