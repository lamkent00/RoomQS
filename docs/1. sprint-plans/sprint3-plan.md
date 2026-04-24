# SPRINT BRIEF

Sprint: Sprint 3 — Room Pipeline LISP→Python + UI Form
Phase: GIAI ĐOẠN 3 — MVP BUILD (Sprint 3–4)
Mục tiêu sprint: Hoàn thiện luồng dữ liệu từ AutoLISP đến Shapely Polygon trong Python; gắn tên/mã phòng; loại trùng lặp; gán cửa vào phòng (spatial cơ bản); template Excel đóng băng; UI form cơ bản validate được.

In-scope:
- BL-12: Door Sealing trước BPOLY trong LISP (Dev-B, 2 ngày)
- BL-13: LISP → JSON: xuất tọa độ Polyline ra file (Dev-B, 1.5 ngày)
- BL-14: Python: JSON → Shapely Polygon (Dev-A, 1.5 ngày)
- BL-15: Python: gắn text phòng vào Polygon (Dev-A, 1.5 ngày)
- BL-16: Python: loại bỏ Polygon trùng lặp (Dev-A, 1 ngày)
- BL-17: Python: spatial assignment cửa → phòng — gán cơ bản (Dev-A, 2 ngày)
- BL-26: Review và xác nhận template Excel — **deadline cứng** (PM/QA, 1 ngày)
- BL-31: PySide6: UI form nhập tham số cơ bản (Dev-A, 2 ngày)

Out-of-scope:
- Cửa ranh giới chung (BR-06, BL-18/24 — Sprint 4)
- Nhập cửa từ Excel fallback (BL-19 — Sprint 4)
- Bất kỳ tính toán khối lượng nào (Sprint 4)
- Excel export (Sprint 5)
- Integration test end-to-end (Sprint 5)
- Format màu sắc, merge cell trong Excel (Sprint 5 BL-30)

Risks:
- Float precision từ LISP tọa độ gây Polygon invalid (`is_valid = False`) → cần Shapely `buffer(0)` hoặc simplify tolerance
- Text phòng đặt sai vị trí (ngoài polygon) → phòng bị gán tên mặc định "Chua_dinh_danh"
- Template Excel không được PM confirm trước cuối sprint → BLOCKER cho Sprint 5 BL-27
- BL-26 phụ thuộc end user availability → PM phải chủ động book trước ngày 5 sprint

Dependencies:
- Sprint 2 exit criteria pass (prototype XR ≥ 4/5, GB ≥ 2/3, PM confirm "tiếp tục")
- DoorBlock từ T2-02 (cần `position` để spatial assignment)
- config.yaml đã có `calculation.geometry_tolerance_mm`

Danh sách ticket:
1. T3-01: BL-12 — Door Sealing trước BPOLY
2. T3-02: BL-13 — LISP → JSON: xuất tọa độ Polyline
3. T3-03: BL-14 + BL-16 — Python JSON → Shapely Polygon + deduplication
4. T3-04: BL-15 — Gắn text phòng (room_name, room_code) vào Polygon
5. T3-05: BL-17 — Spatial assignment cửa → phòng (cơ bản)
6. T3-06: BL-26 — Xác nhận template Excel
7. T3-07: BL-31 — UI form nhập tham số cơ bản (PySide6)

---

# TICKET CONTEXT PACK

Ticket: T3-01 — BL-12 Door Sealing trước BPOLY
Người phụ trách: Dev-B
Mục tiêu: Xử lý vấn đề tường hở tại vị trí cửa (ranh giới phòng không khép kín do cửa cắt tường) bằng cách vẽ Line tạm tại vị trí cửa trước khi gọi BPOLY, sau đó xóa Line tạm sau khi có boundary.

**Bối cảnh kỹ thuật:**
Trong bản vẽ kiến trúc, tường tại vị trí cửa bị cắt đứt. BPOLY không thể tạo vùng kín nếu tường hở. Door Sealing: LISP `ssget` tìm block cửa gần điểm click, tính vị trí 2 đầu mở của tường, vẽ LINE tạm (`ADDTODB`) lấp hở, gọi BPOLY/GB, sau đó `erase` LINE tạm. LINE tạm phải ở layer riêng để dễ xóa.

