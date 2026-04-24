# 03 – User Stories
## Công cụ tự động nhận diện phòng và bóc khối lượng từ bản vẽ mặt bằng

**Phiên bản:** 1.0  
**Ngày soạn:** 2025  
**Trạng thái:** Draft – chờ review BA/QA  
**Tài liệu gốc:** SRS v1.0, Techstack v1.0

---

## 1. Mục đích tài liệu

### 1.1. Mục tiêu sử dụng

Tài liệu này chuyển toàn bộ yêu cầu trong SRS thành user stories có cấu trúc, testable, phục vụ trực tiếp cho:

- **Dev:** hiểu đúng scope từng task, tránh hiểu nhầm nghiệp vụ, biết rõ acceptance criteria trước khi code.
- **QA:** viết test case từ acceptance criteria mà không cần đọc lại SRS.
- **BA/PM:** quản lý backlog, ước lượng effort, theo dõi traceability từ story đến FR/BR/NFR.

### 1.2. Phạm vi áp dụng

Bao phủ toàn bộ 24 FR, 7 BR, và các NFR liên quan trong SRS v1.0. Không bao gồm các tính năng ngoài phạm vi SRS (thiết kế 3D, tiến độ thi công, quản trị user phức tạp).

### 1.3. Nguyên tắc viết story

- Mỗi story là một đơn vị giá trị nghiệp vụ độc lập, có thể test riêng lẻ.
- Không gộp nhiều hành vi phức tạp vào một story nếu làm khó test.
- Acceptance criteria phải observable và verifiable, không dùng từ chung chung như "đúng", "hợp lệ" khi không kèm định nghĩa cụ thể.
- Happy path và exception path tách story riêng khi cần thiết.
- Mọi story phải trace được ít nhất một FR/BR trong SRS.

---

## 2. Quy ước

### 2.1. Format story

```
Story ID:   US-[EPIC_PREFIX]-[NNN]
Epic:       Tên epic
Tên story:  Tên ngắn gọn, hành động
User story: Là [vai trò], tôi muốn [hành động], để [mục tiêu nghiệp vụ].
```

### 2.2. Format acceptance criteria

Ưu tiên dạng **Given / When / Then** cho flow có context rõ ràng.  
Dùng **checklist điều kiện / hành động / kết quả** cho các trường hợp validation thuần.

### 2.3. Định nghĩa priority

| Priority | Mô tả |
|---|---|
| **P0 – Critical** | Blocking: thiếu là không build được sản phẩm, không nghiệm thu được |
| **P1 – High** | Core feature: ảnh hưởng trực tiếp đến mục tiêu nghiệp vụ chính |
| **P2 – Medium** | Important: nên có trong bản release đầu, ảnh hưởng trải nghiệm |
| **P3 – Low** | Nice-to-have: có thể defer sang sprint sau |

### 2.4. Definition of Ready (DoR)

Story được đưa vào sprint khi:
- [ ] Story đã có acceptance criteria đầy đủ
- [ ] Dev và QA cùng đọc và không còn câu hỏi mở quan trọng
- [ ] Dữ liệu test (file DXF mẫu / Excel cửa mẫu) đã chuẩn bị hoặc có kế hoạch chuẩn bị
- [ ] Dependency rõ ràng (story nào phải done trước)

### 2.5. Definition of Done (DoD)

Story được đóng khi:
- [ ] Code hoàn thành, pass tất cả acceptance criteria
- [ ] Unit test viết và pass (với story tính toán: pytest coverage ≥ 90% logic)
- [ ] QA verify trên ít nhất 1 file DXF thực tế và 1 file test case synthetic
- [ ] Không có open bug P0/P1 liên quan
- [ ] Code review approved
- [ ] Tài liệu kỹ thuật cập nhật nếu có thay đổi interface/data model

---

## 3. Danh sách User Stories theo Epic

---

### EPIC 1: INPUT – Nhập dữ liệu và phạm vi xử lý

---

#### US-INP-001 – Nhập file DXF bản vẽ mặt bằng

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-INP-001 |
| **Epic** | Input & Phạm vi xử lý |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-01, NFR-07 |

**User story:**  
Là người thực hiện bóc tách khối lượng, tôi muốn nhập file DXF bản vẽ mặt bằng vào hệ thống, để hệ thống có dữ liệu hình học và thuộc tính làm cơ sở xử lý.

**Mô tả chi tiết:**  
Người dùng chọn file DXF từ file picker trên giao diện Python desktop (PySide6). Hệ thống đọc file bằng `ezdxf`, load toàn bộ entities, layer metadata. Sau khi load xong, hệ thống thông báo trạng thái đọc (số lượng entity, danh sách layer nhận diện được).

**Preconditions:**
- File DXF tồn tại và không bị corrupt
- File DXF có chứa đối tượng geometry (LINE, LWPOLYLINE) và text/block entities

**Main flow:**
1. User click nút "Chọn file DXF" trên giao diện
2. File picker mở, user chọn file .dxf
3. Hệ thống đọc file bằng ezdxf
4. Hệ thống hiển thị thông tin: số entities đọc được, danh sách layer tìm thấy
5. Hệ thống cho phép tiếp tục sang bước chọn phạm vi

**Alternate / Exception flow:**
- File không tồn tại hoặc không đúng định dạng → hiển thị lỗi rõ ràng, không crash
- File DXF không có entity nào → cảnh báo "File không chứa dữ liệu hình học"
- File DXF bị corrupt (ezdxf raise exception) → bắt exception, hiển thị thông báo lỗi, cho phép chọn lại file

**Acceptance criteria:**
- [ ] **Given** file DXF hợp lệ có chứa geometry, **When** user chọn file, **Then** hệ thống load thành công và hiển thị số lượng entity đọc được (≥ 1)
- [ ] **Given** file DXF hợp lệ, **Then** danh sách layer nhận diện được hiển thị trên UI
- [ ] **Given** file không phải DXF (ví dụ: .dwg, .pdf), **When** user chọn, **Then** hệ thống hiển thị thông báo lỗi định dạng, không crash
- [ ] **Given** file DXF bị corrupt, **When** đọc, **Then** hệ thống catch exception và hiển thị thông báo, không crash ứng dụng
- [ ] Sau khi load thành công, nút "Tiếp tục" / bước tiếp theo được kích hoạt

**Input:** File .dxf từ AutoCAD  
**Output:** Object model entities trong bộ nhớ (ezdxf model), danh sách layer  
**Ghi chú QA:** Test với ít nhất 3 file: (1) file sạch chuẩn, (2) file có nhiều layer rác, (3) file corrupt

---

#### US-INP-002 – Chọn phạm vi xử lý bằng quét vùng trên AutoCAD

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-INP-002 |
| **Epic** | Input & Phạm vi xử lý |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-02, NFR-06 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn dùng chuột quét chọn vùng mặt bằng trên AutoCAD, để giới hạn phạm vi xử lý chỉ ở căn hộ hoặc vùng cần thiết, tránh xử lý toàn bộ bản vẽ lớn.

**Mô tả chi tiết:**  
Người dùng thao tác trực tiếp trên AutoCAD (thông qua lệnh AutoLISP). Hệ thống AutoLISP nhận vùng quét (crossing window), truyền bounding box hoặc selection set đó sang Python (qua file JSON trung gian). Python chỉ xử lý các entities nằm trong phạm vi đó.

**Preconditions:**
- AutoCAD đang mở với file bản vẽ
- AutoLISP đã được load

**Main flow:**
1. User gõ lệnh AutoLISP trên Command Line (ví dụ: `BOKL`)
2. LISP yêu cầu user quét chọn vùng (crossing window)
3. User kéo chuột quét chọn vùng căn hộ cần xử lý
4. LISP ghi phạm vi (tọa độ bounding box + selection set info) vào `input.json`
5. LISP kích hoạt Python script
6. Python đọc `input.json`, lọc entities trong phạm vi đó từ DXF

**Alternate / Exception flow:**
- User bấm ESC không chọn vùng → LISP thông báo "Chưa chon vung xu ly" và thoát
- Vùng chọn không chứa entity hình học nào → Python cảnh báo "Vung chon trong, khong co du lieu"

