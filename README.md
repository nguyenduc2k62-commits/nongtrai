# Sổ Ruộng

Bản mẫu ứng dụng nhật ký canh tác lúa cho HTX và hộ sản xuất.

Ý tưởng lõi: nông dân ghi một dòng vào sổ, ứng dụng trả lại thứ cuốn sổ giấy không cho được —
**ngày sớm nhất được thu hoạch**, tính tự động từ thời gian cách ly (PHI) của thuốc đã dùng.

## Chạy

Không cần cài gì, không cần build. Mở thẳng `index.html` bằng trình duyệt.

| File | Nội dung |
|---|---|
| `index.html` | Web app đầy đủ — 8 trang, dùng trên máy tính |
| `mobile.html` | Bản khung điện thoại, làm trước để thử vòng lặp lõi |

## Các phần

| Trang | Làm gì |
|---|---|
| Tổng quan | Đồng hồ đếm ngược ngày được gặt, lịch cách ly từng thửa |
| Thửa ruộng | Theo dõi từng thửa trong vụ |
| Tra bệnh | Đối chiếu triệu chứng theo 4 bước → chọn thuốc → ghi thẳng vào sổ |
| Nhật ký | Toàn bộ việc đã làm, xuất hồ sơ cho bên thu mua |
| Pha thuốc | Cảnh báo tương kỵ trước khi đổ chung một bình |
| Điểm bán | Vườn ươm, đại lý vật tư, kho thu mua quanh vùng |
| Giá thị trường | Giá thu mua theo tuần |
| Mô phỏng | Sandbox cellular automata: đất, nước, phân, rễ, nấm bệnh, thuốc |

## Cảnh báo quan trọng

**Toàn bộ số liệu trong bản này là dữ liệu dựng để demo.** Thời gian cách ly, danh mục thuốc,
giá cả và điểm bán đều chưa đối chiếu với:

- Thông tư 75/2025/TT-BNNMT (hiệu lực 10/02/2026) — Danh mục thuốc BVTV được phép sử dụng
- Thông tư 28/2026/TT-BNNMT (hiệu lực 15/08/2026) — sửa đổi Phụ lục I

Không dùng để quyết định ngoài đồng cho tới khi thay bằng dữ liệu thật từ hai văn bản trên.

Luật trong phần mô phỏng là mô hình rút gọn để minh hoạ, không phải mô hình nông học đã
kiểm chứng. Dùng để dạy và demo.

## Việc tiếp theo

- [ ] Parse phụ lục Thông tư 75/2025 + 28/2026 ra JSON, thay dữ liệu thuốc giả
- [ ] Thay sơ đồ bệnh bằng ảnh thật từ PlantDoc (CC BY 4.0) và Bugwood
- [ ] Đổi sơ đồ bản đồ sang Leaflet + OpenStreetMap
- [ ] PWA: service worker + IndexedDB (Dexie) để chạy offline ngoài đồng
- [ ] Backend Node + PostgreSQL để nhiều hộ trong một HTX dùng chung

## Kỹ thuật

JavaScript thuần, một file, **không cần bước build**.

| Thành phần | Dùng gì |
|---|---|
| Giao diện | [Franken UI 2.1](https://franken-ui.dev) qua CDN — bản HTML-first của shadcn/ui, dựng trên UIkit 3 + Tailwind |
| Chủ đề | `uk-theme-green`, nền tối bật bằng class `dark` trên thẻ `<html>` |
| Phông chữ | Be Vietnam Pro + IBM Plex Mono (Google Fonts) |
| Biểu đồ | SVG tự vẽ, không dùng thư viện |
| Mô phỏng | Canvas + cellular automata tự viết |
| Lưu dữ liệu | `localStorage` của trình duyệt |

Màu nghiệp vụ (dải độc trên nhãn thuốc BVTV, trạng thái cách ly) được định nghĩa
riêng trong `<style>`, tách khỏi màu chủ đề — vì chúng mang nghĩa chứ không phải trang trí.

Có một khối `<style>` dự phòng đặt **trước** link CDN: nếu CDN hỏng thì trang vẫn
đọc được thay vì trắng bệch.
