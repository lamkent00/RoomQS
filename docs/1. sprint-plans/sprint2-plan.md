# SPRINT BRIEF

Sprint: Sprint 2 — Room Recognition Prototype ⚠️
Phase: GIAI ĐOẠN 2 — PROTOTYPE & VALIDATE
Mục tiêu sprint: Validate thuật toán nhận diện phòng (XR + GB) trên bản vẽ thực. Đây là **go/no-go decision point** của toàn dự án. Nếu không đạt ngưỡng → PM quyết định re-estimate hoặc thu hẹp scope trước khi tiếp tục.

In-scope:
- BL-08: Cơ chế config layer name — không hard-code, đọc từ config.yaml (Dev-B, 1 ngày)
- BL-07: Parser DXF — đọc INSERT block cửa + attributes (Dev-A, 1.5 ngày)
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
- width/height cửa từ Excel (BL-19 — Sprint 4)

Risks:
- BPOLY bị "nhiễu" bởi nội thất, hatch, rác ngắn < 300mm → GB lọc theo `short_segment_threshold_mm=300` trong config
- Layer tường không khớp tên cấu hình → BL-08 xử lý; nhưng nếu file DXF thực có convention khác → cần re-config ngay
- Phòng L-shape phức tạp hơn dự kiến → GB có thể không đạt ngưỡng 2/3; nếu vậy → PM quyết định thu hẹp MVP
- Không có AutoCAD 2019+ → BLOCKER cứng cho BL-10/BL-11

Contingency Plan (W-03 — Dev-B capacity tight):
- Ngày 1–5: Dev-B ưu tiên T2-01 → T2-03 (XR) là critical path
- Ngày 6+: Dev-B chuyển sang T2-04 (GB) sau khi T2-03 đạt hard gate
- Nếu T2-04 không đủ thời gian test đủ 3 case trước ngày 9: ghi nhận kết quả sơ bộ (X/3), extend T2-04 sang Sprint 2.5
- Dev-A hỗ trợ test manual T2-04 sau khi hoàn thành T2-02 (~ngày 2)
- PM chuẩn bị phương án thu hẹp MVP xuống "chỉ phòng vuông vức" nếu GB chưa đủ kết quả vào ngày demo

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

# PM REVIEW DECISIONS
> *Cập nhật sau QA Review ngày 2026-04-24. Tất cả decisions dưới đây phải được Tech Lead và Dev xác nhận trước Sprint Start.*

## D-01 — W-01: Kiến trúc door_reader và ezdxf boundary
**Quyết định: Option 2 — Pass through cad_parser (clean boundary)**

`cad_parser/dxf_reader.py` (T1-03) được mở rộng để trả thêm `RawCADData.door_blocks: list[dict]` chứa INSERT entities đã được extract thành thuần Python (không expose ezdxf object). `door_engine/door_reader.py` chỉ nhận `list[dict]` này — không import ezdxf trực tiếp.

- Thực hiện trong T2-02, không tạo thêm ticket
- `RawCADData` dataclass thêm field `door_blocks: list[dict]`
- Arch doc section MOD-02 ghi nhận: cad_parser là điểm duy nhất tương tác ezdxf (giữ nguyên nguyên tắc)
- Effort bổ sung ước tính ~2–3 giờ cho Dev-A

## D-02 — W-02: Phân tách output BL-07 giữa T2-02 và BL-19
**Quyết định: Confirm split — T2-02 giao code/position/raw_attributes; width/height ở BL-19**

- `DoorBlock(door_code: str, position: tuple, raw_attributes: dict)` là deliverable hoàn chỉnh của T2-02
- `width_mm`, `height_mm` không có trong T2-02 — sẽ được bổ sung ở BL-19 Sprint 4 sau khi có cơ chế tra cứu Excel
- PRD BL-07 cần được annotate: "Deliverable chia 2 sprint: code/position/raw_attributes → Sprint 2; width/height → Sprint 4 (BL-19)"

