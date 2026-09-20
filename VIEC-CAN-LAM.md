# Sổ Ruộng — việc cần làm và chức năng

Cập nhật 20/09/2026.

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
| Đồng hồ đếm ngược ngày được gặt, tính từ PHI | Xong |
| Lịch cách ly theo thửa (biểu đồ thời gian) | Xong |
| Tra bệnh 4 bước theo triệu chứng | Xong, dùng sơ đồ vẽ tay |
| Gợi ý thuốc → ghi thẳng vào nhật ký | Xong, dữ liệu mẫu |
| Cảnh báo tương kỵ khi pha chung bình | Xong, 4 quy tắc |
| Nhật ký canh tác + xuất hồ sơ | Xong, mã QR còn là chỗ trống |
| Bản đồ điểm bán | Sơ đồ vẽ tay, chưa phải bản đồ thật |
| Giá thị trường | Dữ liệu mẫu |
| Mô phỏng đồng ruộng (cellular automata) | Xong, là đồ trình diễn |
| Nền sáng/tối, nhớ lựa chọn | Xong |

Lưu dữ liệu: `localStorage` của trình duyệt. Mất khi đổi máy hoặc xoá dữ liệu
trang. Chưa có tài khoản, chưa có máy chủ.

---

## 2. Phải làm trước khi cho người thật dùng

Ba việc này là **chặn cứng**. Chưa xong thì băng cảnh báo "số liệu chưa thẩm
định" phải giữ nguyên trên mọi trang.

### 2.1 Thay dữ liệu thuốc giả bằng dữ liệu thật — ưu tiên cao nhất

Nguồn: **Thông tư 75/2025/TT-BNNMT** (hiệu lực 10/02/2026) và **Thông tư
28/2026/TT-BNNMT** (hiệu lực 15/08/2026, sửa Phụ lục I).

Cần bảng: hoạt chất — tên thương phẩm — cây trồng đăng ký — đối tượng phòng trừ
— **thời gian cách ly (PHI)** — nhóm độc.

PHI không nằm trong Thông tư mà in trên nhãn từng thuốc, nên phần này phải gom
tay. Bắt đầu bằng ~30 thuốc phổ biến nhất trên lúa, không cần làm hết danh mục.

Ước lượng: 2–3 ngày parse + 3–5 ngày gom PHI.
**Đây là phần không copy được từ đâu, nên cũng là phần đáng giá nhất.**

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

- [ ] Tailwind Play CDN → Tailwind CLI build ra CSS tĩnh. Play in cảnh báo ra
      console và không dành cho bản chạy thật.
- [ ] Tách `index.html` (hiện ~1.100 dòng) thành nhiều file khi có bước build.
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
- **Mở rộng sang nhiều loại cây trước khi một loại chạy tốt.** Làm lúa trước.

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

Nếu chỉ chọn được một việc để làm tiếp: **mục 2.1 — dữ liệu thuốc thật.**

Nó gỡ được băng cảnh báo, biến bản mẫu thành thứ dùng được, và là phần duy
nhất trong toàn dự án không copy được từ đâu.
