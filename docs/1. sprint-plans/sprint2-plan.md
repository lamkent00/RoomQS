# SPRINT BRIEF

Sprint: Sprint 2 — Room Recognition Prototype ⚠️
Phase: GIAI ĐOẠN 2 — PROTOTYPE & VALIDATE
Mục tiêu sprint: Validate thuật toán nhận diện phòng (XR + GB) trên bản vẽ thực. Đây là **go/no-go decision point** của toàn dự án. Nếu không đạt ngưỡng → PM quyết định re-estimate hoặc thu hẹp scope trước khi tiếp tục.

In-scope:
- BL-07: Parser DXF — đọc INSERT block cửa + attributes (Dev-A, 1.5 ngày)
- BL-08: Cơ chế config layer name — không hard-code, đọc từ config.yaml (Dev-B, 1 ngày)
- BL-10: [PROTOTYPE] AutoLISP thuật toán XR — phòng vuông vức (Dev-B, 3–4 ngày) — **PRIORITY CAO NHẤT**
- BL-11: [PROTOTYPE] AutoLISP thuật toán GB — phòng L-shape (Dev-B, 3–4 ngày)

Out-of-scope:
- LISP → JSON export (BL-13 — Sprint 3)
- Python parse JSON (BL-14 — Sprint 3)
- Door Sealing (BL-12 — Sprint 3)
- Gắn tên phòng (BL-15 — Sprint 3)
- Unit test tính toán (Sprint 4)
- Bất kỳ feature UI nào
- XR/GB cho case phức tạp hơn L-shape (Phase 2)

Risks:
- BPOLY bị "nhiễu" bởi nội thất, hatch, rác ngắn < 300mm → GB lọc theo `short_segment_threshold_mm=300` trong config
- Layer tường không khớp tên cấu hình → BL-08 xử lý; nhưng nếu file DXF thực có convention khác → cần re-config ngay
- Phòng L-shape phức tạp hơn dự kiến → GB có thể không đạt ngưỡng 2/3; nếu vậy → PM quyết định thu hẹp MVP
- Không có AutoCAD 2019+ → BLOCKER cứng cho BL-10/BL-11

Dependencies:
- Sprint 1 exit criteria pass (CI, .exe prototype, DXF parser)
- AutoCAD 2019+ trên máy Dev-B (xác nhận từ Sprint 0 T0-06)
- Sample DXF thực có phòng vuông + L-shape (từ Sprint 0 T0-01)
- config.yaml đã có section `cad.wall_layer_names` và `cad.short_segment_threshold_mm`

Danh sách ticket:
1. T2-01: BL-08 — Config layer name (không hard-code)
2. T2-02: BL-07 — Parser INSERT block cửa + attributes
3. T2-03: BL-10 — [PROTOTYPE] AutoLISP thuật toán XR
4. T2-04: BL-11 — [PROTOTYPE] AutoLISP thuật toán GB
5. T2-05: Báo cáo prototype + demo cho PM/BA

---

# TICKET CONTEXT PACK

Ticket: T2-01 — BL-08 Config layer name — không hard-code
Người phụ trách: Dev-B
Mục tiêu: Cơ chế đọc layer name từ config.yaml thay vì hard-code trong LISP/Python, để hệ thống có thể dùng được trên nhiều file bản vẽ có convention layer khác nhau.

**Bối cảnh kỹ thuật:**
File bản vẽ của các dự án khác nhau có thể đặt tên layer tường là "TUONG", "A-WALL", "WALL", "Tuong", v.v. Hard-code là rủi ro cao. Cơ chế: Python đọc `config.yaml` → pass `wall_layer_names` vào DXF parser; LISP đọc từ file config riêng hoặc nhận tham số khi gọi lệnh.

In scope:
- Module `src/config/config_loader.py`:
  - Hàm `load_config(path: str = "config.yaml") -> dict`
  - Đọc section `cad.wall_layer_names` trả về list string
  - Đọc `cad.short_segment_threshold_mm` (float)
- LISP side: tạo hàm `(defun get-wall-layers ())` đọc từ biến toàn cục hoặc nhận qua prompt
- Unit test: load config mock và verify đúng giá trị

Out of scope:
- UI để user nhập layer name (trong MVP, chỉ sửa config.yaml trực tiếp)
- Dynamic reload config khi app đang chạy

