# Sổ Ruộng — việc cần làm và chức năng

Cập nhật 24/09/2026. Xem thêm `BAN-GIAO.md` để nắm nguồn dữ liệu và các bẫy đã gặp.

---

## 0. Nguyên tắc giữ suốt dự án

Ba câu này quyết định mọi thứ bên dưới. Lệch khỏi chúng là lạc đường.

**Giá trị nằm ở hồ sơ tuân thủ, không nằm ở tư vấn.** Đối thủ thật không phải
mấy app nông nghiệp đang ế, mà là chủ đại lý vật tư đầu làng — miễn phí, trả
lời trong 30 giây, bán luôn thuốc, cho nợ tới mùa. Không đấu được ở đó. Đấu ở
chỗ họ không làm: chứng minh với bên thu mua rằng lô hàng đạt dư lượng.

**Tra bệnh là móc câu, không phải sản phẩm.** Nông dân không có lý do gì mở
một app ghi chép. Họ có lý do mở app khi cây có bệnh. Vào rồi thì việc ghi chép
xảy ra như hệ quả.

**Người trả tiền là HTX và doanh nghiệp thu mua, không phải nông dân.** Họ bị
ép bởi quy định dư lượng của bên mua, hiện quản lý bằng Excel và ảnh chụp sổ
tay gửi Zalo. Một HTX gật đầu là có ngay vài chục hộ dùng.

---

## 1. Đang chạy được

| Chức năng | Trạng thái |
|---|---|
| Đồng hồ đếm ngược ngày được gặt | Xong. PHI do người dùng nhập từ nhãn. Từ 24/09: cà phê/tiêu/sầu riêng chỉ cảnh báo khi chồng mùa thu hoạch; cao su nhắc ngày vào cạo |
| Nút "🌸 Cây ra hoa" → ước tính mùa thu hoạch | Xong 24/09. Số ngày từ ra hoa tới chín **cần thẩm định** |
| Lịch cách ly theo thửa (biểu đồ) | Xong |
| Tra bệnh: cây → dịch hại → thuốc → ghi sổ | Xong, **dữ liệu thật** 5.914 thuốc / 345 cây / 488 dịch hại |
| Chặn hoạt chất cấm | Xong, 33 hoạt chất theo Phụ lục II |
| Hiện ngưỡng dư lượng MRL | Xong. Không có ngưỡng thì báo "chưa có", không đoán |
| Cảnh báo tương kỵ khi pha chung bình | Xong, tìm trong 5.914 thuốc thật, 4 quy tắc |
| Nhật ký canh tác + xuất hồ sơ | Xong, mã QR còn là ô trống |
| Đa cây trồng | Xong. 4 lô mẫu: lúa, cà phê, cao su, sầu riêng. Mọi lô đều đếm cách ly |
| Ảnh bệnh đối chiếu | Vài ảnh mẫu; tải ảnh lên chỉ *đoán theo tên file*, chưa nhận diện ảnh thật |
| Bản đồ điểm bán | Sơ đồ vẽ tay, chưa phải bản đồ thật |
| Giá thị trường | Dữ liệu mẫu nhập sẵn, ghi rõ trên trang |
| Mô phỏng đồng ruộng (cellular automata) | Xong, là đồ trình diễn |
| Hai chế độ giao diện Bình thường / Chuyên nghiệp | Xong |
| Ảnh bao bì thuốc | 20 thuốc, đã soát khớp nhãn 24/09 |

Lưu dữ liệu: `localStorage` của trình duyệt. Mất khi đổi máy hoặc xoá dữ liệu
trang. Chưa có tài khoản, chưa có máy chủ.

---

## 2. Phải làm trước khi cho người thật dùng

Ba việc này là **chặn cứng**. Chưa xong thì băng cảnh báo "số liệu chưa thẩm
định" phải giữ nguyên trên mọi trang.

### 2.1 Dữ liệu thuốc thật — ĐÃ XONG PHẦN DANH MỤC

Đã parse và nối vào app. Xem `du-lieu/` và `BAN-GIAO.md` mục 3.

| Bộ | Số lượng | Nguồn |
|---|---|---|
| Danh mục thuốc | **5.929** | Thông tư 75/2025 + sửa đổi 28/2026 |
| Hoạt chất cấm | 33 | Phụ lục II Thông tư 75/2025 |
| Ngưỡng dư lượng MRL | 4.322 | Thông tư 50/2016 (Bộ Y tế) |
| Dịch hại | 546 | Rút từ chính danh mục |
| Cây trồng | 367 | Rút từ chính danh mục |

