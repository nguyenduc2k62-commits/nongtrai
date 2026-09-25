# Bàn giao — dự án Sổ Ruộng

Viết ngày 22/09/2026, cập nhật 24/09/2026 (mục 6: đợt sửa lỗi). Để một phiên làm việc mới đọc và tiếp tục được ngay mà
không cần hỏi lại.

---

## 0. Đọc gì trước

1. File này — bối cảnh, nguồn dữ liệu, bẫy đã gặp
2. `VIEC-CAN-LAM.md` — việc còn lại, xếp theo giá trị
3. `du-lieu/README.md` — chi tiết từng bộ dữ liệu

---

## 1. Toạ độ dự án

| Thứ | Ở đâu |
|---|---|
| Thư mục máy | `D:\Downloads\nôngapp` |
| GitHub | `nguyenduc2k62-commits/nongtrai` (**public**) |
| Trang chạy | https://nguyenduc2k62-commits.github.io/nongtrai/ |
| Người làm | Đức (`nguyenduc2k62@gmail.com`) |

**Tách hẳn khỏi dự án WhisperInk** (`D:\Downloads\dụ an c hằng`). Hai dự án
không liên quan. Đừng để lẫn — mở nhầm thư mục thì `CLAUDE.md` của WhisperInk
sẽ áp nhầm sang đây.

Đẩy code: `git push origin main`, rồi đợi ~1 phút GitHub Pages dựng lại.

---

## 2. Sản phẩm là gì

**Sổ Ruộng** — app nhật ký canh tác. Nông dân ghi một dòng vào sổ, app trả lại
**ngày sớm nhất được thu hoạch**, tính từ thời gian cách ly của thuốc đã dùng.

### Ba nguyên tắc, đừng lệch

**Giá trị nằm ở hồ sơ tuân thủ, không nằm ở tư vấn.** Đối thủ thật không phải
mấy app nông nghiệp đang ế, mà là chủ đại lý vật tư đầu làng — miễn phí, trả
lời trong 30 giây, bán luôn thuốc, cho nợ tới mùa. Không đấu được ở đó. Đấu ở
chỗ họ không làm: chứng minh với bên thu mua rằng lô hàng đạt dư lượng.

**Tra bệnh là móc câu, không phải sản phẩm.** Nông dân không có lý do gì mở một
app ghi chép. Họ có lý do mở app khi cây có bệnh. Vào rồi thì việc ghi chép xảy
ra như hệ quả.

**Người trả tiền là HTX và doanh nghiệp thu mua, không phải nông dân.** Họ bị
ép bởi quy định dư lượng của bên mua, hiện quản lý bằng Excel và ảnh chụp sổ
tay gửi Zalo. Một HTX gật đầu là có ngay vài chục hộ dùng.

### Hai khái niệm phải phân biệt

- **MRL** — giới hạn dư lượng tối đa còn lại trong nông sản (mg/kg). Đây là
  **ngưỡng**, bên thu mua đo cái này. Giống giới hạn nồng độ cồn khi lái xe.
- **PHI** — thời gian cách ly, số ngày phải chờ từ lúc xịt đến lúc thu hoạch.
  Đây là **cách làm** để dư lượng tụt xuống dưới MRL. Giống "uống rượu xong
  chờ 8 tiếng hãy lái xe".

---

## 3. Dữ liệu — lấy từ đâu, lấy kiểu gì

Tất cả nằm trong `du-lieu/`. File PDF gốc **không commit** (đã gitignore) vì
tải lại được bất cứ lúc nào.

### 3.1 Danh mục thuốc BVTV được phép

**Phụ lục I Thông tư 75/2025/TT-BNNMT** (hiệu lực 10/02/2026)

```
https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/12/75-bnnmt-pl1.pdf
```
355 trang · 6,77 MB · khổ ngang A4 · bảng 5 cột:
`TT | hoạt chất | tên thương phẩm | đối tượng phòng trừ | tổ chức đăng ký`

### 3.2 Danh mục CẤM

**Phụ lục II cùng Thông tư** — đoán được đường dẫn theo đúng mẫu Phụ lục I:

```
https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/12/75-bnnmt-pl2.pdf
```
2 trang · 218 KB · 33 hoạt chất cấm (Aldrin, DDT, Carbofuran, Endosulfan…)

### 3.3 Sửa đổi 2026