## D-03 — W-03: Dev-B capacity contingency
**Quyết định: T2-04 có thể extend sang Sprint 2.5 nếu cần**

- Xem Contingency Plan trong Sprint Brief
- Go/No-go vẫn tiến hành theo lịch — nếu GB chưa đủ kết quả: demo XR (bắt buộc), trình bày kết quả sơ bộ GB

## D-04 — Naming: config_loader.py vs loader.py
**Quyết định: Giữ `src/config/config_loader.py` (tên rõ nghĩa hơn)**

- Arch doc section MOD-12 sẽ được cập nhật để thống nhất tên file sau Sprint 2

## D-05 — Ambiguity T2-01: LISP đọc config từ đâu?
**Quyết định: Python xuất `config/lisp_export.txt` dạng `KEY=VALUE`**

```
WALL_LAYERS=TUONG,A-WALL,WALL
SHORT_SEGMENT_THRESHOLD_MM=300
```

LISP đọc bằng `(open "config/lisp_export.txt" "r")`. Python tự động generate file này khi load config. Không dùng DCL, không dùng prompt.

## D-06 — Ambiguity T2-03: Chiều dày tường — đo mép trong hay tâm?
**Quyết định: LISP đo đến mép trong (inner edge) của LINE/LWPOLYLINE tường**

- Với LINE entity: tia giao với line = mép tường
- Với LWPOLYLINE có width: tia giao với center-line (ezdxf default); chấp nhận sai số ≤ chiều dày tường
- Refinement đo chính xác chiều dày tường dành cho Sprint 3+

## D-07 — Ambiguity T2-04: GB tạo boundary theo tọa độ thực hay selection set?
**Quyết định: Dùng layer filter + coordinate-based boundary set (nhất quán với XR)**

- GB dùng `ssget "X" (list (cons 8 wall-layers))` để build boundary set theo layer
- Không dùng manual selection set (user chỉ click 1 điểm interior, GB tự làm phần còn lại)
- Approach nhất quán với XR: cả 2 lệnh đều chỉ cần 1 điểm click từ user

---

# TICKET CONTEXT PACK

Ticket: T2-01 — BL-08 Config layer name — không hard-code
Người phụ trách: Dev-B
Mục tiêu: Cơ chế đọc layer name từ config.yaml thay vì hard-code trong LISP/Python, để hệ thống có thể dùng được trên nhiều file bản vẽ có convention layer khác nhau.

**Bối cảnh kỹ thuật:**
File bản vẽ của các dự án khác nhau có thể đặt tên layer tường là "TUONG", "A-WALL", "WALL", "Tuong", v.v. Hard-code là rủi ro cao. Cơ chế: Python đọc `config.yaml` → pass `wall_layer_names` vào DXF parser; Python đồng thời xuất `config/lisp_export.txt` (KEY=VALUE) để LISP đọc qua `(open)`.

**Quyết định kiến trúc (D-04, D-05):**
- File đặt tại `src/config/config_loader.py` (khác với arch doc ghi `loader.py` — sẽ đồng bộ doc sau Sprint 2)
- LISP đọc config từ `config/lisp_export.txt` do Python generate — không dùng YAML trực tiếp, không dùng prompt

In scope:
- Module `src/config/config_loader.py`:
  - Hàm `load_config(path: str = "config.yaml") -> dict`
  - Đọc section `cad.wall_layer_names` trả về list string
  - Đọc `cad.short_segment_threshold_mm` (float)
  - Hàm `export_lisp_config(config: dict, output_path: str = "config/lisp_export.txt") -> None` — xuất file KEY=VALUE cho LISP
- LISP side: tạo hàm `(defun load-lisp-config (path))` đọc `lisp_export.txt` và set biến toàn cục `*wall-layers*`, `*short-segment-threshold*`
- Unit test: load config mock và verify đúng giá trị; test export file KEY=VALUE

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
- AC-05: `export_lisp_config()` tạo được file `lisp_export.txt` với format `WALL_LAYERS=...` và `SHORT_SEGMENT_THRESHOLD_MM=...`
- AC-06: LISP load `lisp_export.txt` thành công, biến `*wall-layers*` là list đúng giá trị

