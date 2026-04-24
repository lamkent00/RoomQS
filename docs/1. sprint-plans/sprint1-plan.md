# SPRINT BRIEF

Sprint: Sprint 1 — Foundation & DXF Parsing
Phase: GIAI ĐOẠN 1 — DISCOVERY & FOUNDATION (Sprint 0–1)
Mục tiêu sprint: Môi trường dev hoàn chỉnh; đọc được geometry + text từ DXF (LINE, LWPOLYLINE, TEXT, MTEXT) qua đúng module boundary; prototype packaging .exe chạy được trên máy không có Python. Đây là nền tảng mọi sprint sau phụ thuộc vào.

In-scope:
- BL-01/02: CI pipeline + pytest baseline (Dev-A)
- BL-03: Prototype PyInstaller — Shapely + **PySide6 ≥ 6.6** bundle .exe (Dev-A) — **PRIORITY CAO NHẤT**
- BL-04: Chuẩn bị DXF test fixtures (QA/BA)
- BL-05: CAD Parser đọc LINE/LWPOLYLINE + TEXT/MTEXT → output `RawCADData` (Dev-A) [gộp BL-05 + BL-06]
- BL-06: Đã gộp vào BL-05 — xem trên
- BL-09: Unit detector `$INSUNITS` trong `src/intake/` + apply unit_factor trong `cad_parser` (Dev-A)

Out-of-scope:
- Bất kỳ logic nhận diện phòng nào (Sprint 2)
- Parser INSERT block cửa (BL-07 — Sprint 2)
- Config layer name (BL-08 — Sprint 2)
- Giao diện PySide6 có feature (chỉ cần empty window mở được)
- Unit test BR (Sprint 4)
- MOD-06 text_extractor xử lý tag/classify (Sprint 3)

Risks:
- PyInstaller + Shapely + PySide6 DLL conflict trên Windows → rủi ro cao nhất; phải phát hiện sớm
- BL-04 phụ thuộc file DXF thực từ Sprint 0; nếu chưa có → dùng synthetic tạm
- PySide6 thêm ~60MB vào .exe

Dependencies:
- Sprint 0 exit criteria pass (repo khởi tạo)
- Sample DXF ≥ 1 file (synthetic nếu không có thực)

Danh sách ticket (đã refactor theo kiến trúc):
1. T1-01: Setup CI pipeline + pytest baseline (BL-01, BL-02)
2. T1-02: Prototype PyInstaller — build .exe với Shapely + PySide6 (BL-03)
3. T1-03: CAD Parser — `RawCADData` (LINE/LWPOLYLINE + TEXT/MTEXT + apply unit_factor) [BL-05, BL-06, BL-09 một phần]
4. T1-04: File Intake — detect `$INSUNITS` → `unit_factor` (BL-09 phần intake)
5. T1-05: Text Extractor (MOD-06) — nhận `RawCADData.text_entities`, strip MTEXT formatting
6. T1-06: Chuẩn bị DXF test fixtures (BL-04)

---

# TICKET CONTEXT PACK

Ticket: T1-01 — Setup CI pipeline + pytest baseline
Người phụ trách: Dev-A
Mục tiêu: CI chạy pytest tự động khi push; coverage report làm baseline.

In scope:
- GitHub Actions workflow: `on: [push, pull_request]` → chạy `pytest`
- `pytest.ini` hoặc `pyproject.toml [tool.pytest]`: testpaths=`tests/`, addopts=`--cov=src --cov-report=term-missing`
- `tests/test_smoke.py` — import các module chính, assert không crash
- pre-commit hooks: `ruff` + `black`

Out of scope:
- Coverage threshold enforcement
- Integration test (Sprint 5)
- Deploy / release pipeline

Acceptance Criteria:
- AC-01: GitHub Actions workflow chạy trên mọi push và PR
- AC-02: `pytest` chạy pass (0 lỗi)
- AC-03: Coverage report xuất được
- AC-04: pre-commit hook chạy ruff + black không báo lỗi

Module boundary: `tests/`, `.github/workflows/` — không chạm `src/`

Files dự kiến:
- `.github/workflows/ci.yml` (tạo mới)
- `pytest.ini` hoặc `pyproject.toml`
- `tests/test_smoke.py` (tạo mới)
- `.pre-commit-config.yaml` (tạo mới)

Dependencies: T0-03 (repo tồn tại)

Open ambiguities:
- CI runner Ubuntu hay Windows? (Khuyến nghị: ubuntu-latest để tránh DLL conflict giả trong CI; DLL test thực tế qua T1-02)

Definition of Done:
- [ ] CI pass trên push đầu tiên
- [ ] pytest output hiện trong CI log
- [ ] pre-commit hook hoạt động local

---