Story IDs: US-INP-001 (ngầm định), US-ROOM-001 (precondition layer tường)
Acceptance Criteria IDs: Dẫn xuất từ ADR-04

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: `load_config()` đọc `config.yaml` và trả về dict với đủ keys `cad`, `calculation`, `export`
- AC-02: `config["cad"]["wall_layer_names"]` là list string, match case-insensitive
- AC-03: `config["cad"]["short_segment_threshold_mm"]` là float = 300.0 (default)
- AC-04: Nếu `config.yaml` không tồn tại → raise `FileNotFoundError` với message rõ ràng
- AC-05: LISP lấy được danh sách layer tường từ config (hoặc biến LISP) để dùng trong XR/GB

Module boundary:
- `src/config/config_loader.py` — đọc file, không có logic nghiệp vụ
- `lisp/config_helper.lsp` hoặc biến LISP toàn cục

Files/Modules dự kiến bị ảnh hưởng:
- `src/config/__init__.py`, `src/config/config_loader.py` (tạo mới)
- `config/config.yaml` (đã có template từ T0-03, nay thêm giá trị cụ thể)
- `tests/unit/test_config_loader.py` (tạo mới)

Doc refs:
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-04: Quản lý cấu hình rule nghiệp vụ
- /docs/02-PRD-Product-Backlog.md#Rủi ro dữ liệu DXF (layer naming)

Dependencies: T0-03 (config.yaml template đã có)

Known risks:
- LISP không đọc được YAML trực tiếp → cần cơ chế truyền qua file .ini đơn giản hoặc biến toàn cục LISP

Open ambiguities:
- LISP đọc config từ đâu? Phương án đề xuất: Python write ra `lisp_config.dcl` hoặc LISP prompt user nhập layer name khi chưa có config.

Definition of Done:
- [ ] `config_loader.py` đọc được config.yaml
- [ ] Unit test pass
- [ ] LISP có thể lấy wall_layer_names (qua bất kỳ cơ chế nào đã thống nhất)
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T2-02 — BL-07 Parser INSERT block cửa + attributes
Người phụ trách: Dev-A
Mục tiêu: Module `door_engine` đọc được các INSERT entity (block cửa) từ DXF, lấy `door_code` từ tên block hoặc attribute, và `position` (insertion point) — làm nền cho door mapping ở Sprint 3–4.

**Bối cảnh kỹ thuật:**
INSERT entity trong ezdxf: `entity.dxf.name` là tên block (thường là mã cửa như "D1", "D2"). Nếu là attributed block: `entity.attribs` chứa các ATTRIB entity với `tag` và `value`. Config `door_block_prefixes` dùng để filter block là cửa (loại bỏ block nội thất, ký hiệu kỹ thuật).

In scope:
- Module `src/door_engine/door_reader.py`:
  - Hàm `extract_door_blocks(doc, config: dict, bbox=None) -> list[DoorBlock]`
  - Lọc INSERT theo `door_block_prefixes` từ config
  - Đọc attribute block nếu có (ATTRIB entities)
- Data class `DoorBlock(door_code: str, position: tuple, raw_attributes: dict)`
- **Không** tra cứu kích thước (width/height) trong ticket này — làm ở Sprint 4 BL-19
- Unit test với DXF fixture có block cửa

Out of scope:
- Đọc width/height từ Excel (BL-19 — Sprint 4)
- Spatial assignment vào phòng (BL-17 — Sprint 3/4)
- Parse thuộc tính phức tạp (chỉ cần raw key-value)

Story IDs: US-DOOR-001
Acceptance Criteria IDs: US-DOOR-001 AC-01 đến AC-04

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-DOOR-001): Given bản vẽ có 5 block D1, D2, D3, DW, S1 trong phạm vi, Then hệ thống nhận diện đúng 5 DoorBlock với `door_code` đúng
- AC-02: Mỗi DoorBlock có `position` (x, y) đã normalize mm
- AC-03: Block không phải cửa (prefix không khớp `door_block_prefixes`) bị bỏ qua
- AC-04 (US-DOOR-001): Block có attribute → `raw_attributes` dict có đủ key-value
- AC-05: Unit test pass với fixture có 3 block cửa và 2 block không phải cửa

Module boundary:
- `src/door_engine/door_reader.py` — chỉ đọc, không tính toán
- Phụ thuộc `src/config/config_loader.py` (T2-01)
- Không gọi Shapely