**Acceptance criteria:**
- [ ] **Given** user quét chọn vùng hợp lệ có chứa ít nhất 1 phòng, **When** xử lý, **Then** chỉ các entity trong bounding box đó được đưa vào pipeline
- [ ] Entity nằm hoàn toàn ngoài vùng chọn không xuất hiện trong kết quả
- [ ] Entity nằm một phần trong vùng chọn: xử lý theo logic "intersects bounding box" (cần xác định và document rõ hành vi này)
- [ ] Bounding box được ghi đúng vào `input.json` với tọa độ (xmin, ymin, xmax, ymax)
- [ ] Khi user bấm ESC, hệ thống không crash và không ghi file trung gian

**Giả định:** Đơn vị tọa độ trong DXF là mm, nhất quán với unit cài đặt trong AutoCAD.  
**Input:** Crossing window selection từ AutoCAD  
**Output:** Bounding box tọa độ trong `input.json`  
**Ghi chú QA:** Test vùng chứa toàn bộ mặt bằng và vùng chỉ chứa 1 căn hộ trong mặt bằng nhiều căn

---

#### US-INP-003 – Nhập dữ liệu cửa từ file Excel

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-INP-003 |
| **Epic** | Input & Phạm vi xử lý |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-03, FR-09, BR-02 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn nhập danh sách cửa từ file Excel, để hệ thống có đầy đủ thông tin kích thước cửa mà không cần đọc thủ công từng block trên bản vẽ.

**Mô tả chi tiết:**  
Hệ thống đọc file Excel (dùng `pandas + openpyxl`) chứa danh mục cửa với các cột: mã cửa, tên cửa, chiều rộng (mm), chiều cao (mm). Dữ liệu này được merge với dữ liệu block nhận diện từ DXF dựa trên mã cửa làm key.

**Preconditions:**
- File Excel đã chuẩn bị theo template chuẩn (cột: `ma_cua`, `ten_cua`, `rong_mm`, `cao_mm`)
- Mã cửa trong Excel khớp với mã block trên bản vẽ (ví dụ: D1, D2, DW, S1)

**Main flow:**
1. User chọn file Excel cửa qua file picker
2. Hệ thống đọc file, parse sheet đầu tiên (hoặc sheet được chỉ định)
3. Hệ thống validate: kiểm tra cột bắt buộc (`ma_cua`, `rong_mm`, `cao_mm`) có tồn tại không
4. Hệ thống load danh sách cửa vào dictionary `{ma_cua: {ten, rong, cao}}`
5. Hệ thống thông báo số lượng cửa đọc được

**Alternate / Exception flow:**
- File Excel thiếu cột bắt buộc → cảnh báo cụ thể tên cột bị thiếu, không tiếp tục
- Cửa có `rong_mm` hoặc `cao_mm` là 0 hoặc null → đánh dấu là "thiếu dữ liệu", cảnh báo, không đưa vào tính toán (BR-02)
- Mã cửa trong Excel không tìm thấy trên bản vẽ → ghi log warning, không gây lỗi hệ thống
- File Excel không thể mở (corrupt, password) → hiển thị lỗi, cho phép chọn lại

**Acceptance criteria:**
- [ ] **Given** file Excel hợp lệ với 5 loại cửa D1–D3, DW, S1, **When** load, **Then** hệ thống đọc đúng 5 record với đầy đủ ma_cua, rong_mm, cao_mm
- [ ] **Given** cửa có chiều rộng = 0, **Then** hệ thống đánh dấu cửa đó là "invalid", không dùng trong tính toán, hiển thị cảnh báo
- [ ] **Given** cửa trong Excel không xuất hiện trên bản vẽ, **Then** hệ thống ghi warning log, không crash
- [ ] **Given** file Excel thiếu cột `rong_mm`, **Then** hệ thống hiển thị lỗi: "Thieu cot bat buoc: rong_mm"
- [ ] Chiều rộng và chiều cao được lưu đúng giá trị số (không bị đọc thành string)

**Input:** File .xlsx với danh sách cửa  
**Output:** Dictionary cửa trong bộ nhớ, log warning nếu có  
**Ghi chú QA:** Test với file có cửa trùng mã (cùng D1 xuất hiện 2 lần) – kiểm tra hành vi giữ record nào

---

### EPIC 2: ROOM – Nhận diện phòng và tạo đường bao

---

#### US-ROOM-001 – Click điểm bên trong phòng để kích hoạt nhận diện

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-ROOM-001 |
| **Epic** | Nhận diện phòng |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-04, FR-05, BR-01 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn click vào điểm bên trong mỗi phòng trên AutoCAD, để hệ thống nhận diện và tạo đường bao khép kín cho phòng đó.

**Mô tả chi tiết:**  
Đây là bước tương tác cốt lõi. AutoLISP nhận điểm click từ user, bắn tia (thuật toán X-ray hoặc Ghost Boundary tùy loại phòng), lọc entity rác, tạo LWPOLYLINE khép kín màu đỏ lineweight 0.4mm đại diện cho ranh giới phòng. Polyline này sau đó được Python đọc để tính toán.

**Preconditions:**
- AutoCAD đã mở file bản vẽ
- Layer tường đã được xác định (cấu hình trong LISP hoặc user nhập)
- AutoLISP đã load (lệnh `XR` hoặc `GB` sẵn sàng)

**Main flow:**
1. User gõ lệnh `XR` (phòng vuông) hoặc `GB` (phòng phức tạp) trên CAD command line
2. LISP prompt: "Click 1 diem vao giua phong:"
3. User click vào điểm bên trong phòng
4. LISP bắn 4 tia (XR) hoặc quét chọn vùng (GB), lọc rác, tìm mép tường trong
5. LISP tạo LWPOLYLINE khép kín, màu đỏ (color = 1), lineweight = 40 (0.4mm)
6. Polyline được đặt trên layer riêng (ví dụ: `PHONG_BOUNDARY`)
7. LISP lưu thông tin polyline (entity name / tọa độ) vào `input.json` kèm index phòng

**Alternate / Exception flow:**
- Click điểm nằm ngoài mọi vùng kín → LISP thông báo "Khong tim thay ranh gioi", không tạo polyline
- Không tìm đủ 4 mép tường (XR) → LISP thông báo "Loi: Khong tim thay du 4 vach tuong tieu chuan!"
- Ranh giới không khép kín (GB) → LISP thông báo "Ranh gioi khong khep kin hoac diem click nam ngoai"
- User click 2 lần vào cùng 1 phòng → xử lý trùng lặp tại US-ROOM-003

**Acceptance criteria:**
- [ ] **Given** user click vào điểm rõ ràng bên trong phòng hình chữ nhật, **When** dùng lệnh XR, **Then** LWPOLYLINE khép kín màu đỏ được tạo bao quanh đúng phòng đó
- [ ] LWPOLYLINE có color = 1 (đỏ) và lineweight = 40 (0.4mm)
- [ ] LWPOLYLINE là closed (thuộc tính closed = True)
- [ ] **Given** phòng hình chữ L, **When** dùng lệnh GB, **Then** LWPOLYLINE bao đúng hình dạng phòng, không bị lẹm tại góc giật cấp
- [ ] **Given** click điểm bên trong block đồ nội thất (giường, bàn), **When** XR, **Then** hệ thống vẫn tạo đúng ranh giới phòng (bỏ qua nội thất)
- [ ] **Given** click bên ngoài phòng (vào tường hoặc hành lang), **Then** LISP thông báo lỗi, không tạo polyline sai

**Business rules:** BR-01 – phòng chỉ được đưa vào tính toán khi có vùng hợp lệ  
**Input:** Tọa độ điểm click từ user  
**Output:** LWPOLYLINE khép kín trên bản vẽ, ghi thông tin vào `input.json`  
**Ghi chú QA:** Test 5 loại phòng: (1) hình chữ nhật đơn giản, (2) chữ L, (3) có cột thụt vào, (4) phòng nhỏ, (5) phòng có nhiều đồ nội thất

---