# TICKET CONTEXT PACK

Ticket: T1-02 — Prototype PyInstaller — build .exe với Shapely + PySide6
Người phụ trách: Dev-A
Mục tiêu: Xác nhận Shapely + **PySide6 ≥ 6.6** có thể bundle thành .exe chạy được trên Windows 10/11 không cài Python.

> **Tech stack đã chốt:** PySide6 ≥ 6.6 (theo `04-Kien-Truc-Tech-Stack.md` Section 3). Không dùng PyQt6 hay tkinter.

Bối cảnh kỹ thuật:
Shapely 2.0 dùng GEOS DLL. PySide6 dùng Qt DLL. PyInstaller phải collect đủ cả hai. Xung đột phổ biến: `geos_c.dll` không được include, PySide6 plugin không được copy. Dùng `--onedir` mode (không `--onefile`) để giảm antivirus false positive.

In scope:
- `src/ui/main_window.py` — PySide6 QMainWindow đơn giản (title "RoomQS")
- `src/main.py` — entry point, import Shapely, tạo 1 Polygon cơ bản
- `packaging/roomqs.spec` cho PyInstaller
- Build `--onedir` trên máy Dev-A
- Copy dist/ ra máy Windows sạch (không Python), chạy .exe verify
- Nếu DLL conflict: (1) hook Shapely explicit, (2) `--collect-all shapely`, (3) onefile mode

Out of scope:
- Feature UI (chỉ empty window)
- Bundle LISP files (Sprint 6)
- Code signing (Sprint 6)

Acceptance Criteria:
- AC-01: .exe build thành công không báo lỗi PyInstaller
- AC-02: .exe mở được trên máy Windows 10/11 không cài Python — **hard gate**
- AC-03: Cửa sổ PySide6 hiện trong ≤ 5 giây
- AC-04: `from shapely.geometry import Polygon; Polygon([(0,0),(1,0),(1,1)])` không lỗi
- AC-05: Kết quả ghi vào `packaging/test-results.md`

Module boundary:
- `src/ui/main_window.py` — Presentation Layer (UI shell only)
- `src/main.py` — entry point
- `packaging/roomqs.spec` — build config

Files dự kiến:
- `src/ui/__init__.py`, `src/ui/main_window.py`
- `src/main.py`
- `packaging/roomqs.spec`
- `packaging/test-results.md`

Dependencies: T1-01 (CI pass), T0-03 (repo structure)

Known risks:
- DLL conflict Shapely + PySide6 → buffer 3 ngày; nếu fail → escalate Tech Lead
- Antivirus false positive → workaround: `--onedir`

Definition of Done:
- [ ] .exe build thành công
- [ ] Chạy được trên ≥ 1 máy Windows không cài Python
- [ ] `packaging/test-results.md` ghi kết quả
- [ ] PR merged sau CI pass

---

# TICKET CONTEXT PACK

Ticket: T1-04 — File Intake — detect `$INSUNITS` → `unit_factor`
Người phụ trách: Dev-A
Mục tiêu: Module `src/intake/` (MOD-01) đọc header DXF `$INSUNITS` và trả về `unit_factor` để truyền sang `cad_parser`.

> **Kiến trúc:** Theo MOD-01, việc detect `$INSUNITS` và xuất `unit_factor` là trách nhiệm của `File Intake`, không phải `geometry/`. Module `geometry/` (MOD-03) chỉ làm việc với tọa độ đã chuẩn hóa.

Bối cảnh kỹ thuật (ADR-03):
`$INSUNITS` map: 0=unitless(default 1.0+warning), 1=inch×25.4, 2=feet×304.8, 4=mm×1.0, 5=cm×10, 6=m×1000.
Invariant: mọi float trong Python runtime đều là mm.

In scope:
- `src/intake/unit_detector.py`:
  - `detect_unit_factor(filepath: str) -> tuple[float, str]` — đọc header DXF, trả về `(factor, unit_name)`
  - Warning log khi `$INSUNITS=0`
- `src/intake/models.py`: dataclass `IntakeResult(file_path, dxf_version, unit_factor, unit_name)`
- Unit test với mock DXF header (không cần file DXF thực — mock `ezdxf.readfile`)

Out of scope:
- Hỏi user qua UI khi unitless (UI chỉ display warning)
- Validate toàn bộ file DXF (chỉ đọc header)
- Apply unit_factor vào coordinates (thuộc T1-03 / cad_parser)

Acceptance Criteria:
- AC-01: `$INSUNITS=4` (mm) → factor = 1.0
- AC-02: `$INSUNITS=6` (metres) → factor = 1000.0
- AC-03: `$INSUNITS=1` (inches) → factor = 25.4
- AC-04: `$INSUNITS=0` → factor = 1.0 + log warning "Don vi ve khong xac dinh"
- AC-05: Unit test pass với mock header (không cần file DXF thực)