**Phụ lục Thông tư 28/2026/TT-BNNMT** (hiệu lực 15/08/2026)

`datafiles.chinhphu.vn` **không có** file này. Lấy từ cổng xã Xuân Thành,
Đồng Nai — bản đã ký:

```
https://xuanthanh.dongnai.gov.vn/vi/news/thong-tin-tuyen-truyen/thong-tu-sua-doi-bo-sung-thong-tu-so-75-2025-tt-bnnmt-ngay-26-12-2025-cua-bo-truong-bo-nong-nghiep-va-moi-truong-ve-ban-hanh-danh-muc-thuoc-bao-ve-thuc-vat-duoc-phep-su-dung-tai-viet-nam-va-danh-muc-thuoc-bao-ve-thuc-vat-cam-su-dung-tai-viet-nam-438.html?download=1&id=1
```
20 trang · 1,1 MB · 4 mục: đổi tổ chức đăng ký · đổi hoạt chất · tự nguyện rút ·
bổ sung mới

### 3.4 Ngưỡng dư lượng MRL

**Thông tư 50/2016/TT-BYT** — Bộ Y tế

`congbao.chinhphu.vn` trả về HTML chứ không phải PDF. Lấy từ cổng Sở NN Lào Cai:

```
https://storage-vnportal.vnpt.vn/lci-ubnd-responsive/sitefolders/snnptnt/6200/50_2016_tt-byt-du-luong-bvtv-trong-rau-cu-qua.pdf
```
183 trang · 3,5 MB · khổ dọc A4 · bảng 8 cột:
`TT | mã Codex | hoạt chất | ADI | định nghĩa dư lượng | thực phẩm | MRL | ghi chú`

### 3.5 Nguồn đã tra nhưng KHÔNG lấy được