#### US-ROOM-002 – Tạo đường bao sạch không bị lẹm bởi block cửa

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-ROOM-002 |
| **Epic** | Nhận diện phòng |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-05, FR-04 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn đường bao phòng không bị ảnh hưởng bởi block cửa (cánh cửa, arc quét cửa), để diện tích và chu vi tính ra phản ánh đúng thực tế không gian phòng.

**Mô tả chi tiết:**  
BPOLY mặc định hiểu block cửa như "vật cản", gây lẹm diện tích. Hệ thống dùng kỹ thuật "Lọc ranh giới" (Boundary Set chỉ gồm layer tường) hoặc "Đóng cửa tạm thời" (vẽ Line tạm tại vị trí cửa trước khi chạy BPOLY).

**Preconditions:**
- Layer tường đã được xác định (không chứa block cửa)
- Block cửa nằm trên layer riêng (ví dụ: `CUA`, `DOOR`)

**Main flow:**
1. Trước khi gọi BPOLY, LISP `ssget` lấy selection set chỉ gồm LINE/LWPOLYLINE trên layer tường
2. LISP truyền selection set này vào lệnh `-BOUNDARY` với tùy chọn "Advanced → Boundary Set"
3. BPOLY chỉ "nhìn" vào selection set đó, bỏ qua hoàn toàn block cửa
4. LWPOLYLINE được tạo ra bao sát mép tường trong, không lẹm vào vị trí cửa

**Alternate / Exception flow:**
- Layer tường chưa được cấu hình → LISP cảnh báo yêu cầu nhập tên layer tường trước
- Không có entity nào trên layer tường trong vùng click → LISP thông báo lỗi

**Acceptance criteria:**
- [ ] **Given** phòng có 1 cửa mở vào trong (block cửa + arc quét), **When** tạo boundary, **Then** LWPOLYLINE không bị lẹm vào vị trí cửa, diện tích ≥ diện tích thực tế phòng (không âm lệch)
- [ ] **Given** phòng có 2 cửa đối diện, **When** tạo boundary, **Then** LWPOLYLINE bao toàn bộ phòng liên tục, không bị đứt
- [ ] Diện tích tính từ LWPOLYLINE ≤ 2% sai lệch so với diện tích đo tay từ tọa độ tường
- [ ] Block cửa, arc quét cửa, block nội thất không được phép nằm trên layer tường (QA cần validate naming convention với khách hàng)

**Ghi chú QA:** Tạo test case DXF synthetic với phòng 5×4m, cửa 0.9m, đo diện tích thủ công (20m²), verify kết quả hệ thống ≤ 0.4m² sai lệch

---

#### US-ROOM-003 – Loại bỏ phòng bị nhận diện trùng lặp

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-ROOM-003 |
| **Epic** | Nhận diện phòng |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-06, BR-01 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống tự động loại bỏ khi cùng một phòng bị click nhận diện nhiều lần, để kết quả Excel không bị xuất dữ liệu trùng gây sai tổng khối lượng.

**Mô tả chi tiết:**  
Python kiểm tra overlap giữa các LWPOLYLINE đã tạo. Nếu 2 polygon có độ trùng diện tích > ngưỡng (đề xuất: 90%), coi là trùng lặp, chỉ giữ lại cái được tạo đầu tiên và log warning.

**Preconditions:**
- Đã có ít nhất 2 LWPOLYLINE từ bước nhận diện phòng

**Main flow:**
1. Python load toàn bộ LWPOLYLINE boundary từ bản vẽ/file trung gian
2. Python dùng Shapely để tính intersection area giữa từng cặp polygon
3. Nếu `intersection_area / min(area_A, area_B) > 0.90`: đánh dấu là trùng lặp
4. Giữ lại polygon có `internal_room_id` nhỏ hơn (tạo trước), xóa cái còn lại khỏi danh sách xử lý
5. Log warning: "Phong [ID] bi loai do trung lap voi Phong [ID]"

**Alternate / Exception flow:**
- 2 phòng kề nhau có chia sẻ đoạn tường chung nhưng không trùng lặp (overlap < 5%) → giữ cả 2, không log
- Không có phòng trùng lặp → xử lý bình thường, không log warning

**Acceptance criteria:**
- [ ] **Given** user click 2 lần vào cùng 1 phòng → 2 polygon gần như identical được tạo, **Then** Python giữ lại 1, log warning cho cái bị loại
- [ ] **Given** 2 phòng kề nhau (chỉ share tường chung), **Then** cả 2 phòng được giữ nguyên, không bị loại nhầm
- [ ] Số lượng phòng trong output Excel bằng số phòng thực tế (không bị nhân đôi)
- [ ] Log warning có nội dung: polygon bị loại có `internal_room_id` nào, trùng với ID nào

**Input:** Danh sách LWPOLYLINE từ bước nhận diện  
**Output:** Danh sách phòng đã deduplicate  
**Ghi chú QA:** Test với scenario: 3 phòng, click nhầm phòng giữa 2 lần

---

#### US-ROOM-004 – Gắn tên phòng và mã phòng từ text có sẵn

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-ROOM-004 |
| **Epic** | Nhận diện phòng |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-07, BR-07, NFR-03 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống tự động gắn tên phòng và mã phòng từ text đã có sẵn trong bản vẽ vào đúng phòng tương ứng, để không cần nhập tay và tránh sai sót định danh.

**Mô tả chi tiết:**  
Python dùng ezdxf đọc các entity TEXT/MTEXT trong bản vẽ. Với mỗi text entity, kiểm tra insertion point có nằm trong polygon của phòng nào không (Shapely `contains`). Nếu có → gán text đó là `room_name` hoặc `room_code` theo logic phân biệt (mã phòng thường có pattern như `P01`, `WC`, `BED1`; tên phòng là chuỗi tự nhiên).

**Preconditions:**
- Boundary polygon các phòng đã được tạo (US-ROOM-001 done)
- Text tên/mã phòng nằm bên trong vùng phòng tương ứng trong bản vẽ

**Main flow:**
1. Python lấy toàn bộ TEXT/MTEXT entities trong phạm vi xử lý
2. Với mỗi text, lấy insertion point (x, y)
3. Python kiểm tra điểm đó nằm trong polygon phòng nào (Shapely `polygon.contains(Point(x,y))`)
4. Gán text vào phòng theo rule: ưu tiên text khớp pattern mã phòng làm `room_code`, còn lại làm `room_name`
5. Nếu phòng không có text nào → gán `room_name = "Chua_dinh_danh"`, `room_code = "ROOM_[ID]"`

**Alternate / Exception flow:**
- Text nằm trên ranh giới (điểm chèn đúng mép tường) → xử lý theo rule "gần nhất" (điểm gần tâm phòng nào nhất thì thuộc phòng đó)
- Phòng có nhiều text khác nhau bên trong → gán tất cả, log để QA kiểm tra thủ công
- Text nằm ngoài tất cả các phòng → bỏ qua, không gán

**Acceptance criteria:**
- [ ] **Given** text "PHONG NGU" nằm bên trong polygon phòng A, **Then** `room_name` của phòng A = "PHONG NGU"
- [ ] **Given** text "P01" nằm bên trong polygon phòng A, **Then** `room_code` của phòng A = "P01"
- [ ] **Given** phòng không có text nào bên trong, **Then** `room_name = "Chua_dinh_danh"`, `room_code = "ROOM_[internal_id]"`, cảnh báo được ghi vào log
- [ ] **Given** 2 phòng kề nhau, text của phòng A không bị gán nhầm sang phòng B
- [ ] Thông tin `room_name` và `room_code` xuất hiện đúng trong báo cáo Excel cuối

**Business rules:** BR-07 – ưu tiên dữ liệu text có sẵn  
**Input:** TEXT/MTEXT entities trong DXF, danh sách polygon phòng  
**Output:** `room_name`, `room_code` gán cho từng phòng  
**Ghi chú QA:** Test case: text phòng nằm rất sát mép tường (cách 1mm)

---

### EPIC 3: DOOR – Nhận diện cửa và mapping cửa–phòng

---

#### US-DOOR-001 – Nhận diện block cửa trên bản vẽ

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-DOOR-001 |
| **Epic** | Nhận diện cửa và mapping cửa–phòng |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-08, FR-09, BR-02 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống tự động nhận diện các block cửa (D1, D2, D3, DW, S1, S2…) trong phạm vi xử lý, để không cần đếm tay và có đầy đủ danh sách cửa với thông tin kích thước.