Files/Modules dự kiến bị ảnh hưởng:
- `src/door_engine/__init__.py`, `src/door_engine/door_reader.py` (tạo mới)
- `src/door_engine/models.py` — DoorBlock
- `tests/unit/test_door_reader.py` (tạo mới)
- `tests/fixtures/` — cần fixture có INSERT block cửa

Doc refs:
- /docs/03-User-Stories.md#US-DOOR-001
- /docs/02-PRD-Product-Backlog.md#FR-08, FR-09
- /docs/04-Kien-Truc-Tech-Stack.md#Module Breakdown — door_engine

Dependencies: T2-01 (config_loader), T1-03 (read_dxf hàm chung)

Known risks:
- Block cửa trong bản vẽ thực có thể không dùng attribute — chỉ dùng block name làm mã cửa → cần verify với file DXF thực

Open ambiguities:
- Attribute tag tên cửa là gì? (Cần xem file DXF thực từ Sprint 0)

Definition of Done:
- [ ] `door_reader.py` extract đúng DoorBlock từ INSERT entity
- [ ] Unit test pass với fixture
- [ ] CI pass
- [ ] PR reviewed

---

# TICKET CONTEXT PACK

Ticket: T2-03 — BL-10 [PROTOTYPE] AutoLISP thuật toán XR (X-Ray)
Người phụ trách: Dev-B
Mục tiêu: Viết và validate prototype AutoLISP lệnh `XR` nhận diện phòng hình chữ nhật/vuông vức bằng thuật toán tia X-quang. **Đây là ticket rủi ro cao nhất Sprint 2 — phải pass hard gate: ≥ 4/5 phòng vuông trên file thực.**

**Bối cảnh thuật toán XR (X-Ray / Tia X-quang):**
Từ điểm click của user, LISP bắn 4 tia theo 4 hướng (+X, -X, +Y, -Y). Mỗi tia tìm điểm giao với LINE hoặc LWPOLYLINE trên layer tường gần nhất. Kết nối 4 điểm giao đó tạo ra LWPOLYLINE hình chữ nhật. Điều kiện: phòng phải có 4 mép tường song song tương đối. Lọc boundary set chỉ gồm layer tường (không lẫn nội thất/hatch).

**Ngưỡng pass prototype:**
- XR: ≥ 4/5 phòng hình chữ nhật từ file DXF thực tạo Polyline đúng
- Cửa không bị lẹm: ≥ 2/2 phòng có block cửa tạo boundary không lẹm diện tích

In scope:
- File `lisp/xr.lsp`:
  - Hàm `(defun c:XR ())` — lệnh user gọi trong AutoCAD
  - Prompt "Click 1 diem vao giua phong:"
  - Bắn 4 tia, tìm mép tường, tạo LWPOLYLINE đỏ, closed
  - Thông báo lỗi nếu không tìm đủ 4 mép ("Loi: Khong tim thay du 4 vach tuong!")
  - Lọc boundary set theo layer tường từ config
- Test thủ công trên file DXF thực: 5 phòng hình chữ nhật

Out of scope:
- Export JSON (BL-13 — Sprint 3)
- Door Sealing (BL-12 — Sprint 3)
- Phòng L-shape (BL-11 — T2-04)
- Bất kỳ logic Python nào

Story IDs: US-ROOM-001, US-ROOM-002
Acceptance Criteria IDs: US-ROOM-001 AC-01, AC-02, AC-03, AC-06; US-ROOM-002 AC-01

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-ROOM-001): Given user click điểm rõ ràng bên trong phòng HCN, When XR, Then LWPOLYLINE khép kín màu đỏ được tạo bao đúng phòng
- AC-02 (US-ROOM-001): LWPOLYLINE có color=1 (đỏ), lineweight=40, closed=True
- AC-03 (US-ROOM-001): Given click bên ngoài phòng, Then LISP thông báo lỗi, không tạo polyline sai
- AC-04 (US-ROOM-002): Given phòng có block cửa, Then LWPOLYLINE không bị lẹm vào vị trí cửa
- AC-05 (NGƯỠNG PROTOTYPE): ≥ 4/5 test case phòng HCN từ file DXF thực → Polyline đúng — **hard gate**
- AC-06 (NGƯỠNG PROTOTYPE): ≥ 2/2 phòng có cửa → boundary không lẹm diện tích — **hard gate**

Module boundary:
- `lisp/xr.lsp` — hoàn toàn trong AutoCAD/AutoLISP layer
- Không phụ thuộc Python (prototype phase)