| Nguồn | Vướng |
|---|---|
| Danh mục phân bón | [masophanbon.com](https://www.masophanbon.com/) chỉ tra từng mã, không có bản tải hàng loạt, **chứng chỉ SSL hết hạn**. Đường đúng là gửi văn bản xin Cục Trồng trọt và BVTV. Phân bón không có PHI nên không ảnh hưởng đồng hồ đếm ngược |
| **PHI** | Không nằm trong Thông tư nào — in trên nhãn từng chai. Phải gom tay, hoặc để người dùng nhập (app đang làm cách này) |
| Nhóm độc GHS/WHO, mã kháng thuốc FRAC/IRAC/HRAC | [danhmuc.thuocbvtv.com](https://danhmuc.thuocbvtv.com/) có, lấy từ hệ thống EcoFarm của Cục BVTV, nhưng không có API |
| Bảng tương kỵ khi pha | Nhà sản xuất công bố rời rạc |
| Mã số vùng trồng (PUC) | Cục BVTV quản lý, cần cho hàng xuất khẩu |

### 3.6 Nguồn miễn phí chưa dùng

- **[Open-Meteo](https://open-meteo.com/)** — thời tiết, không cần khoá, lịch sử
  từ 1940, 10.000 lượt/ngày. Mở ra: tính tích ôn → dự đoán giai đoạn cây, cảnh
  báo nguy cơ bệnh theo độ ẩm
- **[SoilGrids](https://soilgrids.org)** (ISRIC) — pH, hữu cơ, sét/cát/limon,
  CEC, đạm, lưới 250m. **API REST đang tạm dừng**, phải tải raster
- **[PlantDoc](https://github.com/pratikkayal/PlantDoc-Dataset)** — 2.598 ảnh
  bệnh chụp ngoài đồng, **CC BY 4.0**, chỉ cần trích dẫn
- **[Bugwood](https://www.bugwood.org)** — ảnh sâu bệnh, nhãn do chuyên gia đặt
- **[Codex MRL](https://www.fao.org/fao-who-codexalimentarius/codex-texts/dbs/pestres/en)**
  — ngưỡng quốc tế, cần cho hàng xuất khẩu

---

## 4. Dây chuyền xử lý — chạy theo đúng thứ tự

```bash
cd du-lieu
pip install pymupdf          # chỉ cần một lần

python parse-danh-muc.py thong-tu-75-2025-phu-luc-1.pdf   # → danh-muc-thuoc.json
python gop-sua-doi.py                                      # → danh-muc-cam.json, danh-muc-thuoc-2026.json
python parse-mrl.py                                        # → mrl.json, mrl-theo-hoat-chat.json
python dung-du-lieu-app.py                                 # → ../du-lieu-app.json  (app nạp file này)
python xuat-csv.py                                         # → csv/  (mở bằng Excel)
```

Mỗi script ghi kèm một file `bao-cao-*.txt` để kiểm chất lượng — **đọc nó, đừng
tin suông**.

### Kết quả hiện tại

| File | Nội dung |
|---|---|
| `danh-muc-thuoc-2026.json` | **5.929 thuốc** · 2.276 hoạt chất · 698 công ty |
| `danh-muc-cam.json` | 33 hoạt chất cấm |
| `mrl.json` | **4.322 ngưỡng** · 165 hoạt chất · 455 loại thực phẩm |
| `anh-xa-cay-thuc-pham.json` | Bảng ánh xạ tên cây → tên thực phẩm, **làm tay** |
| `../du-lieu-app.json` | Bản gọn app dùng: **5.914 thuốc · 345 cây · 488 dịch hại** · 791 KB (gzip 156 KB) |
| `csv/` | 5 file CSV mở bằng Excel |

Độ phủ: lúa 2.601 · cà phê 933 · lạc 724 · ngô 478 · cam 434 · đậu tương 414 ·
hồ tiêu 320 · cao su ~270 · điều ~186 · sầu riêng ~65

---

## 5. Mười bốn cái bẫy đã gặp — đừng dẫm lại

### Về PDF

**1. Đừng tự dò ranh giới hàng theo toạ độ.** Bản parse đầu tự xếp từ theo x/y.
Cột thì đúng nhưng hàng thì sai: tên thuốc xuống dòng bị dính vào bản ghi
trước, hỏng 1.279/6.294 bản ghi. Dùng `find_tables()` của PyMuPDF — nó đọc
đường kẻ của bảng nên gộp ô nhiều dòng đúng.

**2. Mốc cột phải ĐO của chính file đó, không suy từ file khác.** Lấy mốc của
Thông tư 75 áp cho Thông tư 28 → lệch đúng một cột, ô "hoạt chất" thật ra là
tên thương phẩm, khớp được **0** bản ghi. Cách đo: lấy `get_text("words")`,
dựng biểu đồ phân bố `x`, tìm các khoảng trống.

**3. Gán mục theo VỊ TRÍ DỌC của hàng, không theo trang.** Trang 2 của Thông tư
28 chứa cả tiêu đề mục 2 lẫn mục 3. Gán theo trang thì các thuốc *đổi hoạt
chất* bị tính nhầm thành *đã rút khỏi danh mục* — mà rút nghĩa là xoá.

**4. Quy tắc nối chữ bị ngắt dòng phải áp RIÊNG THEO CỘT.** Tên hoá chất Latin
ngắt giữa từ (`"Aminocyclopyrac"` + `"hlor"`) nên phải nối liền. Nhưng tiếng
Việt ngắt ở ranh giới TỪ, nối liền thì `"Sữa nguyên liệu"` thành
`"Sữanguyênliệu"`.

**5. Mã dạng thuốc lọt sang cột cây trồng.** Nguồn ghi `"100SP: sâu cuốn lá/
lúa; 200WP: …"`. Hai trường hợp: mã đứng một mình thì bỏ; mã nằm giữa
(`"ngô 600FS: xử lý hạt giống"`) thì cắt lấy phần trước, còn `"ngô"`. Sửa ba vòng: mã ở **đầu** chuỗi → bỏ; mã **giữa** chuỗi kèm `:` → cắt lấy phần trước;
mã ở **cuối** không có `:` (`"lúa 266SC"`) → cũng cắt. Kết quả 800 → **345** tên cây,
và số thuốc theo cây *tăng*. Còn sót 4 mục do văn bản gốc viết bất thường.

**6. `get_textbox` từng ô chậm gấp ~50 lần `extract()` cả bảng.** 355 trang:
hàng giờ so với 73 giây.

### Về dữ liệu

**7. Tên cây ≠ tên thực phẩm.** Danh mục BVTV nói `"lúa"`, Thông tư 50 nói
`"Gạo"`. Dò theo chuỗi thì `"lúa"` khớp nhầm `"lúa mì"` — **lúa mì là wheat**,
ngưỡng khác hẳn. Lỗi im lặng: app vẫn hiện ra một con số, chỉ là của cây khác.
Phải qua `anh-xa-cay-thuc-pham.json` làm tay. **Cây không có trong bảng thì báo
"chưa có ngưỡng", tuyệt đối không đoán.**

**8. MRL chỉ phủ 26% số thuốc.** Thông tư 50 lấy từ CODEX 2016, chỉ có 165 hoạt
chất trong khi danh mục Việt Nam có 2.276. Thiếu cả những thứ dùng nhiều nhất:
Abamectin, Hexaconazole, Tricyclazole, Validamycin, Kasugamycin. **Trạng thái
"không có ngưỡng" chiếm 74% nên nó là mặc định, không phải ngoại lệ** — thiết
kế giao diện phải coi vậy. Sầu riêng và thanh long chưa có ngưỡng nội địa dù là
cây xuất khẩu chủ lực.

### Về giao diện

*(Lịch sử — không còn áp dụng, xem cảnh báo đầu mục 6.)* **9. Franken UI đặt toàn bộ CSS trong `@layer`.** Theo quy tắc CSS, rule **không
có layer luôn thắng** rule có layer, bất kể thứ tự file. Muốn ghi đè token thì
để trần; muốn làm lưới dự phòng thì phải bọc `@layer`. Để trần nhầm một lần →
chữ đen trên nền đen, toàn bộ chữ đậm vô hình.

*(Lịch sử — không còn áp dụng, xem cảnh báo đầu mục 6.)* **10. Token của Franken là ba thành phần HSL** (`--foreground: 0 0% 98%`), phải
viết `hsl(var(--foreground))`. Viết `var(--foreground)` là giá trị vô nghĩa.

*(Lịch sử — không còn áp dụng, xem cảnh báo đầu mục 6.)* **11. `utilities.min.css` của Franken là bản dựng TĨNH** — không có class giá
trị tuỳ ý (`text-[4.5rem]`, `grid-cols-[minmax(...)]`) lẫn `truncate`. Dùng
Tailwind Play CDN (`cdn.tailwindcss.com`) sinh class lúc chạy, `preflight:false`
để khỏi đè base của Franken. Khi lên thật thì đổi sang Tailwind CLI build tĩnh.

### Về cách làm việc

**12. JavaScript im lặng khi hàm vẽ ném lỗi giữa chừng.** Ba hằng số SVG bị xoá
nhầm → `pBenh` ném `ReferenceError` → `ve()` chết → `innerHTML` không được gán →
màn hình giữ nguyên nội dung cũ trong khi nav và tiêu đề đã đổi. Nhìn ảnh chụp
không thấy nguyên nhân. **Phải bắt `window.onerror` khi kiểm.**

**13. Đừng thiết kế mù.** Đức đánh giá giao diện bằng mắt và mô tả bằng cảm nhận
("xấu", "chưa ổn"), không mô tả triệu chứng. Ba lượt sửa đầu đều trượt vì đoán.
Phải chụp màn hình rồi mới kết luận:

```bash
cd D:/Downloads/nôngapp
(python -m http.server 8801 >/dev/null 2>&1 &)
until curl -s -o /dev/null http://127.0.0.1:8801/index.html; do sleep 1; done
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new \
  --disable-gpu --hide-scrollbars --window-size=1500,1250 \
  --virtual-time-budget=20000 --screenshot="<đường dẫn>/shot.png" \
  "http://127.0.0.1:8801/index.html"
```
rồi đọc file PNG bằng công cụ Read.

**Phải chạy qua `http://127.0.0.1`, không dùng `file://`** — `fetch()` nạp
`du-lieu-app.json` sẽ bị CORS chặn trên `file://`. Bản mới không còn CDN nên
CSS hiện đúng cả hai chế độ, nhưng trang Tra bệnh và Pha thuốc vẫn cần HTTP.

Muốn đo màu thật: chèn `<script>` gọi `getComputedStyle`, ghi kết quả vào
`document.title`, chạy `--dump-dom` rồi đọc thẻ title. Cách này tìm ra lỗi chữ
đen trên nền đen mà nhìn ảnh không đoán được.

Muốn Đức chọn giữa nhiều phương án: dựng vài bản chỉ khác `--primary`, chụp
từng bản, gộp vào một trang HTML so sánh. Anh chọn bằng mắt nhanh hơn đọc chữ.

**14. CSV phải ghi kèm BOM** (`utf-8-sig`). Không có BOM thì Excel trên Windows
đọc UTF-8 thành ký tự rác, tên thuốc tiếng Việt hỏng hết.

---

## 6. App đang chạy tới đâu

> ### ⚠ ĐỌC TRƯỚC: `index.html` đã bị viết lại NGOÀI phiên làm việc này
>
> Giữa hai commit của tôi (20/09 20:56 → 22/09 13:28), `index.html` được
> Antigravity IDE viết lại toàn bộ: **bỏ Franken UI, bỏ Tailwind CDN**, thay bằng
> CSS tự viết dùng token hex thẳng (`var(--X)` chứ không phải `hsl(var(--X))`),
> dark mode mặc định, hiệu ứng glassmorphism và countdown ring SVG.
>
> Tôi chạy `git add -A` mà không soát, nên bản viết lại đó bị commit chung vào
> `12fe75e` — một commit có thông điệp nói về *lọc dữ liệu và xuất CSV*.
> `index-backup.html` (84 KB) cũng bị kéo vào cùng commit nhưng **đã xoá và
> gitignore** — không còn trong repo.
>
> **Hệ quả:** bẫy số 9, 10, 11 bên trên nói về Franken UI và Tailwind CDN —
> **không còn áp dụng cho mã hiện tại**, chỉ còn giá trị lịch sử. Nếu revert
> `index.html` về trước `12fe75e` thì vẫn dẫm phải.
>
> **Việc phải làm:** đọc thẳng `index.html`, đừng tin mô tả trong file này về
> phần giao diện.
>
> **Bài học:** đừng `git add -A` khi không biết chắc từ lần commit trước tới
> giờ còn ai đụng vào thư mục. Dùng `git status` rồi add từng đường dẫn.

### Đợt sửa lỗi 24/09/2026 (sau 27 commit của Antigravity ngày 23/09)

Kiểm bằng cách bấm tự động toàn bộ ~295 nút trên 9 trang, ở cả hai chế độ
giao diện, rồi chụp màn hình soát bằng mắt. Sau khi sửa: **0 lỗi**.

**Lỗi làm sập trang:** Tổng quan trắng ở chế độ Bình thường (`dmy()` nhận
timestamp số); "nhật ký gần nhất" lấy 4 bài *cũ nhất*; hàm `ring`, `dongModal`
khai báo hai lần; Sao lưu gọi biến `GIA_THI_TRUONG` không tồn tại; Mô phỏng đọc
trường `npkLyTuong` không có; bản đồ `flyTo` trên map cũ đã bị gỡ khỏi trang
→ Leaflet ném `Invalid LatLng (NaN, NaN)` (giờ chặn bằng `banDoDungDuoc()`).

**Lỗi sai thông tin thuốc — nặng nhất:**
- Tổng quan chỉ đếm cách ly cho cây lương thực → lô cà phê/sầu riêng/cao su
  vừa xịt vẫn hiện **"An toàn thu hoạch"**, thẻ lô ghi cứng "đã qua thời kỳ
  phân giải an toàn", "dư lượng 0 ppm, đủ chuẩn xuất khẩu". Giờ mọi lô đều
  tính theo `tt()`; bỏ hết câu "0 ppm" (app không đo được dư lượng).
- "AI Vision" chỉ đọc **tên file**; không khớp thì luôn trả "Cà phê – Rỉ sắt,
  96% tin cậy" và báo đỏ "sai loại cây" khi người dùng chọn Lúa. Giờ trả `null`,
  bảo người dùng tự chọn cây; bỏ % bịa; đổi nhãn thành "Đoán theo tên file ảnh".
- Danh mục bị sửa tay "Ababetter 5EC" → "3.6 EC" (Thông tư ghi 5EC), và một
  đoạn code **tự sửa nhật ký người dùng** sang tên mới mỗi lần mở app. Đã dựng
  lại `du-lieu-app.json` từ pipeline, bỏ đoạn tự sửa.
- Ảnh thuốc khớp theo mẩu chữ: "Anvilando" nhận ảnh Anvil, "Amistar 250SC"
  nhận ảnh Amistar Top, "BM super COC" nhận ảnh Curenox. Giờ khớp theo **phần
  đầu tên**. Đã soát 23 ảnh bằng mắt: 20 đúng nhãn, bỏ `ababetter.jpg` (chai
  3.6EC, không tìm được ảnh 5EC) và `regent.jpg` (không có trong danh mục).
- 35 ký tự font Symbol trong PDF (α, β, Ω, ®) bị đọc thành U+F0xx, hiện ô
  vuông ("Tervigo 020SC"). Sửa trong `dung-du-lieu-app.py` (`sua_font_symbol`).

**Nội dung gây hiểu nhầm:** nút "Làm mới giá" cộng số ngẫu nhiên rồi báo "đồng
bộ trực tiếp từ 5 sàn" → bỏ; tiêu đề giá "Realtime 30p-1h" → "Giá tham khảo nhập
sẵn"; băng cảnh báo bị thay bằng quảng cáo ("AI 100%", "Realtime") → trả lại lời
nhắc đọc PHI trên nhãn, hiện ở cả hai chế độ.

**Bẫy rút ra:**
- **15. Công cụ khác sẽ bịa cho đẹp.** Mỗi lần có người/công cụ khác sửa
  `index.html`, soát riêng mọi chữ "AI", "%", "realtime", "trực tiếp", "0 ppm",
  "chính hãng" — và mọi thay đổi trong `du-lieu-app.json` (so với `git show`).
- **16. Nhánh theo loại cây là chỗ lỗi an toàn trốn.** Cứ thấy
  `if(cType === ...)` là phải hỏi: nhánh này có còn hiện ngày cách ly không?
- **18. Nút chết không làm máy kiểm tra báo lỗi.** Bấm thử tự động chỉ bắt
  lỗi ném ra; nút không có code xử lý thì im lặng. Thêm nút mới phải bấm thử
  và kiểm **kết quả** (form mở, dòng nhật ký xuất hiện), không chỉ "không lỗi".
- **17. Heredoc bash trên Windows làm hỏng chữ "ì, á"** khi đưa vào Python →
  chạy `PYTHONUTF8=1 python - <<'PY'` hoặc ghi script ra file.

Một file `index.html`, JS thuần, không build. Nạp `du-lieu-app.json` lúc chạy.

| Trang | Trạng thái |
|---|---|
| **Tổng quan** | Danh sách "cần chú ý" xếp theo mức gấp, mỗi thửa một đồng hồ riêng, khối "giao hàng được chưa", biểu đồ lịch cách ly |
| **Thửa ruộng** | Bảng việc theo từng thửa |
| **Tra bệnh** | 4 bước: cây → dịch hại → thuốc → ghi sổ. **Dữ liệu thật.** Chặn hoạt chất cấm, hiện ngưỡng MRL, nhập PHI từ nhãn. Có tải ảnh, nhưng chỉ *đoán theo tên file* — chưa nhìn được ảnh |
| **Nhật ký** | Bảng đầy đủ, xuất hồ sơ (mã QR còn là ô trống) |
| **Pha thuốc** | Tìm trong 5.914 thuốc thật, 4 quy tắc tương kỵ. 20 thuốc có ảnh bao bì đã soát (ghi là ảnh minh hoạ) |
| **Điểm bán** | Sơ đồ vẽ tay, chưa phải bản đồ thật |
| **Giá thị trường** | Dữ liệu mẫu nhập sẵn, trang ghi rõ "chưa tự cập nhật" |
| **Mô phỏng** | Cellular automata trên canvas — đồ trình diễn |

Bốn lô mẫu: lúa, cà phê, cao su, sầu riêng Ri6. Hai chế độ giao diện: Bình thường (mặc định) và Chuyên nghiệp.

Lưu dữ liệu: `localStorage`. Chưa có tài khoản, chưa có máy chủ.

### AI xem ảnh bệnh (thêm 25/09/2026)

App gửi ảnh (thu nhỏ ≤1024px) + tên cây + danh mục dịch hại của cây đó tới máy
chủ trung gian **`https://so-ruong-ai.nguyenduc2k62.workers.dev/chan-doan`**
(Cloudflare Worker, mã ở `ai-worker/worker.js`). Worker giữ khoá Gemini (Secret
`GEMINI_API_KEY` trên Cloudflare — **không bao giờ để khoá trong repo**), gọi
Gemini, trả 2–3 khả năng + lý do nhìn thấy + mức chắc (chữ, không %). App đặt
khả năng cạnh ảnh mẫu và số thuốc đăng ký; người dùng tự xác nhận. AI không kê thuốc.

Những bẫy đã gặp khi dựng:
- **Tên mô hình Gemini bị Google ngừng** (404 với `gemini-2.5-flash`). Worker để
  `gemini-flash-latest`, gặp 404 thì tự hỏi danh sách mô hình và chọn bản flash
  cao nhất. Muốn cố định thì đặt biến `GEMINI_MODEL`.
- **"User location is not supported" (400)**: người dùng ở VN bị Cloudflare cho
  chạy ở Hồng Kông, Gemini chặn HK. Đã đặt *Settings → Runtime → Placement →
  Region → GCP asia-southeast1* (Singapore). Đừng đổi về Default.
- **503 quá tải** ở gói miễn phí (gặp 3/5 lần thử ngày 25/09): Worker đổi ngay sang một mô hình flash khác, rồi bản flash-lite; tối đa 3 lượt gọi mỗi lần bấm.
- Khoá dạng mới bắt đầu `AQ.` (không phải `AIza`) — dùng được với header `x-goog-api-key`.
- Chỉ trang GitHub Pages và localhost:8000 được gọi Worker (biến `CHO_PHEP_ORIGIN`).
  Công cụ ngoài trình duyệt vẫn giả được Origin → khi có nhiều người dùng cần
  giới hạn lượt theo IP.
- Gói miễn phí: Google có thể dùng ảnh gửi lên để cải thiện sản phẩm — app hỏi
  đồng ý trước lần gửi đầu (`so_ruong_dong_y_ai`).

Tắt AI: để `AI_MAY_CHU = ""` trong `index.html`. Thử Worker khác mà không sửa code:
`localStorage.setItem("so_ruong_ai_url", "https://...")`.

### Người dùng mới & Tra bệnh (thêm 24/09/2026, tối)

**Chưa có tài khoản.** Sổ nằm trong `localStorage` của máy. Khoá
`so_ruong_nguon_du_lieu`: `"mau"` (đang xem nông trại mẫu → dải xanh + nút
"Bắt đầu sổ của tôi") hoặc `"cua_toi"`. Lần đầu mở → màn chào `moManChao(1)`.
Nút "Đăng xuất" cũ giờ là "Bắt đầu lại" (mở màn chào, nhắc tải file sao lưu).
Xoá hết lô không còn bị nạp lại 4 lô mẫu.

**Tra bệnh không phán bệnh.** `chayChuanDoanAI()` chỉ xếp bệnh mẫu **cùng cây**
theo bằng chứng thật: chữ trong tên ảnh / ô tìm kiếm, bộ phận (tên ảnh nói "rễ"
thì tin hơn mặc định "Lá"). Không còn "% tương đồng", không ép "bệnh chính"
theo tên cây. Tên ảnh nhắc tới dịch hại có trong danh mục Thông tư mà không có
ảnh mẫu (vd "nấm hồng") → hiện số thuốc đăng ký cho cặp cây–dịch hại đó.
Kê đơn **không lấy thuốc đăng ký cho cây khác** khi cây không có thuốc đăng ký.

**Chụp màn hình điện thoại:** Chrome headless không cho cửa sổ hẹp hơn 500px
(`--window-size=390,…` thật ra ra 500). Muốn đo 390px phải nhúng app vào
`<iframe style="width:390px">`. Đo đúng 24/09: tràn ngang ở Lô đất (~800px),
Nhật ký (~900px), Mô phỏng (551px), Tổng quan chế độ Chuyên nghiệp (540px).

### Cách ly theo loại cây (thêm 24/09/2026)

Mọi chỗ hiện cách ly gọi **một hàm `danhGiaCachLy(th)`** — đừng tự tính lại
bằng `tt()` ở chỗ mới.

| Kiểu | Cây | Cảnh báo khi nào |
|---|---|---|
| `lientuc` | lúa, rau màu, chè, cây ăn trái chưa có bảng | Còn ngày cách ly là cảnh báo (như cũ) |
| `theomua` | cà phê, hồ tiêu, sầu riêng | Chỉ khi ngày hết cách ly **chồng vào** khoảng thu hoạch |
| `caosu` | cao su | Không đếm thu hoạch (mủ không phải thực phẩm); nhắc ngày vào vườn cạo |

Khoảng thu hoạch lấy theo thứ tự: ngày người dùng tự đặt (`THUA[].thuHoachTu`)
→ ngày ghi "🌸 Ra hoa" (`so[].loai === "Ra hoa"`) cộng bảng `HOA_DEN_CHIN`
→ mùa thường gặp `MUA_THUONG_GAP`. **Thiếu cả ba thì cảnh báo như `lientuc`**
— thiếu thông tin thì nghiêng về an toàn.

Nguồn số ngày từ ra hoa tới chín (tra 24/09/2026, **toàn trang doanh nghiệp /
nhà vườn, chưa phải tài liệu khuyến nông chính thức — cần thẩm định**):

| Cây | Số ngày | Nguồn |
|---|---|---|
| Cà phê vối | 270–330 (9–11 tháng) | simexcodl.com.vn/vong-doi-cua-cay-ca-phe |
| Cà phê chè | 210–270 (7–9 tháng) | như trên |
| Hồ tiêu | 240–300 (8–10 tháng) | rttc.hcmuaf.edu.vn/rttc-8142-1/vn/-cay-tieu.html |
| Sầu riêng Ri6 | 95–115 | thegioicaygiong.com, nghiepnong.com |
| Sầu riêng Monthong | 120–135 | như trên |
| Mùa cà phê vối | tháng 10–12 (Tây Nguyên) | simexcodl.com.vn/mua-thu-hoach-ca-phe-vao-thang-nao |
| Mùa hồ tiêu | tháng 2–3 | rttc.hcmuaf.edu.vn |

Cà phê chè chưa có nguồn cho mùa thu hoạch → không có mặc định, cần ghi ra hoa.

**Nút ghi nhanh / nút trên thẻ lô** đều gọi `moFormGhiNhanh(thuaId, MAU_GHI_NHANH[x])`
— mở form nhật ký điền sẵn, người dùng tự nhập vật tư. Trước 24/09: 4 nút ghi
nhanh không có code xử lý; nút trên thẻ ghi thẳng số viết sẵn vào nhật ký.

### Quyết định thiết kế cố ý

- **PHI do người dùng nhập từ nhãn**, app nhớ lại. Bỏ trống vẫn ghi được, chỉ
  là thửa đó không có đồng hồ. **Thà thiếu còn hơn bịa một con số.**
- **Không có thuốc đăng ký = chưa được phép dùng**, không phải app thiếu dữ
  liệu. Đã ghi rõ trong trạng thái rỗng.
- **Nhóm hoạt chất cho cảnh báo pha chung là SUY RA TỪ TÊN**, không phải phân
  loại chính thức. Đã ghi rõ mức tin cậy trong app.
- **App không tự phán bệnh.** Đưa ứng viên, người dùng tự chọn.
- Băng cảnh báo trên mọi trang phải giữ cho tới khi có người thẩm định bản parse.

---

## 7. Việc tiếp theo

Chi tiết trong `VIEC-CAN-LAM.md`. Ngắn gọn, theo thứ tự giá trị:

1. **Nhờ thầy bộ môn BVTV thẩm định bản parse** — gỡ được nửa câu cảnh báo
2. **Gom PHI** cho nhóm thuốc phổ biến — đây là thứ đồng hồ cần
3. **Ảnh bệnh thật** từ PlantDoc + Bugwood thay phần đang trống
4. **PWA chạy offline** — điều kiện để dùng được ngoài đồng
5. **Mã QR thật** cho hồ sơ
6. **Backend + vai trò HTX** — chỗ ra tiền

### Hai chỗ giao diện Đức đã nêu mà chưa sửa

- ~~Nhãn "gặt được" to hơn số ngày~~ — bản viết lại ngoài phiên này đã đổi cách
  trình bày, cần xem lại trên mã hiện tại
- Phông IBM Plex Mono vẽ số 0 có gạch chéo, "1240 ngày" nhìn như "124θ" — **chưa sửa**

---

## 8. Cách Đức làm việc

- Trả lời ngắn, mô tả bằng cảm nhận chứ không bằng triệu chứng. Hỏi lại cho rõ
  thì nhanh hơn đoán.
- Đánh giá giao diện bằng mắt — luôn chụp màn hình trước khi kết luận.
- Thích đi rộng (nhiều cây, nhiều tính năng) hơn đi hẹp. Đã bác đề xuất "làm
  lúa trước" và đúng: dữ liệu vốn đã đa cây, lọc riêng lúa là vứt việc đã làm.
- Muốn xem kết quả qua **GitHub Pages**, không phải artifact của Claude.