In scope:
- Cập nhật `lisp/xr.lsp` và `lisp/gb.lsp`: thêm logic Door Sealing trước khi tạo boundary
- Hàm LISP `(defun seal-door-gaps (click-pt wall-layer door-layer))`:
  - Tìm block cửa gần click-pt nhất (trong radius = chiều dày tường × 2)
  - Tính 2 endpoint của khe hở tường
  - Vẽ LINE tạm trên layer `_DOOR_SEAL_TEMP`
  - Sau BPOLY xong: xóa tất cả entity trên layer `_DOOR_SEAL_TEMP`
- Test với file DXF có phòng có 1 cửa và 2 cửa

Out of scope:
- Door Sealing cho trường hợp cửa góc phòng (edge case — Phase 2 nếu cần)
- Export JSON (T3-02)

Story IDs: US-ROOM-002 (boundary không bị lẹm)
Acceptance Criteria IDs: US-ROOM-002 AC-01, AC-02, AC-03

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-ROOM-002): Given phòng có 1 cửa mở vào trong (tường hở tại cửa), When tạo boundary, Then LWPOLYLINE không bị đứt tại vị trí cửa
- AC-02 (US-ROOM-002): Given phòng có 2 cửa đối diện, Then LWPOLYLINE liên tục bao toàn bộ phòng
- AC-03 (US-ROOM-002): Diện tích từ LWPOLYLINE ≤ 2% sai lệch so với đo tay tọa độ tường
- AC-04: LINE tạm bị xóa sạch sau khi BPOLY xong — không còn entity trên layer `_DOOR_SEAL_TEMP`
- AC-05 (EC-04): AutoLISP áp dụng Door Sealing khi có khe hở tường, sau khi lấy boundary thì xóa Line tạm

Module boundary:
- `lisp/xr.lsp` và `lisp/gb.lsp` (cập nhật)
- Hoàn toàn trong AutoCAD/AutoLISP layer

Files/Modules dự kiến bị ảnh hưởng:
- `lisp/xr.lsp` (cập nhật)
- `lisp/gb.lsp` (cập nhật)
- `lisp/door_seal.lsp` (tạo mới — chứa hàm seal-door-gaps, được load bởi xr/gb)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-002
- /docs/03-User-Stories.md#EC-04 (Edge case tường hở tại cửa)
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 3 — BL-12

Dependencies: T2-01 (config layer name); T2-03, T2-04 (xr.lsp/gb.lsp đã có)

Known risks:
- Block cửa không chuẩn → khó tính vị trí khe hở → fallback: ghi warning "Door Sealing failed", vẫn tạo boundary bình thường

Open ambiguities:
- Chiều dày tường thực tế ảnh hưởng đến độ chính xác của Door Sealing — cần biết từ config `default_wall_thickness_mm`

Definition of Done:
- [ ] Door Sealing chạy trong XR và GB
- [ ] LINE tạm bị xóa sau boundary
- [ ] Test thủ công phòng có cửa: boundary không bị đứt
- [ ] Ghi kết quả test vào PR description

---

# TICKET CONTEXT PACK

Ticket: T3-02 — BL-13 LISP → JSON: xuất tọa độ Polyline ra file
Người phụ trách: Dev-B
Mục tiêu: Sau khi XR/GB tạo LWPOLYLINE cho phòng, LISP xuất tọa độ đỉnh của tất cả Polyline vào file `output.json` để Python đọc — đây là điểm tích hợp duy nhất giữa AutoLISP và Python.

**Bối cảnh kỹ thuật:**
LISP không có thư viện JSON native. Dùng cách thủ công: viết file text theo format JSON bằng hàm `(write-line ...)`. Cấu trúc JSON:
```json
{
  "rooms": [
    {
      "lisp_index": 0,
      "vertices": [[x1,y1],[x2,y2],...]
    }
  ]
}
```
Tọa độ là số thực LISP (dùng `(rtos coord 2 6)` để đủ precision). File lưu vào thư mục cùng với DXF hoặc thư mục temp được config.

