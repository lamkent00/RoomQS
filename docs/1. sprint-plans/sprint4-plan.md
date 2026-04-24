# SPRINT BRIEF

Sprint: Sprint 4 — Door Assignment + Calculation Engine + UAT Prep
Phase: GIAI ĐOẠN 3 — MVP BUILD (Sprint 3–4)
Mục tiêu sprint: Hoàn thiện gán cửa ranh giới chung (BR-06); toàn bộ tính toán khối lượng; 100% unit test business rule BR-04/05/06 pass. Đây là **Core Engine Complete milestone (M4)** — sau sprint này, mọi số liệu tính toán phải chính xác.

In-scope:
- BL-18: Python: phát hiện cửa trên ranh giới chung (Dev-A, 2 ngày)
- BL-19: Python: nhập cửa từ Excel đầu vào (fallback) (Dev-A, 1.5 ngày)
- BL-20: Python: tính diện tích, chu vi (Shapely .area, .length) (Dev-A, 1 ngày)
- BL-21: Python: chiều dài từng cạnh (edge list) (Dev-A, 1 ngày)
- BL-22: Python: tính khối lượng sàn (BR-04) (Dev-A, 0.5 ngày)
- BL-23: Python: tính khối lượng tường (trừ cửa đơn, BR-05) (Dev-A, 1.5 ngày)
- BL-24: Python: xử lý cửa ranh giới chung (BR-06) (Dev-A, 2 ngày)
- BL-25: pytest: unit test BR-04/05/06 (QA/Dev, 2 ngày) — **viết SONG SONG với implementation**
- BL-36: UAT preparation: test cases từ SRS Section 15 (QA, 2 ngày)

Out-of-scope:
- Excel export (Sprint 5)
- UI integration (Sprint 5)
- Integration test end-to-end (Sprint 5)
- Phòng có chiều cao tường khác nhau theo phòng (Phase 2)
- Bất kỳ thay đổi template Excel (đã frozen ở Sprint 3)

Risks:
- BR-06 bị hiểu sai (trừ chia đôi thay vì trừ từng phòng) → PHẢI có test case BR-06 với số liệu cụ thể được viết TRƯỚC khi code BL-24
- Polygon từ Sprint 3 có float precision issue → cần tolerance khi tính diện tích (Shapely xử lý tốt nhưng cần verify)
- Cửa ranh giới chung phức tạp hơn dự kiến → buffer 2 ngày BL-18+BL-24

Dependencies:
- Sprint 3 exit criteria pass (Polygon hợp lệ ≥ 90%, room_name gắn đúng, template Excel frozen)
- Spatial assignment cơ bản từ T3-05 (is_shared_boundary flag)
- BA/PM phải viết test case BR-06 với số liệu cụ thể trước khi code BL-24

Danh sách ticket:
1. T4-01: BL-18 — Phát hiện cửa trên ranh giới chung (shared boundary detection)
2. T4-02: BL-19 — Nhập cửa từ Excel fallback
3. T4-03: BL-20 + BL-21 — Tính diện tích, chu vi, chiều dài cạnh
4. T4-04: BL-22 + BL-23 — Tính khối lượng sàn (BR-04) + tường cơ bản (BR-05)
5. T4-05: BL-24 — Xử lý cửa ranh giới chung trong tính toán (BR-06)
6. T4-06: BL-25 — pytest unit test BR-04/05/06 (viết song song)
7. T4-07: BL-36 — UAT preparation: checklist 13 tiêu chí SRS Section 15

---

# TICKET CONTEXT PACK

Ticket: T4-01 — BL-18 Phát hiện cửa trên ranh giới chung (shared boundary detection)
Người phụ trách: Dev-A
Mục tiêu: Nâng cấp door_mapper để phát hiện chính xác cửa nằm trên tường chung giữa 2 phòng bằng Shapely intersection — gán đúng `related_room_a` và `related_room_b`, set `is_shared_boundary = True`.