**Mô tả chi tiết:**  
Python dùng ezdxf đọc các INSERT entity (block reference) trong phạm vi xử lý. Với mỗi INSERT, đọc `block_name` (tên block) và các attribute để nhận diện mã cửa. Sau đó tra cứu kích thước (rộng, cao) từ dictionary đã load từ Excel (US-INP-003) hoặc từ attribute block trực tiếp.

**Preconditions:**
- File DXF đã load (US-INP-001)
- Danh sách cửa từ Excel đã load (US-INP-003) hoặc attribute block có đủ thông tin

**Main flow:**
1. Python lấy toàn bộ INSERT entity trong phạm vi bounding box
2. Với mỗi INSERT, đọc `block_name` và attributes (nếu là attributed block)
3. Đối chiếu `block_name` / attribute value với danh sách mã cửa từ Excel
4. Nếu khớp: tạo Door object với `door_code`, `door_name`, `width`, `height`, `position` (insertion point)
5. Tính `door_area = width × height`
6. Nếu không khớp: bỏ qua block đó (không phải block cửa)

**Alternate / Exception flow:**
- Block cửa có tên nhưng không có trong Excel → đọc attribute block trực tiếp; nếu attribute cũng không có width/height → đánh dấu "thiếu dữ liệu", cảnh báo (BR-02)
- Block cửa có width/height = 0 → cảnh báo, không đưa vào tính toán
- Không tìm thấy block cửa nào trong phạm vi → cảnh báo "Khong tim thay cua", tiếp tục xử lý phòng

**Acceptance criteria:**
- [ ] **Given** bản vẽ có 5 block D1, D2, D3, DW, S1 trong phạm vi xử lý, **Then** hệ thống nhận diện đúng 5 cửa
- [ ] Mỗi cửa nhận diện được có đầy đủ: `door_code`, `width` (mm), `height` (mm), `position` (x, y)
- [ ] `door_area = width × height` được tính đúng (đơn vị mm²) và chuyển đổi sang m² khi xuất báo cáo
- [ ] **Given** block D1 không có trong file Excel cửa, **Then** hệ thống đọc attribute block, nếu vẫn không có width/height → cảnh báo và đánh dấu invalid
- [ ] Block không phải cửa (block nội thất, ký hiệu kỹ thuật) không bị nhận diện là cửa

**Business rules:** BR-02  
**Input:** INSERT entities từ DXF, dictionary cửa từ Excel  
**Output:** Danh sách Door objects với đầy đủ thuộc tính  
**Ghi chú QA:** Test với bản vẽ có block cửa và block không phải cửa lẫn lộn

---

#### US-DOOR-002 – Gán cửa vào phòng (cửa 1 phòng)

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-DOOR-002 |
| **Epic** | Nhận diện cửa và mapping cửa–phòng |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-10, FR-11, BR-03 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống tự động xác định cửa nào thuộc phòng nào, để quan hệ cửa–phòng được ghi chính xác vào báo cáo mà không cần gán thủ công.

**Mô tả chi tiết:**  
Python dùng Shapely để kiểm tra insertion point của block cửa có nằm trong hoặc gần ranh giới polygon phòng nào. Nếu insertion point nằm trong polygon → cửa đó thuộc phòng đó (`related_room_a`). Nếu nằm trên/gần ranh giới (buffer) → xem xét case cửa 2 phòng (US-DOOR-003).

**Preconditions:**
- Danh sách Door objects đã có (US-DOOR-001)
- Danh sách Room polygons đã có (US-ROOM-001)

**Main flow:**
1. Với mỗi Door, lấy `position` (x, y)
2. Kiểm tra `polygon.contains(Point(x, y))` cho từng phòng
3. Nếu 1 phòng chứa insertion point → gán `related_room_a = room_id` đó
4. Nếu 0 phòng chứa → áp dụng buffer distance (đề xuất: 50mm) để tìm phòng gần nhất
5. Lưu quan hệ Door ↔ Room

**Alternate / Exception flow:**
- Insertion point nằm ngoài tất cả phòng kể cả sau buffer → đánh dấu cửa "unassigned", cảnh báo
- Insertion point nằm trong nhiều phòng (polygon overlap) → ưu tiên phòng có diện tích lớn hơn, log warning

**Acceptance criteria:**
- [ ] **Given** block D1 có insertion point rõ ràng bên trong phòng "Phong ngu", **Then** `related_room_a` của D1 = ID phòng ngủ
- [ ] **Given** cửa nằm trong phòng với polygon hợp lệ, **Then** quan hệ cửa–phòng xuất hiện đúng trong báo cáo
- [ ] **Given** cửa không nằm trong phòng nào, **Then** hệ thống cảnh báo cửa "unassigned", không crash, không gán sai
- [ ] Tổng số cửa gán được + cảnh báo unassigned = tổng số cửa nhận diện được

**Business rules:** BR-03  
**Ghi chú QA:** Test với cửa đặt đúng giữa phòng và cửa đặt sát mép tường

---

#### US-DOOR-003 – Gán cửa vào 2 phòng (cửa trên ranh giới chung)

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-DOOR-003 |
| **Epic** | Nhận diện cửa và mapping cửa–phòng |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-10, FR-11, FR-17, BR-03, BR-06 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống nhận biết khi cửa nằm trên ranh giới chung giữa 2 phòng và gán cửa đó vào cả 2 phòng, để logic trừ diện tích cửa được áp dụng đúng theo nghiệp vụ.

**Mô tả chi tiết:**  
Khi insertion point của block cửa nằm trong buffer của đường biên chung giữa 2 polygon (giao đoạn chung của 2 boundary), hệ thống xác định đây là cửa trên ranh giới chung. Cửa này có `related_room_a` và `related_room_b` đều khác null.

**Preconditions:**
- US-DOOR-002 đã xác định cửa có thể liên quan đến 2 phòng
- Hai phòng kề nhau có đoạn tường chung

**Main flow:**
1. Khi `polygon.contains(Point)` trả về 0 phòng và buffer trả về ≥ 2 phòng:
2. Python tính shared edge giữa các phòng này bằng Shapely (`boundary.intersection`)
3. Kiểm tra insertion point cửa có gần shared edge không (distance < chiều dày tường + tolerance)
4. Nếu có → gán `related_room_a` và `related_room_b` tương ứng, đặt cờ `is_shared_boundary = True`
5. Lưu để phục vụ tính toán BR-06

**Alternate / Exception flow:**
- Cửa gần ranh giới nhưng 2 phòng không thực sự kề nhau → không đặt `is_shared_boundary`, chỉ gán 1 phòng

**Acceptance criteria:**
- [ ] **Given** cửa D2 nằm trên tường chung giữa phòng "Phong ngu" và "Phong khach", **Then** `related_room_a` = phòng ngủ, `related_room_b` = phòng khách, `is_shared_boundary = True`
- [ ] **Given** cửa D1 chỉ thuộc 1 phòng, **Then** `related_room_b = None`, `is_shared_boundary = False`
- [ ] Trong báo cáo Excel, cột "Phong lien quan" của cửa ranh giới chung hiển thị tên 2 phòng (ví dụ: "Phong ngu / Phong khach")
- [ ] Flag `is_shared_boundary` được truyền đúng sang bước tính toán khối lượng tường (US-CALC-003)

**Business rules:** BR-03, BR-06  
**Ghi chú QA:** Tạo DXF synthetic với 2 phòng kề nhau, cửa thông giữa 2 phòng, verify cả 2 phòng đều ghi nhận cửa này

---

### EPIC 4: CALC – Tính toán số liệu

---

#### US-CALC-001 – Tính diện tích và chu vi phòng

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-CALC-001 |
| **Epic** | Tính toán số liệu |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-12, FR-13, NFR-04 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống tính đúng diện tích và chu vi mỗi phòng từ đường bao đã nhận diện, để có số liệu chính xác phục vụ tính khối lượng hoàn thiện.