In scope:
- File `lisp/export_rooms.lsp`:
  - Hàm `(defun c:EXPORTROOMS ())` — sau khi user xong click tất cả phòng, gọi lệnh này để xuất JSON
  - Hoặc auto-export sau mỗi phòng (cần quyết định trong sprint planning)
  - Lặp qua tất cả LWPOLYLINE trên layer `PHONG_BOUNDARY`
  - Ghi file `output.json` vào thư mục cấu hình
- Format JSON đã thống nhất (cần Dev-A và Dev-B agree schema trước khi code)

Out of scope:
- Python parse JSON (T3-03)
- Bất kỳ attribute phòng nào (room_name, door — Python gắn sau)

Story IDs: US-INP-002 (phần LISP → JSON bridge)
Acceptance Criteria IDs: Dẫn xuất từ Sprint 3 Exit Criteria + ADR file-based integration

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: `output.json` được tạo ra sau khi gọi lệnh LISP, không báo lỗi
- AC-02: JSON có đủ các phòng đã click (số phòng trong JSON = số LWPOLYLINE trên layer PHONG_BOUNDARY)
- AC-03: Mỗi phòng có `lisp_index` (int) và `vertices` (list of [x, y] float, đủ precision ≥ 4 decimals)
- AC-04: Tọa độ vertices đã là mm (từ AutoCAD model space, không cần convert thêm nếu $INSUNITS=4)
- AC-05: Dev-A verify file JSON đọc được bằng Python `json.loads()` không lỗi
- AC-06: Nếu chưa có LWPOLYLINE nào trên PHONG_BOUNDARY → thông báo "Chua co phong nao duoc nhan dien"

Module boundary:
- `lisp/export_rooms.lsp` — AutoCAD/AutoLISP layer
- File `output.json` — tại điểm tích hợp LISP/Python

Files/Modules dự kiến bị ảnh hưởng:
- `lisp/export_rooms.lsp` (tạo mới)
- `lisp/README.md` (cập nhật workflow: XR/GB → EXPORTROOMS)
- Schema file: `docs/output-json-schema.md` (tạo mới để Dev-A và Dev-B cùng dùng)

Doc refs:
- /docs/04-Kien-Truc-Tech-Stack.md#2 Kiến trúc tổng thể (file-based integration)
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 3 — BL-13

Dependencies: T2-03 (XR tạo LWPOLYLINE), T2-04 (GB tạo LWPOLYLINE), T3-01 (Door Sealing)

Known risks:
- Float precision trong LISP rts string → cần test round-trip: tọa độ LISP → JSON → Python → Shapely không lỗi

Open ambiguities:
- EXPORTROOMS gọi thủ công hay tự động sau mỗi click? (Thủ công đơn giản hơn cho prototype)

Definition of Done:
- [ ] `export_rooms.lsp` tạo ra file `output.json` đúng schema
- [ ] JSON có thể parse bằng Python `json.loads()` không lỗi
- [ ] Tọa độ tương ứng với geometry trong AutoCAD (kiểm tra bằng cách so sánh 1 điểm)
- [ ] Schema được document

---

# TICKET CONTEXT PACK

Ticket: T3-03 — BL-14 + BL-16 Python: JSON → Shapely Polygon + Deduplication
Người phụ trách: Dev-A
Mục tiêu: Module `room_engine` đọc `output.json` từ LISP, tạo Shapely Polygon hợp lệ cho từng phòng, loại bỏ trùng lặp, và trả về danh sách Room object chuẩn cho pipeline.

**Bối cảnh kỹ thuật:**
- BL-14: `json.load()` → lấy `vertices` → `Shapely Polygon(vertices)`. Validate `polygon.is_valid`. Nếu invalid → thử `polygon.buffer(0)` (repair). Nếu vẫn fail → loại phòng và log warning.
- BL-16: Deduplication: nếu 2 polygon có `intersection.area / min(area1, area2) > 0.9` → trùng lặp, giữ cái đầu tiên, warning cái thứ hai.
- Data model Room: `room_id` (auto), `polygon: Polygon`, `lisp_index: int`.

In scope:
- Module `src/room_engine/room_builder.py`:
  - Hàm `build_rooms_from_json(json_path: str, unit_factor: float) -> list[Room]`
  - Validate và repair polygon
  - Log warning phòng invalid