Module boundary:
- `src/config/config_loader.py` — đọc file + xuất lisp config, không có logic nghiệp vụ
- `lisp/config_helper.lsp` — đọc `lisp_export.txt`, set biến toàn cục LISP

Files/Modules dự kiến bị ảnh hưởng:
- `src/config/__init__.py`, `src/config/config_loader.py` (tạo mới)
- `config/config.yaml` (đã có template từ T0-03, nay thêm giá trị cụ thể)
- `config/lisp_export.txt` (auto-generated, thêm vào .gitignore hoặc commit template rỗng)
- `lisp/config_helper.lsp` (tạo mới)
- `tests/unit/test_config_loader.py` (tạo mới)

Doc refs:
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-04: Quản lý cấu hình rule nghiệp vụ
- /docs/02-PRD-Product-Backlog.md#Rủi ro dữ liệu DXF (layer naming)

Dependencies: T0-03 (config.yaml template đã có)

Known risks:
- LISP AutoCAD 2019 có thể có path resolution khác nhau khi đọc file tương đối → cần test trên máy Dev-B ngay ngày 1

Open ambiguities: **RESOLVED — D-05**: Python generate `config/lisp_export.txt` dạng KEY=VALUE; LISP đọc qua `(open)`.

Definition of Done:
- [ ] `config_loader.py` đọc được `config.yaml`
- [ ] `export_lisp_config()` tạo được `lisp_export.txt` đúng format
- [ ] LISP `load-lisp-config` load được file và set biến toàn cục đúng
- [ ] Unit test pass (Python side)
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T2-02 — BL-07 Parser INSERT block cửa + attributes
Người phụ trách: Dev-A
Mục tiêu: Module `door_engine` đọc được các INSERT entity (block cửa) từ DXF, lấy `door_code` từ tên block hoặc attribute, và `position` (insertion point) — làm nền cho door mapping ở Sprint 3–4.

**Bối cảnh kỹ thuật:**
INSERT entity trong ezdxf: `entity.dxf.name` là tên block (thường là mã cửa như "D1", "D2"). Nếu là attributed block: `entity.attribs` chứa các ATTRIB entity với `tag` và `value`. Config `door_block_prefixes` dùng để filter block là cửa (loại bỏ block nội thất, ký hiệu kỹ thuật).

**Quyết định kiến trúc (D-01 — W-01):**
`door_reader.py` **KHÔNG** import ezdxf trực tiếp. Thay vào đó:
1. `cad_parser/dxf_reader.py` được mở rộng: thêm method `extract_door_block_data(doc) -> list[dict]` trả về list dict thuần Python `{name, position, attribs}` từ INSERT entities
2. `RawCADData` dataclass thêm field `door_blocks: list[dict]`
3. `door_engine/door_reader.py` nhận `raw_cad_data.door_blocks` và filter/map thành `list[DoorBlock]`
Approach này giữ MOD-02 là điểm duy nhất tương tác ezdxf.

**Xác nhận scope BL-07 (D-02 — W-02):**
T2-02 chỉ giao `DoorBlock(door_code, position, raw_attributes)`. `width_mm` và `height_mm` sẽ được bổ sung ở BL-19 Sprint 4 sau khi có tra cứu Excel. `raw_attributes` dict sẽ bảo tồn đầy đủ key-value từ ATTRIB entity để Sprint 4 có thể đọc nếu cần.

In scope:
- Mở rộng `src/cad_parser/dxf_reader.py` (T1-03):
  - Thêm method `extract_door_block_data(doc) -> list[dict]` — extract INSERT entities thành thuần Python
  - `RawCADData` dataclass thêm field `door_blocks: list[dict]`
- Module `src/door_engine/door_reader.py`:
  - Hàm `extract_door_blocks(raw_door_blocks: list[dict], config: dict, bbox=None) -> list[DoorBlock]`
  - Lọc theo `door_block_prefixes` từ config
  - Map dict → `DoorBlock`