**Còn thiếu ba thứ:**

1. **PHI** — không nằm trong Thông tư nào, in trên nhãn từng chai. App đang để
   người dùng tự nhập và nhớ lại. Gom sẵn cho nhóm thuốc phổ biến thì tốt hơn.
2. **Người thẩm định bản parse.** Số liệu là thật nhưng bản parse chưa ai soát.
   Nhờ một thầy bộ môn BVTV soi qua thì gỡ được nửa câu cảnh báo.
3. **Chuẩn hoá tên cây** — còn ~1% lặp ("Lạc" vs "lạc") và vài mục ngoài nông
   nghiệp (đê, đập, nền móng — mục tiêu thuốc trừ mối).

### 2.2 Cơ chế cập nhật khi Thông tư đổi

Bộ NN sửa danh mục hằng năm. Một app nói sai PHI còn tệ hơn không có app.
Cần: ghi ngày phát hành dữ liệu, hiện trên màn hình, và cảnh báo khi quá hạn
12 tháng chưa cập nhật.

### 2.3 Ảnh bệnh thật thay sơ đồ vẽ tay

- **PlantDoc** (CC BY 4.0) — 2.598 ảnh ngoài đồng, chỉ cần ghi trích dẫn
- **Bugwood / IPM Images** — nhãn do chuyên gia BVTV đặt
- Cây lúa thì hai nguồn trên thiếu → tìm thêm trên Kaggle/Mendeley, hoặc xin
  ảnh từ tài liệu khuyến nông

Nhờ một thầy bộ môn BVTV duyệt lại ~300 ảnh đã chọn. Tốn khoảng 2 tiếng của
thầy, và câu "bộ ảnh đã qua thẩm định của ThS. X" có giá trị với hội đồng.

---

## 3. Chức năng nên làm tiếp, xếp theo giá trị

### Nhóm A — làm cho vòng lặp lõi chạy thật

1. **Chạy offline được (PWA)**
   Service worker + IndexedDB qua Dexie. Nông dân đứng giữa ruộng thường không
   có sóng. Đây là điều kiện để app dùng được thật, không phải tính năng phụ.
   Ước lượng 1 tuần.

2. **Mã QR thật cho hồ sơ**
   Hiện đang là ô trống ghi "MÃ QR". Sinh QR trỏ tới trang hồ sơ chỉ đọc.
   Ước lượng 1–2 ngày.

3. **Nhập nhanh bằng giọng nói**
   Web Speech API chạy phía client. Tay dính bùn thì gõ không nổi.
   Ước lượng 2–3 ngày.

4. **Nhắc việc**
   "Còn 3 ngày nữa hết cách ly", "đến hạn bón đón đòng". Thông báo đẩy.
   Ước lượng 2–3 ngày.

### Nhóm B — làm cho HTX dùng được nhiều hộ

5. **Backend + tài khoản**
   Node + Express + PostgreSQL. Mô hình dữ liệu lấy theo farmOS: `assets`
   (thửa, cây trồng, vật tư) / `logs` (mọi hoạt động) / `plans`. Đọc schema
   của họ trước khi tự thiết kế.
   Ước lượng 2–3 tuần.

6. **Vai trò HTX**
   Một tài khoản HTX nhìn được nhật ký của các hộ trong vùng nguyên liệu, xuất
   hồ sơ cả vùng. **Đây là chỗ ra tiền** — nên đừng để sau cùng.
   Ước lượng 1–2 tuần.

7. **Đồng bộ nhiều máy**
   Mỗi bản ghi thêm `updated_at` + cờ `synced`, có mạng thì đẩy hàng đợi lên.
   Nhật ký canh tác gần như không có xung đột (một người ghi ruộng của mình)
   nên không cần CRDT.

### Nhóm C — làm sau, hoặc bỏ

8. **Bản đồ thật** — Leaflet + OpenStreetMap, miễn phí không cần thẻ. Danh sách
   điểm bán tự gom theo huyện, chính xác hơn Google Maps ở cấp xã.
9. **Giá thị trường** — Việt Nam chưa có nguồn API công khai. Nếu làm thì lấy
   giá do người dùng báo rồi hiện trung vị theo huyện, đừng crawl chợ đầu mối.