**Bối cảnh kỹ thuật:**
Sprint 3 đã set `is_shared_boundary` nhưng chưa xác định chính xác 2 phòng. Bây giờ: dùng `polygon_a.boundary.intersection(polygon_b.boundary)` để lấy đoạn tường chung. Nếu `insertion_point.distance(shared_segment) < wall_thickness + tolerance` → cửa nằm trên tường chung. Gán cả 2 phòng. Rule EC-12: buffer = chiều dày tường. Rule EC-13: nếu 1 phòng ngoài phạm vi xử lý → chỉ trừ phòng trong phạm vi.

In scope:
- Cập nhật `src/door_engine/door_mapper.py`:
  - Hàm mới: `detect_shared_boundary_doors(doors, rooms, wall_thickness_mm, tolerance_mm) -> list[Door]`
  - Tính shared_segment giữa mọi cặp phòng kề nhau
  - Check distance từ door insertion_point đến shared_segment
  - Gán related_room_b nếu is_shared_boundary
- Unit test: 3 scenarios (cửa 1 phòng, cửa 2 phòng, cửa gần nhưng không shared)

Out of scope:
- Tính toán khối lượng BR-06 (T4-05)
- Trường hợp ≥ 3 phòng có chung đỉnh (edge case — Phase 2)

Story IDs: US-DOOR-003
Acceptance Criteria IDs: US-DOOR-003 AC-01, AC-02, AC-03

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-DOOR-003): Given cửa D2 trên tường chung giữa "Phong ngu" và "Phong khach", Then `related_room_a` = phòng ngủ, `related_room_b` = phòng khách, `is_shared_boundary = True`
- AC-02 (US-DOOR-003): Given cửa D1 chỉ thuộc 1 phòng, Then `related_room_b = None`, `is_shared_boundary = False`
- AC-03 (EC-12): Buffer = chiều dày tường (`wall_thickness_mm` từ config)
- AC-04 (EC-13): Nếu `related_room_b` nằm ngoài phạm vi → `related_room_b = None`, flag `room_b_out_of_scope = True`
- AC-05: Tất cả cửa đã detect từ Sprint 3 giữ nguyên `related_room_a`; chỉ update `related_room_b`

Module boundary:
- `src/door_engine/door_mapper.py` (cập nhật)
- Phụ thuộc: Shapely, Room objects, config `wall_thickness_mm`, `geometry_tolerance_mm`

Files/Modules dự kiến bị ảnh hưởng:
- `src/door_engine/door_mapper.py`
- `tests/unit/test_door_mapper.py` (cập nhật thêm test cases)

Doc refs:
- /docs/03-User-Stories.md#US-DOOR-003
- /docs/03-User-Stories.md#EC-11, EC-12, EC-13
- /docs/02-PRD-Product-Backlog.md#BR-03, BR-06

Dependencies: T3-05 (is_shared_boundary flag đã có), T2-01 (wall_thickness từ config)

Known risks:
- `boundary.intersection()` có thể trả về điểm thay vì đoạn thẳng (khi 2 polygon chỉ share 1 vertex) → phải check type result

Open ambiguities:
- Nếu cửa gần nhiều shared segment của nhiều cặp phòng → gán phòng nào? (Gợi ý: gần nhất)

Definition of Done:
- [ ] `detect_shared_boundary_doors()` hoạt động với ≥ 2 phòng kề nhau
- [ ] Unit test pass 3 scenarios
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T4-02 — BL-19 Nhập cửa từ Excel đầu vào (fallback)
Người phụ trách: Dev-A
Mục tiêu: Module đọc file Excel chứa danh sách cửa (mã, tên, rộng mm, cao mm) làm fallback khi block cửa trên bản vẽ thiếu attribute, hoặc user muốn override kích thước.

**Bối cảnh kỹ thuật:**
Đọc bằng `pandas.read_excel()`. Column required: `ma_cua`, `rong_mm`, `cao_mm`. Optional: `ten_cua`. Merge với DoorBlock từ bản vẽ theo `door_code` (key). Nếu cùng mã có trong cả Excel và block attribute → Excel ưu tiên (override). Nếu mã cửa trong Excel không có trong bản vẽ → log warning.