- Module `src/room_engine/deduplicator.py`:
  - Hàm `deduplicate_rooms(rooms: list[Room], overlap_threshold=0.9) -> list[Room]`
- Data class `Room(room_id: str, polygon: Polygon, lisp_index: int)`
- Unit test với fixture JSON (tạo trực tiếp trong test)

Out of scope:
- Gắn room_name, room_code (T3-04)
- Spatial assignment cửa (T3-05)
- Bất kỳ tính toán khối lượng nào

Story IDs: US-ROOM-001 (FR-05 tạo polygon), US-ROOM-003 (FR-06 deduplication)
Acceptance Criteria IDs: US-ROOM-003 AC-01, AC-02, AC-03; Sprint 3 Exit Criteria

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (Sprint 3 Exit): `polygon.is_valid == True` cho ≥ 90% phòng trong test fixture
- AC-02 (US-ROOM-003): Given 2 polygon gần như identical (click 2 lần cùng phòng), Then giữ 1, log warning với room_id bị loại
- AC-03 (US-ROOM-003): Given 2 phòng kề nhau (share tường chung), Then cả 2 được giữ nguyên
- AC-04: Room invalid (is_valid=False sau buffer(0)) → bị loại, warning ghi vào log
- AC-05 (EC-03): Polygon self-intersecting → thử buffer(0); nếu vẫn fail → loại, cảnh báo

Module boundary:
- `src/room_engine/` — chỉ nhận data structures, không I/O file, không UI
- Phụ thuộc: Shapely (`src/geometry/`), JSON (stdlib)

Files/Modules dự kiến bị ảnh hưởng:
- `src/room_engine/__init__.py`, `src/room_engine/room_builder.py` (tạo mới)
- `src/room_engine/deduplicator.py` (tạo mới)
- `src/room_engine/models.py` — Room dataclass
- `tests/unit/test_room_builder.py` (tạo mới)
- `tests/unit/test_deduplicator.py` (tạo mới)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-001 (BR-01)
- /docs/03-User-Stories.md#US-ROOM-003
- /docs/03-User-Stories.md#EC-01, EC-02, EC-03

Dependencies: T3-02 (schema JSON đã agree), T1-05 (unit_factor từ normalize)

Known risks:
- Shapely `buffer(0)` có thể thay đổi hình dạng polygon → chỉ dùng khi is_valid=False, log khi áp dụng

Open ambiguities:
- overlap_threshold 0.9 hay khác? (Có thể cần điều chỉnh sau test thực tế)

Definition of Done:
- [ ] `build_rooms_from_json()` tạo Room objects hợp lệ
- [ ] `deduplicate_rooms()` loại đúng trùng lặp, giữ đúng phòng kề nhau
- [ ] Unit test cover: polygon hợp lệ, polygon invalid, trùng lặp, phòng kề nhau
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T3-04 — BL-15 Gắn room_name và room_code từ text DXF vào Polygon
Người phụ trách: Dev-A
Mục tiêu: Module `text_extractor` + `room_engine` gắn đúng tên phòng và mã phòng từ TEXT/MTEXT entities vào Room object tương ứng bằng spatial containment (Shapely `contains`).

**Bối cảnh kỹ thuật:**
Với mỗi TextEntity có `position` (x, y), kiểm tra `room.polygon.contains(Point(pos))`. Nếu có → gán vào phòng. Rule BR-07: ưu tiên text có sẵn (không cho phép override bằng code logic). Phân biệt room_name vs room_code: pattern như `P01`, `WC`, `K01` là room_code; text dài hơn là room_name. Nếu không có text → default `"Chua_dinh_danh"` + `"ROOM_{id}"`.

In scope:
- Module `src/room_engine/room_tagger.py`:
  - Hàm `tag_rooms_with_text(rooms: list[Room], texts: list[TextEntity]) -> list[Room]`
  - Spatial lookup: Shapely `polygon.contains(Point(x, y))`
  - Phân biệt room_name vs room_code (regex pattern đơn giản)
  - Default khi không có text
  - Log warning phòng không có text