- Data class `DoorBlock(door_code: str, position: tuple, raw_attributes: dict)`
- **Không** tra cứu kích thước (width/height) trong ticket này — làm ở Sprint 4 BL-19
- Unit test với DXF fixture có block cửa

Out of scope:
- Import ezdxf trong `door_engine/` (xem D-01)
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
- AC-05: `door_reader.py` không import ezdxf — chỉ nhận `list[dict]` từ cad_parser
- AC-06: Unit test pass với fixture có 3 block cửa và 2 block không phải cửa

Module boundary:
- `src/cad_parser/dxf_reader.py` — mở rộng để extract INSERT data (vẫn là điểm duy nhất dùng ezdxf)
- `src/door_engine/door_reader.py` — chỉ nhận `list[dict]`, không dùng ezdxf
- Phụ thuộc `src/config/config_loader.py` (T2-01)
- Không gọi Shapely

Files/Modules dự kiến bị ảnh hưởng:
- `src/cad_parser/dxf_reader.py` (mở rộng — thêm method extract_door_block_data + RawCADData.door_blocks)
- `src/cad_parser/models.py` — RawCADData thêm field door_blocks
- `src/door_engine/__init__.py`, `src/door_engine/door_reader.py` (tạo mới)
- `src/door_engine/models.py` — DoorBlock dataclass
- `tests/unit/test_door_reader.py` (tạo mới)
- `tests/fixtures/` — cần fixture có INSERT block cửa

Doc refs:
- /docs/03-User-Stories.md#US-DOOR-001
- /docs/02-PRD-Product-Backlog.md#FR-08, FR-09
- /docs/04-Kien-Truc-Tech-Stack.md#Module Breakdown — cad_parser (MOD-02), door_engine (MOD-05)

Dependencies: T2-01 (config_loader), T1-03 (dxf_reader — mở rộng, không làm lại từ đầu)

Known risks:
- Block cửa trong bản vẽ thực có thể không dùng attribute — chỉ dùng block name làm mã cửa → cần verify với file DXF thực trước khi code
- Mở rộng T1-03 (cad_parser) phải không phá vỡ test hiện có của Sprint 1

Open ambiguities:
- Attribute tag tên cửa là gì? (Cần xem file DXF thực từ Sprint 0 — nếu không có attribute, `door_code = entity.name`)

Definition of Done:
- [ ] `cad_parser/dxf_reader.py` extract được INSERT entities vào `RawCADData.door_blocks`
- [ ] Sprint 1 test của cad_parser vẫn pass sau khi mở rộng
- [ ] `door_reader.py` extract đúng DoorBlock từ `list[dict]` — không import ezdxf
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

**Quyết định chiều dày tường (D-06):**
LISP đo đến mép trong (inner edge) của LINE/LWPOLYLINE tường. Với LINE: giao điểm tia là mép. Với LWPOLYLINE có width: dùng center-line; chấp nhận sai số ≤ chiều dày tường. Refinement đo chính xác chiều dày tường dành cho Sprint 3+.

In scope:
- File `lisp/xr.lsp`:
  - Load `lisp/config_helper.lsp` để lấy `*wall-layers*` từ `lisp_export.txt`
  - Hàm `(defun c:XR ())` — lệnh user gọi trong AutoCAD
  - Prompt "Click 1 diem vao giua phong:"
  - Bắn 4 tia, tìm mép trong tường, tạo LWPOLYLINE đỏ, closed
  - Thông báo lỗi nếu không tìm đủ 4 mép ("Loi: Khong tim thay du 4 vach tuong!")
  - Lọc boundary set theo layer tường từ biến `*wall-layers*`
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
- Phụ thuộc `lisp/config_helper.lsp` (T2-01)
- Không phụ thuộc Python (prototype phase)