**Mô tả chi tiết:**  
Python dùng Shapely Polygon để tính `.area` (m²) và `.length` (m) từ LWPOLYLINE đã chuyển đổi đơn vị (DXF đơn vị mm → chia 1,000,000 cho area, chia 1,000 cho length).

**Preconditions:**
- Room polygon đã được tạo và khép kín (US-ROOM-001, US-ROOM-002)
- Đơn vị DXF là mm (xác nhận trước khi tính)

**Main flow:**
1. Python load LWPOLYLINE coordinates, tạo Shapely Polygon
2. Kiểm tra polygon hợp lệ: `polygon.is_valid == True` và `polygon.is_simple == True`
3. Tính `area = polygon.area / 1_000_000` (m²)
4. Tính `perimeter = polygon.length / 1000` (m)
5. Làm tròn 2 chữ số thập phân
6. Lưu vào Room object

**Alternate / Exception flow:**
- Polygon không valid (self-intersecting) → cố sửa với `polygon.buffer(0)`, nếu vẫn invalid → cảnh báo, loại phòng đó khỏi tính toán
- Đơn vị DXF không phải mm (phát hiện qua header `$INSUNITS`) → cảnh báo và yêu cầu xác nhận hệ số quy đổi

**Acceptance criteria:**
- [ ] **Given** phòng hình chữ nhật 5000mm × 4000mm (đơn vị DXF: mm), **Then** `area = 20.00 m²`, `perimeter = 18.00 m`
- [ ] **Given** phòng hình chữ L, **Then** diện tích và chu vi tính bằng Shapely cho kết quả khớp trong ±0.01m² / ±0.01m so với tính tay
- [ ] **Given** cùng đầu vào chạy 2 lần, **Then** kết quả giống nhau hoàn toàn (NFR-04)
- [ ] Giá trị `area` và `perimeter` trong báo cáo Excel là số thực, không phải chuỗi
- [ ] Đơn vị hiển thị trong Excel: m² và m, ghi rõ trong header cột

**Business rules:** NFR-04 (nhất quán)  
**Input:** Shapely Polygon từ LWPOLYLINE  
**Output:** `area` (m²), `perimeter` (m) trong Room object  
**Ghi chú QA:** Tạo golden dataset 5 phòng đã có kết quả tính tay, chạy regression test

---

#### US-CALC-002 – Xuất chiều dài từng cạnh phòng

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-CALC-002 |
| **Epic** | Tính toán số liệu |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-14, NFR-03 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn biết chiều dài từng cạnh của mỗi phòng, để có thể đối chiếu và kiểm tra số liệu theo từng đoạn tường cụ thể.

**Mô tả chi tiết:**  
Python lấy `exterior.coords` của Shapely Polygon, tính khoảng cách giữa các cặp điểm kề nhau để ra chiều dài từng đoạn cạnh. Đánh index theo thứ tự cạnh (edge_index: 1, 2, 3...).

**Preconditions:**
- Room polygon hợp lệ đã có (US-CALC-001 done)

**Main flow:**
1. Lấy danh sách vertices từ `polygon.exterior.coords`
2. Với mỗi cặp điểm liên tiếp, tính `distance = sqrt((x2-x1)² + (y2-y1)²) / 1000` (m)
3. Tạo Edge object: `{internal_room_id, edge_index, edge_length}`
4. Lưu danh sách `edge_list` vào Room object

**Alternate / Exception flow:**
- Polygon có đỉnh trùng nhau (cạnh dài 0) → bỏ cạnh đó, không đưa vào edge_list
- Polygon có >100 đỉnh (phòng phức tạp bất thường) → xử lý bình thường, không giới hạn

**Acceptance criteria:**
- [ ] **Given** phòng hình chữ nhật (4 đỉnh), **Then** `edge_list` có 4 cạnh, tổng = perimeter ± 0.01m
- [ ] **Given** phòng chữ L (6 đỉnh), **Then** `edge_list` có 6 cạnh, tổng = perimeter
- [ ] Không có cạnh nào có `edge_length = 0` trong output
- [ ] Sheet "Chi tiet canh" trong Excel có đúng số hàng = tổng số cạnh của tất cả phòng
- [ ] `edge_index` bắt đầu từ 1, tăng dần liên tiếp cho mỗi phòng

**Input:** Shapely Polygon exterior coords  
**Output:** List of Edge objects `{internal_room_id, edge_index, edge_length}`  
**Ghi chú QA:** Sum tất cả `edge_length` của 1 phòng phải khớp với `perimeter`

---

#### US-CALC-003 – Tính khối lượng hoàn thiện bề mặt tường (có trừ cửa)

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-CALC-003 |
| **Epic** | Tính toán số liệu |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-16, FR-17, BR-05, BR-06 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống tính đúng diện tích hoàn thiện bề mặt tường bên trong mỗi phòng, bao gồm trừ phần diện tích cửa đúng theo quy tắc nghiệp vụ, để số liệu tô trát phản ánh thực tế.

**Mô tả chi tiết:**  
Công thức cơ bản: `S_to = perimeter × H - ΣS_cua`  
Trong đó `H` là chiều cao thông thủy (user nhập hoặc cấu hình mặc định), `S_cua` là tổng diện tích cửa liên quan.  
**Quy tắc BR-06:** Cửa trên ranh giới chung giữa 2 phòng → trừ `S_cua` 2 lần (mỗi phòng trừ 1 lần).  
Cửa chỉ thuộc 1 phòng → phòng đó trừ `S_cua` 1 lần.

**Preconditions:**
- `perimeter` đã tính (US-CALC-001)
- Danh sách cửa gán vào phòng đã có (US-DOOR-002, US-DOOR-003)
- `applied_height` đã được cấu hình (user nhập hoặc default từ config)

**Main flow:**
1. Python nhận `perimeter`, `applied_height`, danh sách cửa liên quan, flag `is_shared_boundary`
2. Tính `S_gross = perimeter × applied_height`
3. Với mỗi cửa liên quan:
   - Nếu `is_shared_boundary = False`: trừ `door.area` một lần
   - Nếu `is_shared_boundary = True` và cả 2 phòng đều trong phạm vi tính: trừ `door.area` một lần cho **mỗi** phòng (tổng cộng trừ 2 lần trên toàn hệ thống)
4. `wall_finish_quantity = S_gross - Σ(door_area)` (m²)
5. Lưu vào Room object

**Alternate / Exception flow:**
- `applied_height` = 0 hoặc không được nhập → cảnh báo, dừng tính, yêu cầu nhập lại
- Không có cửa liên quan → `wall_finish_quantity = perimeter × H` (không trừ gì)
- Cửa invalid (thiếu width/height) → không trừ, log warning tên cửa đó

**Acceptance criteria:**
- [ ] **Given** phòng P1 có `perimeter = 18m`, `H = 2.8m`, 1 cửa D1 rộng 0.9m cao 2.1m (S_cua = 1.89m²) chỉ thuộc P1, **Then** `wall_finish = 18×2.8 - 1.89 = 48.51 m²`
- [ ] **Given** phòng P1 và P2 kề nhau, cửa D2 trên ranh giới chung (S_cua = 1.89m²), **Then** P1 bị trừ 1.89m², P2 cũng bị trừ 1.89m² – không chia đôi
- [ ] **Given** cửa invalid không có kích thước, **Then** `wall_finish` không trừ cửa đó, log warning rõ ràng
- [ ] **Given** `applied_height` chưa nhập, **Then** hệ thống không tính và cảnh báo trước khi xuất báo cáo
- [ ] Kết quả `wall_finish_quantity` ≥ 0 trong mọi trường hợp (không ra số âm)

**Business rules:** BR-05, BR-06  
**Input:** Room, applied_height, danh sách Door với flag  
**Output:** `wall_finish_quantity` (m²)  
**Ghi chú QA:** Đây là rule nghiệp vụ quan trọng nhất – cần test riêng với pytest, ít nhất 5 test case covering BR-06

---

#### US-CALC-004 – Tính khối lượng hoàn thiện bề mặt sàn

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-CALC-004 |
| **Epic** | Tính toán số liệu |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-15, BR-04 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống tính khối lượng hoàn thiện bề mặt sàn cho mỗi phòng bằng diện tích phòng, để phục vụ bóc tách nhanh mà không phải đo lại.