- Unit test với fixture có text đúng vị trí và text sai vị trí

Out of scope:
- Text nằm trên ranh giới (EC-06) → dùng "gần nhất tính theo tâm" nếu cần; nếu phức tạp → loại, warning

Story IDs: US-ROOM-004
Acceptance Criteria IDs: US-ROOM-004 AC-01, AC-02, AC-03, AC-04; Sprint 3 Exit Criteria

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-ROOM-004): Text "PHONG NGU" bên trong polygon A → `room_name` của A = "PHONG NGU"
- AC-02 (US-ROOM-004): Text "P01" bên trong polygon A → `room_code` của A = "P01"
- AC-03 (US-ROOM-004): Phòng không có text → `room_name = "Chua_dinh_danh"`, cảnh báo ghi log
- AC-04 (US-ROOM-004): Text của phòng A không bị gán nhầm sang phòng B kề nhau
- AC-05 (Sprint 3 Exit): `room_name` và `room_code` gắn đúng trong ≥ 95% trường hợp với fixture
- AC-06 (EC-05): Text ngoài tất cả polygon → bị bỏ qua, không crash

Module boundary:
- `src/room_engine/room_tagger.py`
- Phụ thuộc: `src/text_extractor/` (TextEntity), Shapely
- Không gọi UI, không I/O file

Files/Modules dự kiến bị ảnh hưởng:
- `src/room_engine/room_tagger.py` (tạo mới)
- `tests/unit/test_room_tagger.py` (tạo mới)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-004
- /docs/03-User-Stories.md#EC-05, EC-06, EC-07
- /docs/02-PRD-Product-Backlog.md#FR-07, BR-07

Dependencies: T3-03 (Room objects), T1-04 (TextEntity từ text_extractor)

Known risks:
- Pattern phân biệt room_name vs room_code phụ thuộc convention bản vẽ → cần xem file DXF thực

Open ambiguities:
- Regex pattern cho room_code là gì? (Cần BA xác nhận convention mã phòng khách hàng dùng)

Definition of Done:
- [ ] `tag_rooms_with_text()` gắn đúng room_name và room_code
- [ ] Default khi không có text hoạt động đúng
- [ ] Unit test pass với ≥ 3 scenarios
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T3-05 — BL-17 Spatial assignment cửa → phòng (cơ bản)
Người phụ trách: Dev-A
Mục tiêu: Module `door_engine` gán mỗi DoorBlock vào phòng tương ứng bằng spatial containment — đủ để pipeline chạy end-to-end; cửa ranh giới chung (2 phòng) xử lý ở Sprint 4.

**Bối cảnh kỹ thuật:**
Dùng Shapely: với mỗi DoorBlock, `Point(position)`. Kiểm tra `polygon.contains(Point)` cho từng phòng. Nếu không contain → dùng buffer 50mm để tìm phòng gần nhất. Gán `related_room_a`. Cửa trên ranh giới chung (cả 2 phòng đều trong buffer) → để `is_shared_boundary = True` nhưng chưa xử lý BR-06 (Sprint 4).

In scope:
- Module `src/door_engine/door_mapper.py`:
  - Hàm `assign_doors_to_rooms(doors: list[DoorBlock], rooms: list[Room]) -> list[Door]`
  - Cơ chế: contains → buffer 50mm → unassigned
  - Gán `related_room_a`, flag `is_shared_boundary`
  - Warning cửa unassigned
- Data class `Door` (extend DoorBlock): thêm `related_room_a`, `related_room_b`, `is_shared_boundary`

Out of scope:
- Xử lý BR-06 (cửa ranh giới chung — Sprint 4 BL-24)
- Nhập cửa từ Excel fallback (Sprint 4 BL-19)
- Kiểm tra buffer = chiều dày tường (EC-12 — chỉ cần buffer 50mm cố định ở sprint này)