Files/Modules dự kiến bị ảnh hưởng:
- `lisp/xr.lsp` (tạo mới)
- `lisp/config_helper.lsp` (từ T2-01)
- `lisp/README.md` (cập nhật: cách load và test XR)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-001, US-ROOM-002
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 2 — Acceptance ngưỡng prototype
- /docs/02-PRD-Product-Backlog.md#Rủi ro nhận diện phòng / cửa

Dependencies: T2-01 (config_helper.lsp + lisp_export.txt đã có); AutoCAD 2019+ (T0-06)

Known risks:
- BPOLY bị nhiễu bởi hatch, nội thất → giải pháp: boundary set chỉ layer tường
- Tường hở tại vị trí cửa gây 4 tia không gặp đủ mép → Door Sealing là giải pháp (BL-12 Sprint 3); ở prototype: ghi nhận case này là "fail — cần Door Sealing"
- Phòng không vuông (góc không 90°) → XR sẽ fail → đây là use case của GB

Open ambiguities: **RESOLVED — D-06**: LISP đo đến mép trong (inner edge) của tường. Sai số chiều dày tường chấp nhận ở prototype.

Definition of Done:
- [ ] `lisp/xr.lsp` load được vào AutoCAD 2019+ không báo lỗi
- [ ] `config_helper.lsp` load được và biến `*wall-layers*` đúng giá trị
- [ ] Test thủ công 5 phòng HCN — ghi kết quả pass/fail từng case
- [ ] ≥ 4/5 pass — hard gate
- [ ] ≥ 2/2 phòng có cửa không bị lẹm — hard gate
- [ ] Kết quả ghi vào `docs/sprint2-prototype-report.md`

---

# TICKET CONTEXT PACK

Ticket: T2-04 — BL-11 [PROTOTYPE] AutoLISP thuật toán GB (Ghost Boundary)
Người phụ trách: Dev-B (hỗ trợ test: Dev-A sau khi T2-02 xong)
Mục tiêu: Viết và validate prototype AutoLISP lệnh `GB` nhận diện phòng L-shape và phòng không vuông vức bằng thuật toán Ghost Boundary. **Ngưỡng: ≥ 2/3 phòng L-shape từ file thực.**

**Bối cảnh thuật toán GB (Ghost Boundary):**
GB dùng lệnh AutoCAD `-BOUNDARY` với boundary set được lọc. Khác với XR (tia), GB tạo ra boundary dựa trên vùng kín xung quanh điểm click. Lọc entity ngắn < `short_segment_threshold_mm` (300mm) để loại rác. Phù hợp với phòng có hình dạng phức tạp mà XR không xử lý được.

**Ngưỡng pass prototype:**
- GB: ≥ 2/3 phòng L-shape từ file DXF thực tạo Polyline đúng

**Quyết định approach (D-07):**
GB dùng `ssget "X" (list (cons 8 wall-layers-string))` để build boundary set theo layer — không dùng manual selection. User chỉ cần click 1 điểm interior. Approach nhất quán với XR, cả 2 lệnh đều single-click.

**Contingency (W-03):** Nếu T2-04 không xong trước ngày demo → ghi nhận kết quả sơ bộ (X/3 đã test), extend sang Sprint 2.5. PM được thông báo ngay ngày 8 nếu có risk.

In scope:
- File `lisp/gb.lsp`:
  - Load `lisp/config_helper.lsp` để lấy `*wall-layers*` và `*short-segment-threshold*`
  - Hàm `(defun c:GB ())` — lệnh GB
  - Build boundary set bằng `ssget "X"` filter theo layer tường
  - Filter entity rác < `*short-segment-threshold*` mm
  - Gọi `-BOUNDARY` với boundary set đã lọc
  - Lấy LWPOLYLINE kết quả, đổi màu đỏ (color=1), closed=True
  - Thông báo lỗi nếu không tạo được boundary ("Ranh gioi khong khep kin hoac diem click nam ngoai")
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
- `lisp/config_helper.lsp` (từ T2-01)
- `lisp/README.md` (cập nhật hướng dẫn GB)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-001, US-ROOM-002
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 2 — Acceptance ngưỡng prototype
- /docs/02-PRD-Product-Backlog.md#Rủi ro nhận diện phòng