In scope:
- Module `src/door_engine/door_excel_reader.py`:
  - Hàm `load_doors_from_excel(path: str) -> dict[str, DoorSpec]`
  - DoorSpec: `{door_code, door_name, width_mm, height_mm}`
  - Validate cột bắt buộc; cảnh báo cửa width=0/null
- Hàm merge: `enrich_doors_with_excel(doors: list[DoorBlock], specs: dict) -> list[DoorBlock]`
- Unit test với fixture Excel

Out of scope:
- Sheet thứ 2 hoặc multi-sheet Excel cửa (chỉ đọc sheet đầu tiên)
- Tự động match block name vs mã cửa khi naming convention khác (Phase 2)

Story IDs: US-INP-003
Acceptance Criteria IDs: US-INP-003 AC-01 đến AC-05

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-INP-003): Given file Excel 5 loại cửa D1–D3, DW, S1, When load, Then 5 record đúng ma_cua, rong_mm, cao_mm
- AC-02 (US-INP-003): Given cửa width=0, Then đánh dấu invalid, cảnh báo
- AC-03 (US-INP-003): Given cửa trong Excel không có trong bản vẽ, Then warning log, không crash
- AC-04 (US-INP-003): Given thiếu cột `rong_mm`, Then lỗi rõ: "Thieu cot bat buoc: rong_mm"
- AC-05 (EC-15): Given mã cửa D1 xuất hiện 2 lần trong Excel, Then dùng record đầu, warning "Ma cua D1 bi trung, dung dong 1"

Module boundary:
- `src/door_engine/door_excel_reader.py`
- Phụ thuộc: pandas, openpyxl, không gọi Shapely

Files/Modules dự kiến bị ảnh hưởng:
- `src/door_engine/door_excel_reader.py` (tạo mới)
- `tests/unit/test_door_excel_reader.py` (tạo mới)
- `tests/fixtures/doors_sample.xlsx` (tạo mới)

Doc refs:
- /docs/03-User-Stories.md#US-INP-003
- /docs/03-User-Stories.md#EC-08, EC-09, EC-10, EC-15
- /docs/02-PRD-Product-Backlog.md#FR-03, FR-09, BR-02

Dependencies: T2-02 (DoorBlock model), T3-06 (template Excel format đã frozen)

Known risks:
- User upload Excel sai cột → cần message rõ để user tự sửa được

Open ambiguities: Không có — spec rõ

Definition of Done:
- [ ] `load_doors_from_excel()` đọc đúng 5 cột required/optional
- [ ] `enrich_doors_with_excel()` merge đúng theo door_code
- [ ] Unit test pass EC-08, EC-09, EC-15
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T4-03 — BL-20 + BL-21 Tính diện tích, chu vi, chiều dài cạnh
Người phụ trách: Dev-A
Mục tiêu: Module `calc_engine` tính đúng diện tích (m²), chu vi (m), và danh sách cạnh (edge list) cho từng Room object từ Shapely Polygon.

**Bối cảnh kỹ thuật:**
- BL-20: `area = polygon.area / 1_000_000` (mm² → m²); `perimeter = polygon.length / 1_000` (mm → m). Làm tròn 2 chữ số theo config `decimal_places`.
- BL-21: Lấy `polygon.exterior.coords` → cặp điểm liên tiếp → `distance / 1000` (m). Bỏ cạnh length=0. Sort theo thứ tự vertex từ LISP (deterministic).
- Golden dataset: 5 phòng với diện tích tính tay chuẩn → sai lệch < 1%.

In scope:
- Module `src/calc_engine/geometry_calc.py`:
  - Hàm `calc_area_perimeter(room: Room) -> Room` (mutate hoặc return updated)
  - Hàm `calc_edges(room: Room) -> list[Edge]`
- Data class `Edge(room_id, edge_index, length_m)`
- Unit test với golden dataset

Out of scope:
- Tính khối lượng sàn/tường (T4-04/T4-05)
- Xuất Excel (Sprint 5)

