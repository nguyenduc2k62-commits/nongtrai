# Bàn giao — dự án Sổ Ruộng

Viết ngày 22/09/2026, để một phiên làm việc mới đọc và tiếp tục được ngay mà
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

**Phải chạy qua `http://127.0.0.1`, không dùng `file://`** — CDN không kịp chạy,
ảnh ra trang trắng trơn không đại diện gì.

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
> Giữa hai commit của tôi (20/09 20:56 → 22/09 13:28), `index.html` được một
> công cụ khác viết lại toàn bộ: **bỏ Franken UI, bỏ Tailwind CDN**, thay bằng
> CSS tự viết dùng token hex thẳng (`var(--X)` chứ không phải `hsl(var(--X))`).
>
> Tôi chạy `git add -A` mà không soát, nên bản viết lại đó bị commit chung vào
> `12fe75e` — một commit có thông điệp nói về *lọc dữ liệu và xuất CSV*. Cùng
> commit đó còn kéo theo `index-backup.html` (84 KB) mà không ai chủ ý tạo.
>
> **Hệ quả:** bẫy số 9, 10, 11 bên trên nói về Franken UI và Tailwind CDN —
> **không còn áp dụng cho mã hiện tại**, chỉ còn giá trị lịch sử. Mô tả giao
> diện bên dưới cũng có thể lệch.
>
> **Việc phải làm:** đọc thẳng `index.html`, đừng tin mô tả trong file này về
> phần giao diện. Và quyết định xem có giữ `index-backup.html` không.
>
> **Bài học:** đừng `git add -A` khi không biết chắc từ lần commit trước tới
> giờ còn ai đụng vào thư mục. Dùng `git status` rồi add từng đường dẫn.

Một file `index.html`, JS thuần, không build. Nạp `du-lieu-app.json` lúc chạy.

| Trang | Trạng thái |
|---|---|
| **Tổng quan** | Danh sách "cần chú ý" xếp theo mức gấp, mỗi thửa một đồng hồ riêng, khối "giao hàng được chưa", biểu đồ lịch cách ly |
| **Thửa ruộng** | Bảng việc theo từng thửa |
| **Tra bệnh** | 4 bước: cây → dịch hại → thuốc → ghi sổ. **Dữ liệu thật.** Chặn hoạt chất cấm, hiện ngưỡng MRL, nhập PHI từ nhãn |
| **Nhật ký** | Bảng đầy đủ, xuất hồ sơ (mã QR còn là ô trống) |
| **Pha thuốc** | Tìm trong 5.914 thuốc thật, 4 quy tắc tương kỵ |
| **Điểm bán** | Sơ đồ vẽ tay, chưa phải bản đồ thật |
| **Giá thị trường** | Dữ liệu mẫu |
| **Mô phỏng** | Cellular automata trên canvas — đồ trình diễn |

Ba thửa mẫu: Đồng Bưng (lúa), Ruộng Trên (lúa), Vườn Cà phê (cà phê).

Lưu dữ liệu: `localStorage`. Chưa có tài khoản, chưa có máy chủ.

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