Story IDs: US-DOOR-002, US-DOOR-003 (phần detect, chưa xử lý BR-06)
Acceptance Criteria IDs: US-DOOR-002 AC-01, AC-02, AC-03; Sprint 3 Exit Criteria

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-DOOR-002): Given block D1 insertion point rõ ràng bên trong polygon phòng ngủ, Then `related_room_a` của D1 = room_id phòng ngủ
- AC-02 (US-DOOR-002): Given cửa không nằm trong phòng nào, Then cảnh báo "unassigned", không crash
- AC-03 (Sprint 3 Exit): Pipeline chạy được (không yêu cầu 100% cửa gán đúng — chỉ cần pipeline không crash)
- AC-04 (EC-11): Cửa insertion point trên biên chung → `is_shared_boundary = True` được gán
- AC-05: Tổng cửa gán được + unassigned = tổng cửa nhận diện

Module boundary:
- `src/door_engine/door_mapper.py`
- Phụ thuộc: Shapely, Room objects, DoorBlock objects

Files/Modules dự kiến bị ảnh hưởng:
- `src/door_engine/door_mapper.py` (tạo mới)
- `src/door_engine/models.py` — Door class (extend DoorBlock)
- `tests/unit/test_door_mapper.py` (tạo mới)

Doc refs:
- /docs/03-User-Stories.md#US-DOOR-002
- /docs/03-User-Stories.md#EC-11, EC-12, EC-13
- /docs/02-PRD-Product-Backlog.md#FR-10, FR-11, BR-03

Dependencies: T3-03 (Room objects), T2-02 (DoorBlock)

Known risks: Cửa nằm đúng giữa 2 polygon → có thể bị double-assign nếu cả 2 contain → cần xử lý priority

Open ambiguities:
- Buffer 50mm hay dùng `default_wall_thickness_mm` từ config? (Cần quyết định)

Definition of Done:
- [ ] `assign_doors_to_rooms()` gán đúng cửa 1 phòng
- [ ] `is_shared_boundary` flag được gán cho cửa trên ranh giới
- [ ] Cửa unassigned có warning
- [ ] Unit test pass
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T3-06 — BL-26 Xác nhận template Excel với end user (deadline cứng)
Người phụ trách: PM / QA
Mục tiêu: Template Excel được PM và ít nhất 1 end user xác nhận format chính thức, để format đóng băng sau sprint này và Sprint 5 có thể export đúng template mà không cần rework.

**Cảnh báo quan trọng:** Đây là **hard gate của Sprint 3**. Nếu không có xác nhận trước cuối sprint → Sprint 5 BL-27/28/29 bị block hoặc phải rework. PM phải book meeting với end user trong tuần đầu Sprint 3.

In scope:
- Gửi draft template (từ T0-02) cho end user review lần cuối
- Cập nhật template theo feedback (nếu có) — chỉ thay đổi cột, không thêm sheet
- Lấy xác nhận bằng văn bản (email / comment)
- Document final column list vào `docs/excel-template-final.md`
- Đóng băng format: ghi nhận "Template v1.0 — frozen, không thay đổi sau ngày X"

Out of scope:
- Format màu sắc, merge cell (Sprint 5 BL-30)
- Thêm sheet thứ 4 hoặc báo cáo tổng hợp (out of scope MVP)
- Công thức Excel

Story IDs: US-EXP-001, US-EXP-002, US-EXP-003
Acceptance Criteria IDs: Sprint 3 Exit Criteria (hard gate)

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (Sprint 3 Exit — hard gate): End user xác nhận qua email/comment trong issue tracker
- AC-02: Template final có đủ 3 sheet với tên và cột đã thống nhất
- AC-03: `docs/excel-template-final.md` ghi rõ từng sheet: tên cột, kiểu dữ liệu, đơn vị
- AC-04: PM ghi nhận "Template v1.0 frozen" trong Slack/issue — mọi thay đổi sau đây phải qua approval process

Module boundary: Documentation — không có code

Files/Modules dự kiến bị ảnh hưởng:
- `docs/excel-template-final.md` (tạo/cập nhật)
- `samples/template-excel/template_v1.xlsx` (version final)

Doc refs:
- /docs/02-PRD-Product-Backlog.md#FR-18, FR-19, FR-20, FR-21
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 3 — BL-26 (deadline cứng)

Dependencies: T0-02 (draft từ Sprint 0)

Known risks:
- End user không available → PM escalate ngay tuần 1 Sprint 3
- End user muốn thêm sheet/cột nhiều → PM negotiate, giữ scope MVP