**Mô tả chi tiết:**  
Theo BR-04, khối lượng hoàn thiện sàn = diện tích phòng. Không có hệ số nhân mặc định trong SRS. Nếu cần hệ số quy đổi vật liệu, sẽ được cấu hình bên ngoài (không thuộc scope SRS này).

**Preconditions:**
- `area` đã tính (US-CALC-001)

**Main flow:**
1. `floor_finish_quantity = area` (m²)
2. Lưu vào Room object

**Alternate / Exception flow:**
- `area = 0` (polygon degenerate) → không tính, cảnh báo phòng đó

**Acceptance criteria:**
- [ ] **Given** phòng có `area = 20.00 m²`, **Then** `floor_finish_quantity = 20.00 m²`
- [ ] Giá trị `floor_finish_quantity` trong báo cáo Excel bằng đúng `area`
- [ ] Đơn vị m² ghi rõ trong header Excel

**Business rules:** BR-04  
**Ghi chú QA:** Regression test đơn giản nhưng cần có để catch nếu ai đó vô tình thêm hệ số

---

#### US-CALC-005 – Nhập và áp dụng chiều cao thông thủy

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-CALC-005 |
| **Epic** | Tính toán số liệu |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-16, BR-05 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn nhập giá trị chiều cao thông thủy trước khi chạy tính toán, để số liệu tường phản ánh đúng công trình thực tế.

**Mô tả chi tiết:**  
Giao diện PySide6 có ô nhập `applied_height` (m) với giá trị mặc định đề xuất là `2.8`. Giá trị này áp dụng đồng nhất cho toàn bộ phòng trong một lần xử lý (giả định chiều cao đồng nhất). Nếu cần chiều cao khác nhau theo phòng → scope mở rộng, chưa có trong SRS.

**Preconditions:**
- Giao diện đang ở trạng thái sẵn sàng chạy tính toán

**Main flow:**
1. User nhập `applied_height` vào ô text trên UI (đơn vị: m)
2. Hệ thống validate: giá trị > 0 và ≤ 10 (giới hạn hợp lý, tránh nhập sai đơn vị)
3. Lưu giá trị vào cấu hình phiên làm việc hiện tại
4. Dùng giá trị này trong US-CALC-003

**Alternate / Exception flow:**
- Nhập giá trị âm hoặc 0 → báo lỗi validation ngay trên UI
- Nhập ký tự chữ → báo lỗi "Phai nhap so"
- Nhập > 10 → cảnh báo "Gia tri bat thuong, vui long xac nhan" nhưng vẫn cho phép tiếp tục

**Acceptance criteria:**
- [ ] Ô nhập `applied_height` có giá trị mặc định hiển thị (đề xuất: 2.8)
- [ ] **Given** user nhập `3.0`, **Then** tất cả tính toán tường dùng H = 3.0
- [ ] **Given** user nhập `-1`, **Then** hệ thống hiển thị lỗi validation, không cho chạy
- [ ] **Given** user nhập `abc`, **Then** hệ thống hiển thị lỗi "Phai nhap so"
- [ ] Giá trị `applied_height` được ghi vào log / báo cáo để truy vết

---

### EPIC 5: EXPORT – Xuất báo cáo

---

#### US-EXP-001 – Xuất báo cáo Excel tổng hợp sau một lần xử lý

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-EXP-001 |
| **Epic** | Xuất báo cáo |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-18, FR-22, NFR-03, NFR-06 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn xuất toàn bộ kết quả ra file Excel sau một lần xử lý toàn phạm vi đã chọn, để có ngay bảng số liệu hoàn chỉnh mà không cần xử lý từng phòng rồi gộp lại.

**Mô tả chi tiết:**  
Python dùng `openpyxl` tạo file Excel multi-sheet. Tên file mặc định có timestamp. User có thể chỉ định thư mục xuất. Toàn bộ phòng + cửa + cạnh được xuất trong cùng 1 lần export.

**Preconditions:**
- Tất cả bước tính toán đã hoàn thành (US-CALC-001 đến US-CALC-004 done)
- Ít nhất 1 phòng hợp lệ tồn tại

**Main flow:**
1. User click "Xuat Excel" trên UI
2. Hệ thống mở dialog chọn thư mục xuất (hoặc dùng thư mục mặc định)
3. Python tạo file `.xlsx` với tên: `BokTach_[timestamp].xlsx`
4. Ghi 3 sheet: "Tong hop phong", "Chi tiet cua", "Chi tiet canh"
5. Hiển thị progress bar trong quá trình ghi
6. Thông báo thành công + path file khi xong
7. Cho phép mở file ngay từ UI (nút "Mo file")

**Alternate / Exception flow:**
- Thư mục xuất không có quyền ghi → thông báo lỗi, gợi ý chọn thư mục khác
- Không có phòng hợp lệ nào → thông báo "Chua co du lieu de xuat", không tạo file
- File cùng tên đã tồn tại → hỏi user: ghi đè hay tạo tên mới

**Acceptance criteria:**
- [ ] File Excel được tạo thành công với 3 sheet đúng tên
- [ ] Tổng số hàng ở sheet "Tong hop phong" = số phòng hợp lệ đã xử lý
- [ ] **Given** 5 phòng và 8 cửa, **Then** "Tong hop phong" có 5 hàng dữ liệu, "Chi tiet cua" có 8 hàng
- [ ] Không có ô nào có giá trị `None` hoặc `NaN` trong các cột số (thay bằng 0 hoặc để trống rõ ràng)
- [ ] File có thể mở được bằng Excel/LibreOffice mà không có warning corrupt
- [ ] Progress bar cập nhật trong quá trình ghi, UI không bị freeze

**Input:** Toàn bộ Room, Door, Edge objects đã tính toán  
**Output:** File .xlsx multi-sheet  
**Ghi chú QA:** Mở file Excel và verify thủ công 2-3 phòng so với kết quả preview UI

---

#### US-EXP-002 – Nội dung sheet "Tổng hợp phòng"

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-EXP-002 |
| **Epic** | Xuất báo cáo |
| **Priority** | P0 – Critical |
| **FR/BR/NFR** | FR-19, NFR-03 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn sheet "Tổng hợp phòng" có đầy đủ các cột số liệu theo từng phòng, để có thể kiểm tra và sử dụng tiếp trong bảng tính dự toán.

**Acceptance criteria (theo cột bắt buộc):**
- [ ] Cột `Ma phong` – giá trị từ `room_code`
- [ ] Cột `Ten phong` – giá trị từ `room_name`
- [ ] Cột `Dien tich (m2)` – giá trị `area`, 2 chữ số thập phân
- [ ] Cột `Chu vi (m)` – giá trị `perimeter`, 2 chữ số thập phân
- [ ] Cột `Chieu cao ap dung (m)` – giá trị `applied_height`
- [ ] Cột `So cua` – số lượng cửa liên quan
- [ ] Cột `Tong dien tich cua (m2)` – tổng `door.area` liên quan, đã quy đổi m²
- [ ] Cột `KL hoan thien san (m2)` – `floor_finish_quantity`
- [ ] Cột `KL xu ly tuong (m2)` – `wall_finish_quantity`
- [ ] Hàng tổng cộng ở cuối sheet (sum các cột số)
- [ ] Header row được format (bold, background color)
- [ ] Các cột số được format dạng number (không phải text)

**Ghi chú QA:** Kiểm tra hàng tổng: `sum(area)` của tất cả phòng phải khớp với tổng trong cell tổng cộng

---

#### US-EXP-003 – Nội dung sheet "Chi tiết cửa" và "Chi tiết cạnh"

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-EXP-003 |
| **Epic** | Xuất báo cáo |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-20, FR-14, NFR-03 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn có sheet chi tiết cửa và chi tiết cạnh để kiểm tra từng đối tượng riêng lẻ khi cần đối chiếu.