Story IDs: US-CALC-001, US-CALC-002
Acceptance Criteria IDs: US-CALC-001 AC-01, AC-02, AC-03; US-CALC-002 AC-01, AC-02, AC-03

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-CALC-001): Given phòng HCN 5000mm×4000mm, Then `area = 20.00 m²`, `perimeter = 18.00 m`
- AC-02 (US-CALC-001): Given phòng L-shape, Then kết quả Shapely ±0.01m² / ±0.01m so với tính tay
- AC-03 (US-CALC-001 / NFR-04): Cùng đầu vào chạy 2 lần → kết quả giống nhau hoàn toàn
- AC-04 (Sprint 4 Exit): Sai lệch diện tích < 1% so với golden dataset
- AC-05 (US-CALC-002): Phòng HCN → 4 cạnh trong edge_list, sum = perimeter ± 0.01m
- AC-06 (US-CALC-002): Không có cạnh length=0 trong output
- AC-07: `edge_index` bắt đầu từ 1, tăng dần liên tiếp

Module boundary:
- `src/calc_engine/geometry_calc.py`
- Phụ thuộc: Shapely, Room, Edge models
- Không gọi UI, không I/O

Files/Modules dự kiến bị ảnh hưởng:
- `src/calc_engine/__init__.py`, `src/calc_engine/geometry_calc.py` (tạo mới)
- `src/calc_engine/models.py` — Edge dataclass
- `tests/unit/test_geometry_calc.py` (tạo mới)
- `tests/fixtures/golden_dataset.json` (5 phòng với expected values)

Doc refs:
- /docs/03-User-Stories.md#US-CALC-001, US-CALC-002
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-05 (determinism)

Dependencies: T3-03 (Room objects với valid Polygon), T1-05 (unit factor — mm invariant)

Known risks: Không có — Shapely .area và .length đã tested và reliable

Open ambiguities: Không có

Definition of Done:
- [ ] `calc_area_perimeter()` và `calc_edges()` hoạt động đúng
- [ ] Unit test pass với golden dataset (< 1% sai lệch)
- [ ] NFR-04 verified: 2 lần chạy cùng output
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T4-04 — BL-22 + BL-23 Tính khối lượng sàn (BR-04) + tường cơ bản (BR-05)
Người phụ trách: Dev-A
Mục tiêu: Module `calc_engine` tính khối lượng hoàn thiện sàn (= diện tích, BR-04) và tường cơ bản (perimeter × H − cửa đơn, BR-05) cho từng phòng.

**Bối cảnh nghiệp vụ quan trọng:**
- **BR-04:** `floor_finish_quantity = area` (m²). Không có hệ số nhân mặc định.
- **BR-05:** `wall_finish_quantity = perimeter × H − Σ(door_area)` với cửa không shared_boundary. Cửa shared_boundary → xử lý riêng ở T4-05.
- **H** = `applied_height` (m) từ user input (UI). **KHÔNG hard-code.**
- Cửa invalid (width=0 hoặc null) → không trừ, log warning cụ thể tên cửa.

**Test case cụ thể BA/PM phải cung cấp trước khi code:**
- P1: perimeter=18m, H=2.8m, cửa D1 (0.9×2.1m, S=1.89m²) → wall_finish = 18×2.8 - 1.89 = 48.51 m²
- P2: perimeter=12m, H=2.8m, không cửa → wall_finish = 33.6 m²

In scope:
- `src/calc_engine/quantity_calc.py`:
  - Hàm `calc_floor_finish(room: Room) -> Room` — `floor_finish_quantity = room.area`
  - Hàm `calc_wall_finish_basic(room: Room, applied_height: float, doors: list[Door]) -> Room`
    - Tính gross = perimeter × H
    - Trừ door_area cho cửa `related_room_a == room.room_id` và `is_shared_boundary = False`
- Unit test với golden dataset

Out of scope:
- BR-06 cửa shared_boundary (T4-05 — đây là điểm phức tạp nhất)

Story IDs: US-CALC-003, US-CALC-004, US-CALC-005
Acceptance Criteria IDs: US-CALC-003 AC-01, AC-05; US-CALC-004 AC-01, AC-02; US-CALC-005

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-CALC-004): Given area=20.00m², Then floor_finish_quantity=20.00m²
- AC-02 (US-CALC-003): Given P1 perimeter=18m, H=2.8m, cửa D1 S=1.89m², Then wall_finish=48.51m²
- AC-03 (US-CALC-003): Given phòng không có cửa (perimeter=12m, H=2.8m), Then wall_finish=33.6m²
- AC-04 (US-CALC-003): Given cửa invalid (width=0), Then wall_finish không trừ cửa đó, warning log
- AC-05 (US-CALC-003): Given H chưa nhập, Then không tính, cảnh báo trước khi xuất