10. **AI chẩn đoán bệnh qua ảnh** — chỉ bàn khi đã có kho ảnh riêng từ người
    dùng. Đấu Plantix (miễn phí, 800 triệu ảnh) từ đầu là thua.
11. **Sàn giao dịch, gọi video chuyên gia** — không phải bài toán code. Bỏ.

---

## 4. Việc kỹ thuật

- [ ] `esc()` chưa thoát dấu `'` — tên lô có `'` sẽ làm hỏng nút `onclick`.
- [ ] `du-lieu/csv/*.csv` và `danh-muc-thuoc*.json` vẫn còn ký tự font Symbol
      (U+F0xx) — mới sửa ở bước dựng `du-lieu-app.json`.
- [ ] Tách `index.html` (hiện ~11.400 dòng) thành nhiều file khi có bước build.
- [ ] Đưa 4 trang còn lại (Tra bệnh, Pha thuốc, Bản đồ, Giá) vào thẻ trắng cho
      đồng bộ với Tổng quan và Nhật ký.
- [ ] Kiểm ở 375px / 768px / 1024px / 1440px.
- [ ] Kiểm tương phản chữ đạt 4.5:1 ở cả hai nền.
- [ ] Kiểm điều hướng bằng bàn phím trên toàn bộ luồng tra bệnh.

---

## 5. Cố ý KHÔNG làm

Ghi ra đây để sau này không ai lôi lại.

- **Sàn thương mại điện tử.** Two-sided market, cần vốn và đội thực địa.
- **Gọi video với chuyên gia.** Cần *có chuyên gia trực*, là chi phí vận hành
  hàng tháng chứ không phải tính năng.
- **Tự động phán bệnh bằng AI rồi kết luận thay người dùng.** App đưa ứng viên,
  người dùng tự đối chiếu và tự chọn. Sai thì cũng là họ chọn — và họ tin hơn
  vì chính mắt họ so.
- ~~Mở rộng sang nhiều loại cây trước khi một loại chạy tốt.~~ Đức đã bác, đi đa cây — xem `BAN-GIAO.md` mục 8.

---

## 6. Rủi ro phải nhớ

| Rủi ro | Cách giảm |
|---|---|
| Nói sai PHI → nông dân bị trả lô hàng | Giữ băng cảnh báo tới khi có dữ liệu thật; ghi rõ ngày phát hành dữ liệu |
| Ảnh bệnh gán nhãn sai → xịt sai thuốc | Chỉ dùng nguồn có nhãn do chuyên gia đặt; hiện 3 ứng viên, không phán 1 đáp án |
| Thông tư đổi mà app không biết | Cảnh báo khi dữ liệu quá 12 tháng chưa cập nhật |
| Nông dân cài rồi bỏ | Đo tỉ lệ mở lại sau 7 và 30 ngày. Đây là con số quyết định dự án sống hay chết, không phải số lượt cài |
| Luật mô phỏng bị hiểu là mô hình thật | Giữ nguyên câu "mô hình rút gọn để minh hoạ" trong trang mô phỏng |

---

## 7. Mốc gần nhất

24/09/2026: xong đợt sửa lỗi sau bản viết lại của Antigravity (chi tiết `BAN-GIAO.md` mục 6).
24/09/2026: cách ly theo loại cây + nút ra hoa. Việc tiếp theo đã thống nhất với Đức: sửa tràn màn hình điện thoại (đo lại đúng: Lô đất, Nhật ký, Mô phỏng, Tổng quan chế độ Chuyên nghiệp), bỏ số bịa còn lại (đại lý giả quanh ruộng thật, bảng NPK, DRC/Brix trên thẻ; % tương đồng và huy hiệu xác thực đã bỏ 24/09), tách rau màu khỏi lúa, rút menu Bình thường còn 4 mục.

Mục 2.1 đã xong phần danh mục. Việc đáng làm tiếp, theo thứ tự:

1. **Nhờ thầy BVTV thẩm định bản parse** — rẻ nhất, gỡ được nửa câu cảnh báo
2. **Gom PHI** cho nhóm thuốc phổ biến — đây là thứ đồng hồ đếm ngược cần
3. **Ảnh bệnh thật** từ PlantDoc (CC BY 4.0) + Bugwood
4. **PWA chạy offline** — điều kiện để dùng được ngoài đồng