**Acceptance criteria – sheet "Chi tiet cua":**
- [ ] Cột: `Ma cua`, `Ten cua`, `Chieu rong (mm)`, `Chieu cao (mm)`, `Dien tich cua (m2)`, `Phong lien quan`
- [ ] Cửa trên ranh giới chung: cột "Phong lien quan" hiển thị tên 2 phòng, phân cách bởi " / "
- [ ] `Dien tich cua (m2)` = `width_mm × height_mm / 1_000_000`, làm tròn 4 chữ số thập phân

**Acceptance criteria – sheet "Chi tiet canh":**
- [ ] Cột: `Ma phong`, `Ten phong`, `Thu tu canh`, `Chieu dai canh (m)`
- [ ] Mỗi phòng có đúng số cạnh tương ứng với số đỉnh polygon
- [ ] Tổng `Chieu dai canh` của 1 phòng = `Chu vi` phòng đó (±0.001m dung sai làm tròn)

---

#### US-EXP-004 – Kiểm tra lại kết quả theo từng phòng trên UI

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-EXP-004 |
| **Epic** | Xuất báo cáo |
| **Priority** | P2 – Medium |
| **FR/BR/NFR** | FR-21, FR-24, NFR-03 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn xem trước kết quả tính toán từng phòng ngay trên giao diện trước khi xuất Excel, để phát hiện sai số trước khi lưu file chính thức.

**Acceptance criteria:**
- [ ] UI hiển thị bảng kết quả tổng hợp sau khi xử lý xong (trước khi xuất Excel)
- [ ] Có thể click vào từng phòng để xem chi tiết: diện tích, chu vi, danh sách cửa, danh sách cạnh
- [ ] Phòng có cảnh báo (thiếu tên, cửa invalid) được highlight màu khác trong bảng
- [ ] User có thể scroll qua toàn bộ danh sách phòng

---

### EPIC 6: ALERT – Cảnh báo và xử lý lỗi

---

#### US-ALERT-001 – Cảnh báo phòng không nhận diện được hoặc thiếu thông tin

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-ALERT-001 |
| **Epic** | Cảnh báo / Lỗi / Kiểm tra lại |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-23, NFR-07, BR-01, BR-07 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống cảnh báo rõ ràng khi có phòng không nhận diện được hoặc thiếu tên/mã, để tôi biết chỗ nào cần kiểm tra lại trước khi dùng kết quả.

**Acceptance criteria:**
- [ ] **Given** phòng không có text tên/mã trong bản vẽ, **Then** hệ thống cảnh báo: "Phong [ID] chua co ten hoac ma phong"
- [ ] **Given** BPOLY không tạo được polyline khép kín tại điểm click, **Then** LISP cảnh báo ngay trên command line AutoCAD
- [ ] **Given** polygon tạo ra không valid (self-intersecting), **Then** Python cảnh báo: "Phong [ID] co ranh gioi khong hop le, bo qua"
- [ ] Tất cả cảnh báo được tổng hợp vào một log file `warnings_[timestamp].txt`
- [ ] Sau khi xử lý xong, UI hiển thị tóm tắt: "X phong hop le, Y phong canh bao" trước khi cho xuất Excel

---

#### US-ALERT-002 – Cảnh báo cửa thiếu dữ liệu hoặc không gán được phòng

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-ALERT-002 |
| **Epic** | Cảnh báo / Lỗi / Kiểm tra lại |
| **Priority** | P1 – High |
| **FR/BR/NFR** | FR-23, NFR-07, BR-02 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống cảnh báo khi cửa thiếu kích thước hoặc không gán được vào phòng nào, để không bị tính toán thiếu mà không biết.

**Acceptance criteria:**
- [ ] **Given** cửa D1 không có width/height, **Then** cảnh báo: "Cua D1: Thieu kich thuoc, khong tinh vao kq"
- [ ] **Given** cửa nằm ngoài mọi phòng sau buffer, **Then** cảnh báo: "Cua [ma]: Khong xac dinh duoc phong"
- [ ] Cửa invalid/unassigned KHÔNG được trừ trong tính toán tường, KHÔNG xuất hiện trong tổng số cửa của phòng
- [ ] Số lượng cảnh báo cửa được hiển thị trên UI sau khi xử lý

---

#### US-ALERT-003 – Cảnh báo dữ liệu trùng lặp

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-ALERT-003 |
| **Epic** | Cảnh báo / Lỗi / Kiểm tra lại |
| **Priority** | P2 – Medium |
| **FR/BR/NFR** | FR-06, FR-23, NFR-07 |

**User story:**  
Là người thực hiện bóc tách, tôi muốn hệ thống cảnh báo khi phát hiện dữ liệu trùng lặp (phòng click 2 lần, mã cửa duplicate trong Excel), để tôi biết dữ liệu đầu vào cần được làm sạch.

**Acceptance criteria:**
- [ ] **Given** user click 2 lần vào cùng 1 phòng, **Then** sau deduplicate, cảnh báo: "Phong [ID] duoc nhan dien nhieu lan, giu 1 ket qua"
- [ ] **Given** file Excel cửa có 2 dòng cùng mã `D1`, **Then** cảnh báo: "Ma cua D1 bi trung trong Excel, su dung dong dau tien"
- [ ] Cảnh báo trùng lặp được ghi vào warning log, không block luồng xử lý chính

---

### EPIC 7: OPS – Vận hành và packaging

---

#### US-OPS-001 – Đóng gói thành file .exe chạy được trên Windows

| Thuộc tính | Nội dung |
|---|---|
| **Story ID** | US-OPS-001 |
| **Epic** | Packaging / Vận hành |
| **Priority** | P1 – High |
| **FR/BR/NFR** | NFR-06 |

**User story:**  
Là người dùng cuối không phải lập trình viên, tôi muốn chạy tool bằng file .exe không cần cài Python, để tự dùng được mà không cần hỗ trợ kỹ thuật mỗi lần.

**Acceptance criteria:**
- [ ] File `.exe` build bằng PyInstaller chạy được trên Windows 10/11 (64-bit)
- [ ] Không yêu cầu cài Python hoặc bất kỳ dependency nào trước khi chạy
- [ ] Giao diện PySide6 mở được trong vòng 5 giây trên máy cấu hình thấp (Core i5, 8GB RAM)
- [ ] AutoLISP files (.lsp) được distribute kèm với hướng dẫn load vào AutoCAD
- [ ] File .exe được ký code (code signing) hoặc có hướng dẫn bypass SmartScreen nếu chưa ký

**Giả định:** PyInstaller sử dụng chế độ `--onedir` thay vì `--onefile` để tránh antivirus false positive.

---

## 4. Acceptance Criteria Standards

Acceptance criteria trong tài liệu này tuân theo các nguyên tắc sau:

| Nguyên tắc | Mô tả |
|---|---|
| **Observable** | Kết quả phải nhìn/đo được: giá trị số cụ thể, trạng thái UI, nội dung file |
| **Testable** | QA có thể viết test case tương ứng mà không cần giải thích thêm |
| **Specific** | Không dùng từ chung chung: "đúng", "hợp lệ", "bình thường" – phải kèm định nghĩa |
| **Independent** | Mỗi criterion kiểm tra một hành vi, không gộp 2 điều kiện vào 1 bullet |
| **Boundary-explicit** | Dung sai số học phải được ghi rõ (ví dụ: ±0.01m², ≤2%) |

**Ví dụ viết đúng:**
> `floor_finish_quantity = 20.00 m²` (khi area = 20.00 m²)

**Ví dụ viết sai:**
> ~~"Diện tích sàn được tính đúng"~~ (không đo được)

---

## 5. Edge Cases và Negative Cases

### 5.1. Phòng không khép kín

| ID | Scenario | Hành vi mong đợi |
|---|---|---|
| EC-01 | BPOLY không thể tạo vùng kín tại điểm click (tường hở) | LISP cảnh báo ngay, không tạo polyline, cho phép user click lại |
| EC-02 | Shapely Polygon nhận vào coords không tạo thành vùng khép kín | Python log error, loại phòng đó, không crash |
| EC-03 | Polygon tạo ra là self-intersecting (figure-8) | Thử `buffer(0)` để repair; nếu vẫn fail → loại, cảnh báo |
| EC-04 | Phòng có ranh giới mở ở vị trí cửa (tường bị cắt) | AutoLISP áp dụng "Door Sealing" (vẽ Line tạm), sau khi lấy boundary thì xóa Line tạm |