Dependencies: T2-01 (config_helper.lsp + lisp_export.txt); T2-03 (config_helper.lsp đã dùng trong XR — tái sử dụng)

Known risks:
- `-BOUNDARY` lệnh AutoCAD có thể không tạo được LWPOLYLINE nếu vùng không kín hoàn toàn → cần Door Sealing (Sprint 3)
- Phòng L-shape phức tạp (nhiều góc) có thể vượt khả năng GB cơ bản → ghi nhận trong báo cáo prototype
- Dev-B capacity tight (W-03) → Dev-A hỗ trợ test manual từ ngày 2

Open ambiguities: **RESOLVED — D-07**: GB dùng `ssget "X"` layer filter + single interior click; không dùng manual selection set. Nhất quán với XR approach.

Definition of Done:
- [ ] `lisp/gb.lsp` load được vào AutoCAD 2019+ không báo lỗi
- [ ] `config_helper.lsp` load được và biến `*short-segment-threshold*` đúng giá trị
- [ ] Test thủ công 3 phòng L-shape — ghi kết quả từng case
- [ ] ≥ 2/3 pass — hard gate (hoặc ghi nhận partial nếu extend sang Sprint 2.5)
- [ ] Kết quả ghi vào `docs/sprint2-prototype-report.md`

---

# TICKET CONTEXT PACK

Ticket: T2-05 — Báo cáo prototype + demo cho PM/BA + quyết định go/no-go
Người phụ trách: Dev-B (demo), PM (quyết định)
Mục tiêu: Tổng hợp kết quả prototype, thực hiện live demo cho PM/BA, có quyết định rõ ràng "Tiếp tục Sprint 3" hoặc "Cần re-estimate" trước khi sprint đóng.

**Bối cảnh quan trọng:**
Đây là **Checkpoint CP-1 (Go/No-go)**. Không có trạng thái "có vẻ ổn". Phải có số liệu cụ thể. Nếu XR < 4/5 hoặc GB < 2/3 → PM triệu tập session khẩn, quyết định (1) extend Sprint 2/2.5 hoặc (2) thu hẹp scope xuống chỉ phòng vuông vức.

**Nếu T2-04 extend sang Sprint 2.5 (W-03 contingency):** Demo vẫn tiến hành với kết quả XR (bắt buộc) + kết quả GB sơ bộ. PM ra quyết định dựa trên kết quả XR + kế hoạch GB.

In scope:
- Viết `docs/sprint2-prototype-report.md`:
  - Bảng kết quả: case ID | loại phòng | thuật toán | pass/fail | nguyên nhân fail (nếu có)
  - Tổng hợp: X/Y pass XR, X/Y pass GB, X/Y phòng có cửa không lẹm
  - Các case fail: mô tả nguyên nhân kỹ thuật cụ thể
  - Kết luận: đạt/không đạt ngưỡng
- Live demo trong meeting: click phòng trong AutoCAD → LWPOLYLINE đỏ xuất hiện
- PM xác nhận: "Tiếp tục Sprint 3" hoặc "Re-estimate" hoặc "Extend Sprint 2.5"

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

Dependencies: T2-03 (kết quả XR); T2-04 (kết quả GB — có thể partial nếu extend)

Known risks:
- PM/BA không available cho meeting → cần book slot ngay từ đầu sprint (ngày 1)
- Kết quả boundary tạo xong nhưng không đúng hình dạng → vẫn là "fail", không được tính là "pass"

Open ambiguities: Không có — ngưỡng đã được định nghĩa rõ

Definition of Done:
- [ ] Báo cáo prototype hoàn chỉnh với số liệu thực
- [ ] Demo đã diễn ra
- [ ] PM đã có quyết định rõ ràng bằng văn bản
- [ ] Sprint 2 được đóng chính thức sau khi PM confirm