Module boundary:
- `src/calc_engine/quantity_calc.py`
- Không gọi UI, không I/O, không Shapely trực tiếp (chỉ dùng room.area, room.perimeter đã có)

Files/Modules dự kiến bị ảnh hưởng:
- `src/calc_engine/quantity_calc.py` (tạo mới)
- `tests/unit/test_quantity_calc.py` (tạo mới)

Doc refs:
- /docs/03-User-Stories.md#US-CALC-003, US-CALC-004, US-CALC-005
- /docs/02-PRD-Product-Backlog.md#BR-04, BR-05

Dependencies: T4-03 (area, perimeter), T4-01 (door is_shared_boundary)

Known risks:
- Cộng dồn float precision lỗi nhỏ → dùng `round(x, decimal_places)` từ config

Open ambiguities:
- H nhập bằng m hay mm? (Tài liệu nói "chiều cao thông thủy" — thường m; phải document rõ trong code)

Definition of Done:
- [ ] `calc_floor_finish()` và `calc_wall_finish_basic()` đúng với golden dataset
- [ ] Cửa invalid không làm crash, có warning
- [ ] Unit test pass
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T4-05 — BL-24 Xử lý cửa ranh giới chung trong tính toán (BR-06)
Người phụ trách: Dev-A
Mục tiêu: Implement đúng BR-06 — cửa trên ranh giới chung được trừ đầy đủ cho **cả 2 phòng** (không chia đôi), với test case cụ thể được viết trước khi code.

**Nghiệp vụ BR-06 — đây là rule phức tạp nhất:**
> Khi cửa nằm trên tường chung giữa phòng A và phòng B:
> - Phòng A trừ `door_area` một lần (đầy đủ)
> - Phòng B trừ `door_area` một lần (đầy đủ)
> **KHÔNG** chia đôi `door_area` giữa 2 phòng.

**Test case bắt buộc trước khi code (BA/PM phải confirm):**
- Phòng A: perimeter=18m, H=2.8m, cửa D2 (0.9×2.1m = 1.89m²) trên tường chung với B
  → `wall_finish_A = 18×2.8 - 1.89 = 48.51 m²`
- Phòng B: perimeter=16m, H=2.8m, cùng cửa D2 trên tường chung
  → `wall_finish_B = 16×2.8 - 1.89 = 42.91 m²`
- **Tổng trừ toàn hệ thống cho D2 = 2 × 1.89 = 3.78 m²** (không phải 1.89/2)

In scope:
- Cập nhật `src/calc_engine/quantity_calc.py`:
  - Hàm `calc_wall_finish_with_shared_doors(room, applied_height, doors) -> Room`
  - Xử lý cửa `is_shared_boundary = True`:
    - Nếu `room.room_id == door.related_room_a` OR `room.room_id == door.related_room_b` → trừ full door_area
  - Trường hợp EC-13: `room_b_out_of_scope = True` → phòng trong phạm vi vẫn trừ đủ; phòng ngoài không tính
- Unit test ≥ 3 case BR-06 với số liệu cụ thể

Out of scope:
- Cửa nằm giữa 3+ phòng (edge case không có trong MVP scope)

Story IDs: US-DOOR-003, US-CALC-003
Acceptance Criteria IDs: US-CALC-003 AC-02, AC-03; Sprint 4 Exit Criteria (hard gate)

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (US-CALC-003 / BR-06): Given P1 và P2 kề nhau, cửa D2 shared_boundary (S=1.89m²): P1 trừ 1.89m², P2 trừ 1.89m² – **không chia đôi** — hard gate
- AC-02 (US-CALC-003): Given cửa chỉ thuộc 1 phòng: chỉ phòng đó trừ, phòng kia không bị ảnh hưởng
- AC-03 (EC-13): Given related_room_b ngoài phạm vi: phòng trong phạm vi vẫn trừ đủ door_area
- AC-04 (Sprint 4 Exit — hard gate): ≥ 2 pytest test case BR-06 với số liệu trên phải pass
- AC-05 (Sprint 4 Exit — hard gate): 100% unit test BR-04/05/06 pass