Module boundary: `src/intake/` — chỉ đọc header ezdxf, không parse entities

Files dự kiến:
- `src/intake/__init__.py`, `src/intake/unit_detector.py` (tạo mới)
- `src/intake/models.py` — `IntakeResult`
- `tests/unit/test_unit_detector.py`

Dependencies: Không có (module độc lập, có thể mock hoàn toàn)

Definition of Done:
- [ ] `unit_detector.py` với hàm `detect_unit_factor()`
- [ ] Unit test cover tất cả $INSUNITS values
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T1-03 — CAD Parser — `RawCADData` (LINE/LWPOLYLINE + TEXT/MTEXT + apply unit_factor)
Người phụ trách: Dev-A
Mục tiêu: Module `src/cad_parser/` (MOD-02) là điểm duy nhất tương tác với ezdxf entities. Output là `RawCADData` chuẩn hóa đơn vị mm — data structure trung gian cho tất cả modules sau.

> **Kiến trúc:** MOD-02 chịu trách nhiệm đọc TẤT CẢ entities (LINE, LWPOLYLINE, TEXT, MTEXT) VÀ apply `unit_factor` vào tọa độ. MOD-06 (text_extractor) và MOD-03 (geometry) KHÔNG tương tác trực tiếp với ezdxf.

Bối cảnh kỹ thuật:
- LINE: `dxf.start`, `dxf.end` → apply factor
- LWPOLYLINE: `.get_points()` → apply factor
- TEXT: `dxf.text`, `dxf.insert` → apply factor cho position
- MTEXT: `dxf.text` (có thể chứa `{\fArial;PHONG NGU}`) → raw text; strip sẽ do MOD-06 làm
- `unit_factor` nhận từ `IntakeResult` (output của T1-04/MOD-01)

In scope:
- `src/cad_parser/dxf_reader.py`:
  - `parse_dxf(filepath: str, layer_config: LayerConfig, unit_factor: float) -> RawCADData`
  - Đọc LINE/LWPOLYLINE từ wall_layers → `wall_segments`
  - Đọc TEXT/MTEXT từ mọi layer → `text_entities` (raw, chưa strip)
  - Apply `unit_factor` vào MỌI coordinates trước khi đưa vào RawCADData
- `src/cad_parser/models.py`:
  - `RawCADData(wall_segments: list[Segment], text_entities: list[RawTextEntity], door_blocks: list)`
  - `Segment(start: tuple, end: tuple, layer: str)`
  - `RawTextEntity(raw_content: str, position: tuple, layer: str)` — raw_content chưa strip
- Unit test: `tests/unit/test_dxf_reader.py`

Out of scope:
- Strip MTEXT formatting (T1-05 — text_extractor)
- Đọc INSERT block cửa (Sprint 2)
- Geometry normalization / Shapely (MOD-03 — Sprint 2)

Acceptance Criteria:
- AC-01: `parse_dxf()` trả về `RawCADData` với đủ 3 fields
- AC-02: LINE entities từ wall layer đúng số lượng so với fixture đã biết
- AC-03: LWPOLYLINE entities đúng số điểm và layer
- AC-04: TEXT + MTEXT entities đều có trong `text_entities` (raw content, chưa strip)
- AC-05: Tất cả coordinates đã nhân `unit_factor` (`$INSUNITS=1` → ×25.4)
- AC-06: Entity từ layer không có trong wall_layer_names bị exclude khỏi `wall_segments`
- AC-07: File DXF corrupt → raise exception rõ ràng
- AC-08: Unit test pass trong CI

Module boundary:
- `src/cad_parser/` — ezdxf parsing only
- KHÔNG gọi Shapely
- KHÔNG gọi text_extractor
- KHÔNG gọi UI
- Nhận `unit_factor` từ caller (MOD-01), không tự đọc `$INSUNITS`

Files dự kiến:
- `src/cad_parser/__init__.py`, `src/cad_parser/dxf_reader.py`
- `src/cad_parser/models.py`
- `tests/unit/test_dxf_reader.py`
- `tests/fixtures/simple_rooms.dxf` (từ T1-06)

Dependencies: T1-04 (unit_factor), T1-06 (fixtures)

Known risks:
- ezdxf ≥ 1.3 có breaking change API so với 0.x — verify trước khi code
- POLYLINE 3D vs LWPOLYLINE — cần handle cả hai