Files/Modules dự kiến bị ảnh hưởng:
- `lisp/xr.lsp` (tạo mới)
- `lisp/README.md` (cập nhật: cách load và test XR)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-001, US-ROOM-002
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 2 — Acceptance ngưỡng prototype
- /docs/02-PRD-Product-Backlog.md#Rủi ro nhận diện phòng / cửa

Dependencies: T2-01 (config layer name — LISP cần biết wall_layer_names); AutoCAD 2019+ (T0-06)

Known risks:
- BPOLY bị nhiễu bởi hatch, nội thất → giải pháp: boundary set chỉ layer tường
- Tường hở tại vị trí cửa gây 4 tia không gặp đủ mép → Door Sealing là giải pháp (BL-12 Sprint 3); ở prototype: ghi nhận case này là "fail — cần Door Sealing"
- Phòng không vuông (góc không 90°) → XR sẽ fail → đây là use case của GB

Open ambiguities:
- Chiều dày tường ảnh hưởng đến cách đo "từ mép trong tường" — cần quyết định: LISP đo đến mép LINE tường hay đến tâm tường?

Definition of Done:
- [ ] `lisp/xr.lsp` load được vào AutoCAD 2019+ không báo lỗi
- [ ] Test thủ công 5 phòng HCN — ghi kết quả pass/fail từng case
- [ ] ≥ 4/5 pass — hard gate
- [ ] ≥ 2/2 phòng có cửa không bị lẹm — hard gate
- [ ] Kết quả ghi vào `docs/sprint2-prototype-report.md`

---

# TICKET CONTEXT PACK

Ticket: T2-04 — BL-11 [PROTOTYPE] AutoLISP thuật toán GB (Ghost Boundary)
Người phụ trách: Dev-B
Mục tiêu: Viết và validate prototype AutoLISP lệnh `GB` nhận diện phòng L-shape và phòng không vuông vức bằng thuật toán Ghost Boundary. **Ngưỡng: ≥ 2/3 phòng L-shape từ file thực.**

**Bối cảnh thuật toán GB (Ghost Boundary):**
GB dùng lệnh AutoCAD `-BOUNDARY` với boundary set được lọc. Khác với XR (tia), GB tạo ra boundary dựa trên vùng kín xung quanh điểm click. Lọc entity ngắn < `short_segment_threshold_mm` (300mm) để loại rác. Phù hợp với phòng có hình dạng phức tạp mà XR không xử lý được.

**Ngưỡng pass prototype:**
- GB: ≥ 2/3 phòng L-shape từ file DXF thực tạo Polyline đúng

In scope:
- File `lisp/gb.lsp`:
  - Hàm `(defun c:GB ())` — lệnh GB
  - Filter entity rác < 300mm (từ config `short_segment_threshold_mm`)
  - Tạo boundary set từ layer tường, gọi `-BOUNDARY`
  - Lấy LWPOLYLINE kết quả, đổi màu đỏ, gắn đúng thuộc tính
  - Thông báo lỗi nếu không tạo được boundary
- Test thủ công 3 phòng L-shape từ file DXF thực

Out of scope:
- Phòng phức tạp hơn L-shape (Phase 2)
- Integration với JSON export (Sprint 3)

Story IDs: US-ROOM-001, US-ROOM-002
Acceptance Criteria IDs: US-ROOM-001 AC-04 (GB), US-ROOM-002 AC-01

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-ROOM-001): Given phòng hình L, When dùng GB, Then LWPOLYLINE bao đúng hình dạng phòng, không bị lẹm tại góc giật cấp
- AC-02: LWPOLYLINE GB có color=1, closed=True
- AC-03 (NGƯỠNG PROTOTYPE): ≥ 2/3 test case phòng L-shape từ DXF thực → Polyline đúng — **hard gate**
- AC-04: Entity ngắn < 300mm bị bỏ qua trong boundary set (không gây vùng kín giả)
- AC-05: Given click bên ngoài vùng kín, Then GB thông báo lỗi "Ranh gioi khong khep kin hoac diem click nam ngoai"

Module boundary: `lisp/gb.lsp` — AutoCAD/AutoLISP layer

Files/Modules dự kiến bị ảnh hưởng:
- `lisp/gb.lsp` (tạo mới)
- `lisp/README.md` (cập nhật hướng dẫn GB)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-001, US-ROOM-002
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 2 — Acceptance ngưỡng prototype
- /docs/02-PRD-Product-Backlog.md#Rủi ro nhận diện phòng