### 5.2. Text phòng nằm sai vùng

| ID | Scenario | Hành vi mong đợi |
|---|---|---|
| EC-05 | Text "PHONG NGU" nằm bên ngoài polygon phòng ngủ (do người vẽ đặt sai) | Không gán text đó vào phòng; phòng bị cảnh báo "chua co ten" |
| EC-06 | Text nằm trên đúng đường biên polygon (insertion point on edge) | Áp dụng "gần nhất tính theo tâm phòng" để phân biệt; log warning |
| EC-07 | Không có text nào trong bản vẽ (mặt bằng không có annotation) | Tất cả phòng đặt `room_name = "Chua_dinh_danh"`, `room_code = "ROOM_[n]"`; cảnh báo |

### 5.3. Dữ liệu cửa thiếu width/height

| ID | Scenario | Hành vi mong đợi |
|---|---|---|
| EC-08 | Cửa có `width = 0` hoặc `height = 0` | Đánh dấu invalid, không đưa vào tính toán trừ, cảnh báo tên cửa |
| EC-09 | Cửa có `width = NULL` trong Excel | Giống EC-08, cảnh báo cụ thể: "Cot rong_mm bi rong tai dong [n]" |
| EC-10 | Mã cửa trong bản vẽ không có trong file Excel | Đọc attribute block trực tiếp; nếu block không có attribute → cảnh báo |

### 5.4. Cửa nằm giữa 2 phòng

| ID | Scenario | Hành vi mong đợi |
|---|---|---|
| EC-11 | Cửa insertion point nằm chính xác trên đường biên chung | Xem xét buffer 50mm, nếu 2 phòng cùng trong buffer → `is_shared_boundary = True` |
| EC-12 | Cửa insertion point nằm trong vùng tường (giữa 2 mặt tường) | Tương tự EC-11, dùng buffer = chiều dày tường để phát hiện |
| EC-13 | Cửa `is_shared_boundary = True` nhưng 1 phòng nằm ngoài phạm vi xử lý | Chỉ trừ `door_area` cho phòng nằm trong phạm vi; không trừ cho phòng ngoài |

### 5.5. Dữ liệu trùng lặp

| ID | Scenario | Hành vi mong đợi |
|---|---|---|
| EC-14 | User click 2 lần vào cùng 1 phòng | Deduplicate: giữ polyline đầu tiên, log warning |
| EC-15 | Mã cửa D1 xuất hiện 2 lần trong Excel | Dùng record đầu tiên, cảnh báo: "Ma cua D1 bi trung, dung dong [n]" |
| EC-16 | 2 text giống hệt nhau nằm trong cùng 1 phòng | Gán cả 2 vào `room_name` dưới dạng concatenate; log warning yêu cầu QA kiểm tra |

### 5.6. Đơn vị bản vẽ không nhất quán

| ID | Scenario | Hành vi mong đợi |
|---|---|---|
| EC-17 | `$INSUNITS` trong DXF header = 0 (unitless) hoặc không phải mm | Cảnh báo: "Don vi ve khong xac dinh hoac khong phai mm", yêu cầu user xác nhận hệ số quy đổi |
| EC-18 | Bản vẽ dùng đơn vị m thay vì mm | Mọi tính toán bị lệch 10^6 lần nếu không detect → phải có validation step kiểm tra `$INSUNITS` |
| EC-19 | Mix đơn vị (một phần bản vẽ mm, phần khác cm) | Không xử lý tự động, cảnh báo và yêu cầu chuẩn hóa đầu vào trước |

### 5.7. Không export được file

| ID | Scenario | Hành vi mong đợi |
|---|---|---|
| EC-20 | Thư mục xuất không có quyền write | Thông báo lỗi rõ ràng kèm đường dẫn, gợi ý chọn thư mục khác |
| EC-21 | Disk full | Catch exception IOError, hiển thị "Khong du dung luong dia" |
| EC-22 | File Excel đang mở bởi Excel.exe (locked) | Thông báo: "File dang duoc mo boi chuong trinh khac, vui long dong lai" |
| EC-23 | Một phần phòng tính toán lỗi nhưng phần còn lại OK | Xuất các phòng hợp lệ, ghi phòng lỗi vào log, thông báo "Xuat that bai X phong, thanh cong Y phong" |

---

## 6. Traceability Matrix

| Story ID | FR / BR / NFR liên quan | Epic | Loại test gợi ý |
|---|---|---|---|
| US-INP-001 | FR-01, NFR-07 | Input | Integration, UAT |
| US-INP-002 | FR-02, NFR-06 | Input | Integration, UAT |
| US-INP-003 | FR-03, FR-09, BR-02 | Input | Unit, Integration |
| US-ROOM-001 | FR-04, FR-05, BR-01 | Nhận diện phòng | Integration, UAT |
| US-ROOM-002 | FR-05, FR-04 | Nhận diện phòng | Integration, UAT |
| US-ROOM-003 | FR-06, BR-01 | Nhận diện phòng | Unit, Regression |
| US-ROOM-004 | FR-07, BR-07, NFR-03 | Nhận diện phòng | Unit, Integration |
| US-DOOR-001 | FR-08, FR-09, BR-02 | Nhận diện cửa | Unit, Integration |
| US-DOOR-002 | FR-10, FR-11, BR-03 | Nhận diện cửa | Unit, Integration |
| US-DOOR-003 | FR-10, FR-11, FR-17, BR-03, BR-06 | Nhận diện cửa | Unit, Integration, Regression |
| US-CALC-001 | FR-12, FR-13, NFR-04 | Tính toán | Unit, Regression |
| US-CALC-002 | FR-14, NFR-03 | Tính toán | Unit |
| US-CALC-003 | FR-16, FR-17, BR-05, BR-06 | Tính toán | Unit (pytest), Regression |
| US-CALC-004 | FR-15, BR-04 | Tính toán | Unit, Regression |
| US-CALC-005 | FR-16, BR-05 | Tính toán | Unit, UAT |
| US-EXP-001 | FR-18, FR-22, NFR-03, NFR-06 | Xuất báo cáo | Integration, UAT |
| US-EXP-002 | FR-19, NFR-03 | Xuất báo cáo | Integration, UAT |
| US-EXP-003 | FR-20, FR-14, NFR-03 | Xuất báo cáo | Integration |
| US-EXP-004 | FR-21, FR-24, NFR-03 | Xuất báo cáo | UAT |
| US-ALERT-001 | FR-23, NFR-07, BR-01, BR-07 | Cảnh báo | Unit, Integration |
| US-ALERT-002 | FR-23, NFR-07, BR-02 | Cảnh báo | Unit, Integration |
| US-ALERT-003 | FR-06, FR-23, NFR-07 | Cảnh báo | Unit |
| US-OPS-001 | NFR-06 | Vận hành | UAT (smoke test trên máy clean) |

### Mapping FR chưa có story riêng

| FR/BR | Story cover | Ghi chú |
|---|---|---|
| FR-08 (nhận diện cửa) | US-DOOR-001 | Covered |
| FR-11 (lưu quan hệ cửa-phòng) | US-DOOR-002, US-DOOR-003 | Covered |
| FR-22 (xử lý 1 lần) | US-EXP-001 | Covered qua AC của EXP-001 |
| BR-03 (cửa 1 hoặc 2 phòng) | US-DOOR-002, US-DOOR-003 | Covered |
| BR-06 (quy tắc cửa ranh giới chung) | US-DOOR-003, US-CALC-003 | **Critical – cần test riêng bằng pytest** |
| NFR-04 (nhất quán) | US-CALC-001 | AC kiểm tra chạy 2 lần cùng output |
| NFR-05 (mở rộng) | Không có story – design concern | Cần review architecture, không có AC nghiệp vụ cụ thể |

---

*Tài liệu này được soạn dựa trên SRS v1.0 và Techstack v1.0. Mọi thay đổi scope cần cập nhật đồng thời cả SRS và tài liệu này.*

*Version 1.0 – Chờ review BA + QA Lead trước khi đưa vào sprint planning.*