Module boundary:
- `src/calc_engine/quantity_calc.py` (cập nhật)
- Không gọi UI, không Shapely

Files/Modules dự kiến bị ảnh hưởng:
- `src/calc_engine/quantity_calc.py`
- `tests/unit/test_quantity_calc.py` (thêm test cases BR-06)

Doc refs:
- /docs/03-User-Stories.md#US-CALC-003 (Business rules BR-05, BR-06)
- /docs/02-PRD-Product-Backlog.md#BR-06
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 4 — Lưu ý đặc biệt BR-06

Dependencies: T4-01 (is_shared_boundary + related_room_b), T4-04 (wall_finish_basic logic)

Known risks:
- BA/PM chưa xác nhận test case với số liệu → DEV KHÔNG ĐƯỢC CODE T4-05 cho đến khi có test case confirm
- Rule bị hiểu nhầm "chia đôi" → test case phải explicit và được review trước khi merge

Open ambiguities:
- Nếu cửa shared boundary nhưng 1 trong 2 phòng bị loại (invalid polygon) → phòng còn lại có trừ không? (Gợi ý: có, vì phòng đó vẫn có tường)

Definition of Done:
- [ ] BA/PM đã cung cấp và xác nhận test case với số liệu cụ thể trước khi code
- [ ] Test case viết trước khi merge implementation
- [ ] ≥ 2 pytest test case BR-06 pass
- [ ] 100% test BR-04/05/06 pass — hard gate
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T4-06 — BL-25 pytest unit test BR-04/05/06 (viết song song với implementation)
Người phụ trách: QA / Dev (phân công rõ)
Mục tiêu: Đảm bảo toàn bộ business rule tính toán được cover bởi pytest tự động — không merge code tính toán nếu test chưa pass.

**Quy tắc quan trọng:** Test phải được commit TRƯỚC hoặc CÙNG LÚC với implementation. Không được để test ở sau khi code đã merge.

In scope:
- Test file: `tests/unit/test_business_rules.py`
- **BR-04 tests:**
  - `test_floor_finish_equals_area()`: area=20.00 → floor_finish=20.00
  - `test_floor_finish_zero_area_warning()`: area=0 → warning, no crash
- **BR-05 tests:**
  - `test_wall_finish_no_doors()`: perimeter=12, H=2.8 → 33.6
  - `test_wall_finish_one_door()`: perimeter=18, H=2.8, D1=1.89 → 48.51
  - `test_wall_finish_invalid_door_skipped()`: cửa invalid không trừ
- **BR-06 tests:**
  - `test_shared_door_deducted_from_both_rooms()`: P1 và P2, D2=1.89 → cả 2 trừ 1.89, không chia đôi
  - `test_shared_door_room_b_out_of_scope()`: only room_a trừ; EC-13
  - `test_non_shared_door_not_deducted_from_neighbor()`: cửa 1 phòng không ảnh hưởng phòng kề

Out of scope:
- Integration test (Sprint 5)
- Test với file DXF thực (UAT Sprint 6)

Story IDs: US-CALC-003, US-CALC-004; BR-04/05/06
Acceptance Criteria IDs: Sprint 4 Exit Criteria — hard gate

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (Sprint 4 Exit — hard gate): 100% pytest BR-04/05/06 pass khi chạy `pytest tests/unit/test_business_rules.py`
- AC-02: ≥ 8 test functions (2 BR-04 + 3 BR-05 + 3 BR-06 minimum)
- AC-03: Test độc lập — không cần file DXF, không cần AutoCAD (pure Python data structures)
- AC-04: CI pass với 0 test failure, 0 error
- AC-05: Coverage report: `src/calc_engine/quantity_calc.py` ≥ 90% coverage

Module boundary:
- `tests/unit/test_business_rules.py`
- Test chỉ import từ `src/calc_engine/`
- Dùng mock/fixture Room, Door objects — không I/O