Dependencies: T2-01 (config layer, threshold); T2-03 (có thể tái sử dụng filter logic)

Known risks:
- `-BOUNDARY` lệnh AutoCAD có thể không tạo được LWPOLYLINE nếu vùng không kín hoàn toàn → cần Door Sealing (Sprint 3)
- Phòng L-shape phức tạp (nhiều góc) có thể vượt khả năng GB cơ bản → ghi nhận trong báo cáo prototype

Open ambiguities:
- GB tạo boundary theo tọa độ thực hay dùng selection set? (Cần thống nhất với XR approach)

Definition of Done:
- [ ] `lisp/gb.lsp` load được vào AutoCAD 2019+ không báo lỗi
- [ ] Test thủ công 3 phòng L-shape — ghi kết quả từng case
- [ ] ≥ 2/3 pass — hard gate
- [ ] Kết quả ghi vào `docs/sprint2-prototype-report.md`

---

# TICKET CONTEXT PACK

Ticket: T2-05 — Báo cáo prototype + demo cho PM/BA + quyết định go/no-go
Người phụ trách: Dev-B (demo), PM (quyết định)
Mục tiêu: Tổng hợp kết quả prototype, thực hiện live demo cho PM/BA, có quyết định rõ ràng "Tiếp tục Sprint 3" hoặc "Cần re-estimate" trước khi sprint đóng.

**Bối cảnh quan trọng:**
Đây là **Checkpoint CP-1 (Go/No-go)**. Không có trạng thái "có vẻ ổn". Phải có số liệu cụ thể. Nếu XR < 4/5 hoặc GB < 2/3 → PM triệu tập session khẩn, quyết định (1) extend Sprint 2 hoặc (2) thu hẹp scope.

In scope:
- Viết `docs/sprint2-prototype-report.md`:
  - Bảng kết quả: case ID | loại phòng | thuật toán | pass/fail | nguyên nhân fail (nếu có)
  - Tổng hợp: X/Y pass XR, X/Y pass GB, X/Y phòng có cửa không lẹm
  - Các case fail: mô tả nguyên nhân kỹ thuật cụ thể
  - Kết luận: đạt/không đạt ngưỡng
- Live demo trong meeting: click phòng trong AutoCAD → LWPOLYLINE đỏ xuất hiện
- PM xác nhận: "Tiếp tục Sprint 3" hoặc "Re-estimate"

Out of scope:
- Fix case fail (nếu cần — làm trong sprint mở rộng nếu PM quyết định)
- Bất kỳ code Python nào

Story IDs: US-ROOM-001 (validation), US-ROOM-002 (validation)
Acceptance Criteria IDs: Sprint 2 Exit Criteria

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: `sprint2-prototype-report.md` commit vào repo với đủ bảng kết quả
- AC-02: Demo live được thực hiện trong meeting (PM/BA tham dự)
- AC-03: PM xác nhận quyết định go/no-go bằng văn bản (email hoặc comment)
- AC-04: Nếu go → PM confirm "Tiếp tục Sprint 3" trong issue tracker
- AC-05: Báo cáo ghi rõ case nào fail VÀ nguyên nhân (không chỉ ghi "fail")

Module boundary: Documentation, không có code

Files/Modules dự kiến bị ảnh hưởng:
- `docs/sprint2-prototype-report.md` (tạo mới)

Doc refs:
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 2 — Acceptance ngưỡng prototype
- /docs/05-Ke-Hoach-Sprint-Release.md#Checkpoint với Stakeholder (CP-1)
- /docs/05-Ke-Hoach-Sprint-Release.md#2.2 Vì sao technical spike phải đi trước

Dependencies: T2-03 (kết quả XR), T2-04 (kết quả GB)

Known risks:
- PM/BA không available cho meeting → cần book slot ngay từ đầu sprint
- Kết quả boundary tạo xong nhưng không đúng hình dạng → vẫn là "fail", không được tính là "pass"

Open ambiguities: Không có — ngưỡng đã được định nghĩa rõ

Definition of Done:
- [ ] Báo cáo prototype hoàn chỉnh với số liệu thực
- [ ] Demo đã diễn ra
- [ ] PM đã có quyết định rõ ràng bằng văn bản
- [ ] Sprint 2 được đóng chính thức sau khi PM confirm
