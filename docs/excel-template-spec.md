# Excel Template Specification

Tài liệu này định nghĩa cấu trúc các cột cho file Excel output (Draft v0).

## 1. Sheet "Du lieu Phong"
Chứa dữ liệu tổng hợp theo từng phòng.
- `room_id`: ID định danh duy nhất của phòng.
- `room_name`: Tên phòng (ví dụ: Phòng khách, Bếp).
- `room_code`: Mã phòng (nếu có).
- `area_m2`: Diện tích sàn (m2).
- `perimeter_m`: Chu vi phòng (m).
- `floor_finish_m2`: Diện tích hoàn thiện sàn (m2).
- `wall_finish_m2`: Diện tích hoàn thiện tường (m2).

## 2. Sheet "Du lieu Cua"
Chứa dữ liệu chi tiết về các cửa (cửa đi, cửa sổ).
- `door_code`: Mã cửa.
- `door_name`: Tên cửa (ví dụ: D1, W1).
- `width_mm`: Chiều rộng cửa (mm).
- `height_mm`: Chiều cao cửa (mm).
- `area_m2`: Diện tích cửa (m2).
- `related_room_a`: Phòng liên kết A (bên trong/ngoài).
- `related_room_b`: Phòng liên kết B (bên trong/ngoài).

## 3. Sheet "Canh Phong"
Chứa dữ liệu chi tiết về các cạnh của phòng (để tính toán tường).
- `room_id`: ID định danh của phòng.
- `edge_index`: Số thứ tự của cạnh trong phòng.
- `length_m`: Chiều dài cạnh (m).
- `wall_finish_m2`: Diện tích hoàn thiện của bức tường ứng với cạnh này (m2).