Definition of Done:
- [ ] `dxf_reader.py` với hàm `parse_dxf()`
- [ ] `RawCADData` dataclass đầy đủ
- [ ] Unit test pass với ≥ 2 fixture
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T1-05 — Text Extractor (MOD-06) — strip MTEXT, normalize text entities
Người phụ trách: Dev-A
Mục tiêu: Module `src/text_extractor/` (MOD-06) nhận `RawCADData.text_entities` (đã có coordinates mm), strip MTEXT formatting codes, trả về `List[TextTag]` sẵn sàng cho spatial lookup ở Sprint 3.

> **Kiến trúc:** MOD-06 KHÔNG tương tác với ezdxf `doc`. Input duy nhất là `list[RawTextEntity]` từ `RawCADData`. Coordinates đã là mm (do cad_parser apply rồi). MOD-06 chỉ xử lý nội dung text.

Bối cảnh kỹ thuật:
- MTEXT formatting codes ví dụ: `{\fArial|b0|i0|c0|p34;PHONG NGU}`, `\PPHONG NGU` → cần strip
- Strip regex: `re.sub(r'\{\\[^}]*\}', '', text)` + `re.sub(r'\\[A-Za-z]+;?', '', text)`
- Normalize whitespace sau khi strip

In scope:
- `src/text_extractor/processor.py`:
  - `process_text_entities(raw_entities: list[RawTextEntity]) -> list[TextTag]`
  - `strip_mtext_formatting(raw: str) -> str`
- `src/text_extractor/models.py`:
  - `TextTag(content: str, position: tuple[float,float], layer: str)`
- Unit test thuần Python (không cần ezdxf, không cần file DXF)

Out of scope:
- Spatial lookup / point-in-polygon (Sprint 3 — MOD-04)
- Phân loại room_name vs room_code (Sprint 3)
- Tương tác với ezdxf (KHÔNG được phép)

Acceptance Criteria:
- AC-01: TEXT entity raw `"PHONG NGU"` → `TextTag.content = "PHONG NGU"`
- AC-02: MTEXT raw `"{\fArial;PHONG NGU}"` → `TextTag.content = "PHONG NGU"`
- AC-03: MTEXT `"\PPHONG NGU"` → `TextTag.content = "PHONG NGU"`
- AC-04: `position` và `layer` được pass through không thay đổi
- AC-05: Unit test pass (không cần file DXF — dùng mock `RawTextEntity` list)

Module boundary:
- `src/text_extractor/` — text processing only
- KHÔNG import ezdxf
- KHÔNG gọi Shapely
- KHÔNG đọc file

Files dự kiến:
- `src/text_extractor/__init__.py`, `src/text_extractor/processor.py`
- `src/text_extractor/models.py`
- `tests/unit/test_text_processor.py`

Dependencies: T1-03 (RawCADData.RawTextEntity model — cần import để type check)

Known risks: Thấp — logic thuần string, testable hoàn toàn isolated

Definition of Done:
- [ ] `processor.py` với `process_text_entities()` và `strip_mtext_formatting()`
- [ ] Unit test cover TEXT và MTEXT formatting cases
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T1-06 — Chuẩn bị DXF test fixtures
Người phụ trách: QA / BA
Mục tiêu: Bộ fixture DXF đủ để Dev-A viết unit test cho T1-03/T1-04/T1-05.

In scope:
- `simple_rooms.dxf`: synthetic, 3 phòng hình chữ nhật, layer tường "TUONG", text "PHONG NGU"/"WC"/"PHONG KHACH", $INSUNITS=4 (mm)
- `real_sample.dxf`: file DXF thực từ Sprint 0 (nếu có)
- `corrupt.dxf`: file DXF bị truncate để test error handling
- `tests/fixtures/README.md`: mô tả entity count, layer, expected values

Out of scope:
- Fixture L-shape (Sprint 2)
- Fixture với block cửa (Sprint 2)

Acceptance Criteria:
- AC-01: `simple_rooms.dxf` document đúng entity count (VD: 12 LINE trên layer TUONG, 3 TEXT)
- AC-02: File đọc được bằng `ezdxf.readfile()` không exception
- AC-03: `corrupt.dxf` raise `ezdxf.DXFError`
- AC-04: `README.md` liệt kê entity count, layer names, expected values

Module boundary: `tests/fixtures/` — không chạm src/

Files dự kiến:
- `tests/fixtures/simple_rooms.dxf`
- `tests/fixtures/real_sample.dxf`
- `tests/fixtures/corrupt.dxf`
- `tests/fixtures/banve.dxf`
- `tests/fixtures/README.md`

Dependencies: T0-01 (file DXF thực nếu có)

Known risks:
- Nếu không có AutoCAD → tạo `simple_rooms.dxf` bằng script Python + ezdxf

Definition of Done:
- [ ] 3 fixture files tồn tại trong `tests/fixtures/`
- [ ] README.md đầy đủ expected values
- [ ] Dev-A xác nhận fixture dùng được để viết test