Files/Modules dự kiến bị ảnh hưởng:
- `tests/unit/test_business_rules.py` (tạo mới)
- `tests/conftest.py` (thêm fixture Room, Door, Edge)

Doc refs:
- /docs/02-PRD-Product-Backlog.md#BR-04, BR-05, BR-06
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 4 — Lưu ý đặc biệt BR-06

Dependencies: T4-04 (interface hàm), T4-05 (interface hàm BR-06)

Known risks:
- QA không familiar với pytest fixture → cần Dev hỗ trợ setup conftest

Open ambiguities: Không có nếu BA đã confirm test case BR-06

Definition of Done:
- [ ] `test_business_rules.py` có ≥ 8 test functions
- [ ] 100% pass khi chạy `pytest tests/unit/test_business_rules.py -v`
- [ ] CI pass
- [ ] Coverage ≥ 90% trên calc_engine

---

# TICKET CONTEXT PACK

Ticket: T4-07 — BL-36 UAT preparation: checklist 13 tiêu chí SRS Section 15
Người phụ trách: QA
Mục tiêu: Chuẩn bị đầy đủ UAT checklist 13 tiêu chí từ SRS Section 15, có cột pass/fail sẵn sàng, để Sprint 6 có thể thực hiện UAT ngay mà không cần chuẩn bị thêm.

In scope:
- Tạo file `docs/uat-checklist.xlsx` hoặc `uat-checklist.md`:
  - 13 tiêu chí từ SRS Section 15 (hoặc MVP Acceptance Criteria nếu SRS Section 15 không có trong tài liệu đã cung cấp)
  - Mỗi tiêu chí: ID, mô tả, cách kiểm tra, expected result, pass/fail, ghi chú
  - Cột: người thực hiện, ngày test, kết quả
- Map 13 tiêu chí đến Story IDs/FR/BR tương ứng
- Chuẩn bị ít nhất 2 file DXF test cho UAT (yêu cầu: ≥ 5 phòng, ≥ 3 cửa)
- QA tự có thể điền checklist độc lập với dev

Out of scope:
- Thực hiện UAT (Sprint 6)
- Fix bug từ UAT (Sprint 6)

Story IDs: Tất cả US — UAT validates toàn bộ user stories
Acceptance Criteria IDs: Sprint 4 Exit Criteria (UAT checklist đầy đủ)

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (Sprint 4 Exit): UAT checklist có đủ 13 tiêu chí từ SRS Section 15, không thiếu
- AC-02: Mỗi tiêu chí có expected result cụ thể (không dùng từ "đúng" hay "hợp lệ" mà không kèm định nghĩa)
- AC-03: Cột pass/fail sẵn sàng, có thể điền ngay trong Sprint 6
- AC-04: ≥ 2 file DXF test đã được QA xác nhận sẵn sàng (có ghi chú nội dung: số phòng, số cửa, loại phòng)
- AC-05: Checklist được review bởi BA/PM và approve trước khi sprint kết thúc

Module boundary: Documentation, không có code

Files/Modules dự kiến bị ảnh hưởng:
- `docs/uat-checklist.md` hoặc `.xlsx` (tạo mới)
- `tests/fixtures/uat-dxf/` (DXF files cho UAT)

Doc refs:
- /docs/02-PRD-Product-Backlog.md#10. MVP acceptance (13 điều kiện)
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 6 — UAT Checklist 13 tiêu chí

Dependencies: Template Excel frozen (T3-06), story ACs từ 03-User-Stories.md

Known risks:
- SRS Section 15 có thể không có số tiêu chí rõ ràng → QA dùng MVP Acceptance Criteria từ PRD §10 (13 điều kiện)

Open ambiguities:
- SRS Section 15 cụ thể có 13 tiêu chí hay QA cần soạn thêm? → Cần PM xác nhận

Definition of Done:
- [ ] Checklist có ≥ 13 tiêu chí đầy đủ
- [ ] PM/BA approve (email hoặc comment)
- [ ] ≥ 2 file DXF sẵn sàng cho UAT
- [ ] File commit vào repo