Open ambiguities: Không có nếu T0-02 đã done

Definition of Done:
- [ ] Email/comment xác nhận từ end user
- [ ] `docs/excel-template-final.md` commit
- [ ] PM announce "frozen" cho team

---

# TICKET CONTEXT PACK

Ticket: T3-07 — BL-31 PySide6 UI form nhập tham số cơ bản
Người phụ trách: Dev-A
Mục tiêu: Giao diện PySide6 cho phép user nhập các tham số cần thiết (file DXF, chiều cao thông thủy H, chiều dày tường t, file cửa Excel optional) và validate trước khi chạy pipeline.

**Bối cảnh kỹ thuật:**
Theo A6: H và t do user nhập (không đọc tự động từ bản vẽ). UI form cơ bản: QLineEdit cho H và t (validate float > 0), QPushButton chọn file DXF (file picker), QPushButton chọn file Excel cửa (optional). Nút "Chạy" chỉ enabled khi field bắt buộc đã điền hợp lệ. Không có logic nghiệp vụ trong UI — chỉ nhận input và pass xuống pipeline.

In scope:
- Cập nhật `src/ui/main_window.py`:
  - QLineEdit: `floor_height_mm` (H, bắt buộc, float > 0)
  - QLineEdit: `wall_thickness_mm` (t, bắt buộc, float > 0)
  - QPushButton + QLabel: chọn file DXF (bắt buộc)
  - QPushButton + QLabel: chọn file Excel cửa (optional)
  - QPushButton "Chạy": disabled khi field bắt buộc chưa hợp lệ
  - Hiển thị thông báo validation rõ ràng khi thiếu field
- Không kết nối pipeline thực (chỉ cần form validate — integration ở Sprint 5)

Out of scope:
- Progress bar (Sprint 5 BL-32)
- Hiển thị cảnh báo dữ liệu (Sprint 5 BL-33)
- Preview kết quả (Sprint 5 BL-35)
- Nút xuất Excel (Sprint 5 BL-34)

Story IDs: US-INP-001 (UI side), US-INP-003 (chọn file Excel cửa)
Acceptance Criteria IDs: US-INP-001 AC-05; Sprint 3 Exit Criteria

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (Sprint 3 Exit): UI form hiển thị, validate field bắt buộc, không cho chạy khi field trống
- AC-02: Field H nhận giá trị float > 0; nếu nhập string hoặc ≤ 0 → thông báo lỗi inline
- AC-03: Field t nhận giá trị float > 0; validation tương tự H
- AC-04: File picker DXF mở đúng dialog .dxf filter
- AC-05 (US-INP-001): Sau khi chọn file DXF hợp lệ, nút "Tiếp tục" / "Chạy" được kích hoạt
- AC-06: File picker Excel cửa optional — nếu không chọn thì không block "Chạy"

Module boundary:
- `src/ui/main_window.py` — Presentation Layer
- Không gọi pipeline, không chứa business logic
- Chỉ pass input params sang Application Layer (callback/signal)

Files/Modules dự kiến bị ảnh hưởng:
- `src/ui/main_window.py` (cập nhật từ prototype T1-02)
- `tests/unit/test_main_window.py` (tạo mới — test validation logic)

Doc refs:
- /docs/03-User-Stories.md#US-INP-001
- /docs/02-PRD-Product-Backlog.md#FR-22 (UI xử lý 1 lần chạy)
- /docs/04-Kien-Truc-Tech-Stack.md#Presentation Layer

Dependencies: T1-02 (PySide6 window cơ bản đã có)

Known risks:
- PySide6 validation có thể phức tạp với QLineEdit → dùng QDoubleValidator làm đơn giản

Open ambiguities:
- H và t default value trong form: lấy từ config.yaml hay để trống? (Gợi ý: pre-fill từ config)

Definition of Done:
- [ ] Form hiển thị đúng với tất cả field
- [ ] Validation hoạt động: không cho chạy khi field bắt buộc sai
- [ ] File picker hoạt động
- [ ] Unit test validation logic pass
- [ ] .exe rebuild pass với UI mới (verify không có DLL conflict mới)
