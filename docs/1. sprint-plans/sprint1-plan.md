# SPRINT BRIEF

Sprint: Sprint 1 — Foundation & DXF Parsing
Phase: GIAI ĐOẠN 1 — DISCOVERY & FOUNDATION (Sprint 0–1)
Mục tiêu sprint: Môi trường dev hoàn chỉnh; đọc được geometry từ DXF (LINE, TEXT, INSERT); prototype packaging .exe chạy được trên máy không có Python. Đây là nền tảng mọi sprint sau phụ thuộc vào.

In-scope:
- BL-01: Khởi tạo repo hoàn chỉnh, cấu trúc thư mục, CI pipeline cơ bản (Dev-A)
- BL-02: Cấu hình pytest baseline + coverage report (Dev-A)
- BL-03: Prototype PyInstaller — Shapely + PySide6 bundle .exe (Dev-A) — **PRIORITY CAO NHẤT**
- BL-04: Chuẩn bị sample DXF test fixtures (≥ 3 file, gồm 1 thực + synthetic) (QA/BA)
- BL-05: Parser DXF — đọc LINE/LWPOLYLINE theo layer name (Dev-A)
- BL-06: Parser DXF — đọc TEXT/MTEXT (tên phòng, mã phòng) (Dev-A)
- BL-09: Normalize đơn vị DXF từ `$INSUNITS` sang mm (Dev-A)

Out-of-scope:
- Bất kỳ logic nhận diện phòng nào (Sprint 2)
- Parser INSERT block cửa (BL-07 — Sprint 2)
- Config layer name (BL-08 — Sprint 2)
- Giao diện PySide6 có feature (chỉ cần empty window mở được)
- Unit test BR (Sprint 4)

Risks:
- PyInstaller + Shapely + PySide6 DLL conflict trên Windows → đây là rủi ro cao nhất; phải phát hiện sớm
- BL-04 phụ thuộc file DXF thực từ Sprint 0; nếu Sprint 0 chưa có → dùng synthetic tạm
- PySide6 thêm ~60MB vào .exe; nếu size quá lớn → xem xét tkinter thay thế

Dependencies:
- Sprint 0 exit criteria pass (repo khởi tạo, sample DXF có ít nhất 1 file)
- Sample DXF ≥ 1 file (synthetic nếu không có thực)

Danh sách ticket:
1. T1-01: Setup CI pipeline + pytest baseline (BL-01, BL-02)
2. T1-02: Prototype PyInstaller — build .exe với Shapely + PySide6 (BL-03)
3. T1-03: DXF Parser — đọc LINE/LWPOLYLINE theo layer (BL-05)
4. T1-04: DXF Parser — đọc TEXT/MTEXT (BL-06)
5. T1-05: Normalize đơn vị $INSUNITS → mm (BL-09)
6. T1-06: Chuẩn bị DXF test fixtures (BL-04)

---

# TICKET CONTEXT PACK

Ticket: T1-01 — Setup CI pipeline + pytest baseline
Người phụ trách: Dev-A
Mục tiêu: Có CI chạy pytest tự động khi push, đảm bảo không ai merge code broken; có coverage report làm baseline cho các sprint sau.

In scope:
- Setup GitHub Actions workflow: `on: [push, pull_request]` → chạy `pytest`
- Cấu hình `pytest.ini` hoặc `pyproject.toml [tool.pytest]`:
  - testpaths = `tests/`
  - addopts = `--cov=src --cov-report=term-missing`
- Tạo test đầu tiên: `tests/test_smoke.py` — import các module chính, assert không crash
- Cấu hình pre-commit hooks: `ruff` (linting), `black` (formatting)

Out of scope:
- Coverage threshold enforcement (chỉ report, không fail nếu < X%)
- Integration test (Sprint 5)
- Deploy / release pipeline

Story IDs: Không có story riêng — technical prerequisite cho US-OPS-001
Acceptance Criteria IDs: Dẫn xuất từ Exit Criteria Sprint 1

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: GitHub Actions workflow chạy trên mọi push và PR
- AC-02: `pytest` chạy pass (0 lỗi) — dù chỉ có smoke test
- AC-03: Coverage report xuất được (%, không yêu cầu ngưỡng cụ thể ở sprint này)
- AC-04: Pre-commit hook chạy ruff + black không báo lỗi với code hiện tại

Module boundary: `tests/`, CI config (`.github/workflows/`), không chạm module src

Files/Modules dự kiến bị ảnh hưởng:
- `.github/workflows/ci.yml` (tạo mới)
- `pytest.ini` hoặc `pyproject.toml`
- `tests/test_smoke.py` (tạo mới)
- `.pre-commit-config.yaml` (tạo mới)

Doc refs:
- /docs/06-Setup-Moi-Truong-Trien-Khai.md#3. Setup Local Development
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 1 — Exit criteria (CI pipeline)

Dependencies: T0-03 (repo tồn tại)

Known risks:
- GitHub Actions runner trên Windows chậm hơn Linux; có thể cần `runs-on: ubuntu-latest` với cross-platform workaround

Open ambiguities:
- CI chạy trên Windows runner hay Ubuntu? (Cần quyết định — DLL conflict chỉ xảy ra trên Windows)

Definition of Done:
- [ ] GitHub Actions CI chạy và pass trên push đầu tiên
- [ ] pytest output hiện trong CI log
- [ ] pre-commit hook hoạt động local trên máy Dev-A

---

# TICKET CONTEXT PACK

Ticket: T1-02 — Prototype PyInstaller — build .exe với Shapely + PySide6
Người phụ trách: Dev-A
Mục tiêu: Xác nhận stack Shapely + PySide6 có thể bundle thành .exe chạy được trên Windows 10/11 không cài Python — đây là rủi ro kỹ thuật cao nhất của toàn dự án, phải resolve trong Sprint 1.

**Bối cảnh kỹ thuật quan trọng:**
Shapely 2.0 dùng GEOS binary (DLL). PySide6 dùng Qt DLL. PyInstaller phải collect đủ cả hai bộ DLL vào bundle. Xung đột phổ biến: `geos_c.dll` không được include, PySide6 plugin không được copy. Kinh nghiệm: dùng `--onedir` mode (không `--onefile`) để giảm antivirus false positive và dễ debug.

In scope:
- Tạo `src/ui/main_window.py` — PySide6 QMainWindow đơn giản (empty window với title "RoomQS")
- Tạo `src/main.py` — entry point, import Shapely và thử tạo 1 Polygon cơ bản
- Viết `packaging/roomqs.spec` cho PyInstaller
- Build `--onedir` trên máy Dev-A
- Copy dist/ ra máy Windows sạch (không cài Python/Shapely), chạy .exe verify
- Nếu DLL conflict: thử các fix theo thứ tự: (1) hook Shapely explicit, (2) `--collect-all shapely`, (3) onefile mode

Out of scope:
- Bất kỳ feature nào trong UI (chỉ cần cửa sổ mở được)
- Bundle LISP files (Sprint 6)
- Code signing (Sprint 6 / Phase 2)

Story IDs: US-OPS-001
Acceptance Criteria IDs: AC từ US-OPS-001 + Exit Criteria Sprint 1

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: File .exe (hoặc thư mục --onedir) build thành công không báo lỗi PyInstaller
- AC-02: .exe mở được trên máy Windows 10/11 không cài Python — **hard gate Sprint 1**
- AC-03: Giao diện PySide6 (cửa sổ trống) hiện ra trong ≤ 5 giây
- AC-04: Shapely import không lỗi (thử `from shapely.geometry import Polygon; Polygon([(0,0),(1,0),(1,1)])`)
- AC-05: Kết quả test (pass/fail + lý do nếu fail) được ghi vào `packaging/test-results.md`

Module boundary:
- `src/ui/main_window.py` — Presentation Layer (chỉ UI shell)
- `src/main.py` — entry point
- `packaging/roomqs.spec` — build config

Files/Modules dự kiến bị ảnh hưởng:
- `src/ui/__init__.py`, `src/ui/main_window.py` (tạo mới)
- `src/main.py` (tạo mới)
- `packaging/roomqs.spec` (tạo mới)
- `packaging/test-results.md` (ghi chú kết quả)

Doc refs:
- /docs/06-Setup-Moi-Truong-Trien-Khai.md#2.5 Dependencies chính
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 1 — Rủi ro chính + Mitigation
- /docs/02-PRD-Product-Backlog.md#Rủi ro packaging / deployment

Dependencies: T1-01 (CI pass), T0-03 (repo structure)

Known risks:
- DLL conflict Shapely + PySide6 → buffer 3 ngày theo kế hoạch; nếu fail sau 3 ngày → escalate Tech Lead
- Antivirus false positive trên .exe → ghi nhận; workaround: `--onedir` thay `--onefile`
- Máy test "sạch" cần chuẩn bị thực sự sạch (không có Python global)

Open ambiguities:
- PySide6 hay PyQt6? (Tài liệu 06 gợi ý tkinter là mặc định nhưng PRD/kiến trúc chọn PySide6 — cần Tech Lead confirm trước khi code)

Definition of Done:
- [ ] .exe build thành công
- [ ] Chạy được trên ít nhất 1 máy Windows không cài Python (có thể là máy Dev-A sau khi uninstall Python)
- [ ] packaging/test-results.md ghi kết quả
- [ ] PR merged vào develop sau khi CI pass

---

# TICKET CONTEXT PACK

Ticket: T1-03 — DXF Parser — đọc LINE/LWPOLYLINE theo layer
Người phụ trách: Dev-A
Mục tiêu: Module `cad_parser` đọc được các entity hình học (LINE, LWPOLYLINE) từ file DXF, lọc theo layer name, trả về data structure Python — với unit test pass trên file fixture.

**Bối cảnh kỹ thuật:**
ezdxf đọc DXF entities qua `doc.modelspace()`. LINE có `dxf.start`/`dxf.end`. LWPOLYLINE có `.get_points()`. Layer name cần match theo config.yaml (case-insensitive). Entity phải normalize đơn vị mm sau khi đọc (kết hợp với T1-05).

In scope:
- Module `src/cad_parser/dxf_reader.py`:
  - Hàm `read_dxf(filepath: str) -> ezdxf.document.Drawing`
  - Hàm `extract_lines(doc, layer_names: list[str]) -> list[LineEntity]`
  - Hàm `extract_polylines(doc, layer_names: list[str]) -> list[PolylineEntity]`
- Data class `LineEntity(start: tuple, end: tuple, layer: str)`
- Data class `PolylineEntity(points: list[tuple], layer: str, is_closed: bool)`
- Unit test: `tests/unit/test_dxf_reader.py` với DXF fixture

Out of scope:
- Đọc TEXT/MTEXT (T1-04)
- Đọc INSERT block cửa (BL-07 — Sprint 2)
- Normalize đơn vị (T1-05 — nhưng nên integrate sau khi T1-05 done)
- Lọc theo bounding box (Sprint 2 — US-INP-002)

Story IDs: US-INP-001
Acceptance Criteria IDs: US-INP-001 AC-01, AC-02

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01 (từ US-INP-001): Given file DXF hợp lệ có geometry, When đọc, Then trả về list entity với số lượng ≥ 1
- AC-02 (từ US-INP-001): Danh sách layer nhận diện được từ file DXF
- AC-03: `extract_lines()` trả về đúng số LINE entities từ fixture đã biết trước
- AC-04: `extract_polylines()` trả về đúng số LWPOLYLINE entities từ fixture
- AC-05: Entity từ layer không có trong filter bị loại trừ
- AC-06: File DXF bị corrupt → raise exception rõ ràng, không crash silently (US-INP-001 AC-04)
- AC-07: Unit test pass trong CI

Module boundary:
- `src/cad_parser/` — chỉ đọc, không xử lý geometry
- Không gọi Shapely (Shapely thuộc `src/geometry/`)
- Không gọi UI

Files/Modules dự kiến bị ảnh hưởng:
- `src/cad_parser/__init__.py`, `src/cad_parser/dxf_reader.py` (tạo mới)
- `src/cad_parser/models.py` — LineEntity, PolylineEntity data class
- `tests/unit/test_dxf_reader.py` (tạo mới)
- `tests/fixtures/sample_basic.dxf` (từ T1-06)

Doc refs:
- /docs/03-User-Stories.md#US-INP-001
- /docs/04-Kien-Truc-Tech-Stack.md#MOD-01: File Intake, MOD cad_parser
- /docs/02-PRD-Product-Backlog.md#FR-01, FR-03

Dependencies: T1-06 (fixture DXF cần có trước khi viết test); T1-05 (normalize đơn vị — integrate sau)

Known risks:
- ezdxf version ≥ 1.3 có breaking change API so với 0.x — verify API trước khi code
- DXF từ AutoCAD 2019+ có thể dùng entity type `LWPOLYLINE` hoặc `POLYLINE` (3D) — cần handle cả hai

Open ambiguities:
- MLINE (multi-line walls) trong bản vẽ thực có xảy ra không? (Cần xem file DXF thực để quyết định)

Definition of Done:
- [ ] `dxf_reader.py` có đủ 3 hàm trên
- [ ] Unit test pass với ≥ 2 fixture
- [ ] CI pass
- [ ] PR reviewed và merged

---

# TICKET CONTEXT PACK

Ticket: T1-04 — DXF Parser — đọc TEXT/MTEXT
Người phụ trách: Dev-A
Mục tiêu: Module `text_extractor` đọc được TEXT và MTEXT entities từ DXF, lấy nội dung text và vị trí insertion point, phục vụ việc gắn tên phòng vào Polygon ở Sprint 3.

**Bối cảnh kỹ thuật:**
TEXT entity có `dxf.text` và `dxf.insert` (tọa độ). MTEXT phức tạp hơn — text có thể chứa formatting codes (ví dụ: `{\fArial;PHONG NGU}`) cần strip. Vị trí cần normalize sang mm.

In scope:
- Module `src/text_extractor/text_reader.py`:
  - Hàm `extract_texts(doc, layer_names: list[str] = None) -> list[TextEntity]`
  - Strip MTEXT formatting codes (regex đơn giản: xóa `{...;` và `}`)
- Data class `TextEntity(content: str, position: tuple, layer: str)`
- Unit test với DXF fixture có cả TEXT và MTEXT

Out of scope:
- Gắn text vào Polygon (BL-15 — Sprint 3)
- Đọc attribute của INSERT block (BL-07 — Sprint 2)
- Xử lý text trên nhiều dòng phức tạp (chỉ cần lấy raw text, strip formatting)

Story IDs: US-ROOM-004 (gắn tên phòng — context)
Acceptance Criteria IDs: US-ROOM-004 AC (phần extract)

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: TEXT entity trả về `content` đúng và `position` là tuple (x, y) đã normalize mm
- AC-02: MTEXT entity trả về content đã strip formatting code (ví dụ: `"PHONG NGU"` không phải `"{\fArial;PHONG NGU}"`)
- AC-03: Layer filter hoạt động: chỉ trả về text từ layer chỉ định (nếu có)
- AC-04: File fixture có 5 text entity → trả về list 5 TextEntity đúng nội dung
- AC-05: Unit test pass trong CI

Module boundary:
- `src/text_extractor/` — chỉ extract, không làm spatial lookup
- Không gọi Shapely

Files/Modules dự kiến bị ảnh hưởng:
- `src/text_extractor/__init__.py`, `src/text_extractor/text_reader.py` (tạo mới)
- `src/text_extractor/models.py` — TextEntity
- `tests/unit/test_text_reader.py` (tạo mới)

Doc refs:
- /docs/03-User-Stories.md#US-ROOM-004
- /docs/02-PRD-Product-Backlog.md#FR-07
- /docs/04-Kien-Truc-Tech-Stack.md#Module Breakdown

Dependencies: T1-06 (fixture cần có TEXT/MTEXT entities); T1-03 (có thể dùng chung `read_dxf()`)

Known risks:
- MTEXT formatting phức tạp (font, color codes) → chỉ cần strip, không cần parse đầy đủ

Open ambiguities:
- Text phòng có thể nằm trên layer riêng hay cùng layer nội thất? (Cần xem file DXF thực)

Definition of Done:
- [ ] `text_reader.py` có hàm extract TEXT và MTEXT
- [ ] MTEXT formatting được strip
- [ ] Unit test pass
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T1-05 — Normalize đơn vị $INSUNITS → mm
Người phụ trách: Dev-A
Mục tiêu: Module `geometry/unit_normalizer.py` đọc header `$INSUNITS` từ DXF và trả về hệ số chuyển đổi sang mm, đảm bảo mọi tọa độ và độ dài trong Python runtime đều là mm.

**Bối cảnh kỹ thuật:**
DXF header `$INSUNITS` là integer. Map: 0=unitless, 1=inch×25.4, 2=feet×304.8, 4=mm×1.0, 5=cm×10, 6=m×1000. Nếu $INSUNITS=0 → hỏi user qua UI (MVP: default 1.0 và warning). Invariant bắt buộc: mọi float trong pipeline Python đều là mm.

In scope:
- Hàm `get_unit_factor(doc: Drawing) -> tuple[float, str]` → trả về (factor, unit_name)
- Hàm `normalize_point(pt: tuple, factor: float) -> tuple` → apply factor
- Warning khi $INSUNITS=0 (log + return mặc định 1.0)
- Unit test với mock doc có các $INSUNITS khác nhau

Out of scope:
- Hỏi user qua UI (UI chỉ display warning, logic ở đây)
- Xử lý mix đơn vị (EC-19 — out of MVP scope)

Story IDs: US-INP-001 (ngầm định trong FR-01)
Acceptance Criteria IDs: Dẫn xuất từ ADR-03

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: $INSUNITS=4 (mm) → factor = 1.0
- AC-02: $INSUNITS=6 (metres) → factor = 1000.0
- AC-03: $INSUNITS=1 (inches) → factor = 25.4
- AC-04: $INSUNITS=0 (unitless) → factor = 1.0 + log warning "Don vi ve khong xac dinh"
- AC-05: `normalize_point((1000.0, 2000.0), 1.0)` → `(1000.0, 2000.0)` (không đổi khi mm)
- AC-06: Unit test pass với mock DXF header

Module boundary:
- `src/geometry/unit_normalizer.py`
- Không phụ thuộc UI, không gọi I/O file

Files/Modules dự kiến bị ảnh hưởng:
- `src/geometry/__init__.py`, `src/geometry/unit_normalizer.py` (tạo mới)
- `tests/unit/test_unit_normalizer.py` (tạo mới)

Doc refs:
- /docs/04-Kien-Truc-Tech-Stack.md#ADR-03: Kiểm soát đơn vị đo
- /docs/03-User-Stories.md#EC-17, EC-18

Dependencies: Không có (module độc lập)

Known risks: Không có rủi ro cao — logic đơn giản và có thể test fully isolated

Open ambiguities: Không có

Definition of Done:
- [ ] `unit_normalizer.py` với đủ 2 hàm
- [ ] Unit test cover tất cả $INSUNITS values trong bảng
- [ ] CI pass

---

# TICKET CONTEXT PACK

Ticket: T1-06 — Chuẩn bị DXF test fixtures
Người phụ trách: QA / BA
Mục tiêu: Có đủ bộ fixture DXF để Dev-A viết unit test cho T1-03/T1-04/T1-05 và Sprint 2/3 sau này có thể dùng.

In scope:
- Fixture 1 (`simple_rooms.dxf`): bản vẽ synthetic có 3 phòng hình chữ nhật, layer tường "TUONG", text tên phòng "PHONG NGU" / "WC" / "PHONG KHACH", $INSUNITS=4 (mm)
- Fixture 2 (`real_sample.dxf`): file DXF thực từ Sprint 0 (nếu có) — không cần chỉnh sửa, chỉ lưu vào thư mục fixture
- Fixture 3 (`corrupt.dxf`): file DXF bị cắt bỏ giữa chừng để test error handling
- Tạo `tests/fixtures/README.md` mô tả nội dung từng fixture (số entity, layer, giá trị expected)

Out of scope:
- Tạo fixture phòng L-shape (Sprint 2 cần — nhưng QA tạo sau khi có sample DXF thực)
- Fixture với block cửa (Sprint 2 BL-07)

Story IDs: Không có story riêng — test infrastructure
Acceptance Criteria IDs: Dẫn xuất từ DoD chung

Acceptance Criteria (copy/tóm tắt chính xác):
- AC-01: `simple_rooms.dxf` có đúng entity count được document: ví dụ 12 LINE trên layer TUONG, 3 TEXT
- AC-02: File đọc được bằng `ezdxf.readfile()` không raise exception
- AC-03: `corrupt.dxf` raise `ezdxf.DXFError` khi đọc
- AC-04: `tests/fixtures/README.md` liệt kê tên file, số entity expected, layer names

Module boundary: `tests/fixtures/` — không chạm module src

Files/Modules dự kiến bị ảnh hưởng:
- `tests/fixtures/simple_rooms.dxf` (tạo mới bằng ezdxf script hoặc AutoCAD)
- `tests/fixtures/real_sample.dxf` (copy từ Sprint 0 nếu có)
- `tests/fixtures/corrupt.dxf` (tạo bằng cách cắt truncate file)
- `tests/fixtures/README.md`

Doc refs:
- /docs/03-User-Stories.md#US-INP-001 (Ghi chú QA)
- /docs/05-Ke-Hoach-Sprint-Release.md#Sprint 1 — BL-04

Dependencies: T0-01 (file DXF thực từ Sprint 0 nếu có)

Known risks:
- Nếu QA không có AutoCAD → tạo `simple_rooms.dxf` bằng script Python + ezdxf (đơn giản, không cần AutoCAD)

Open ambiguities:
- Fixture synthetic tạo bằng script hay bằng tay qua AutoCAD?

Definition of Done:
- [ ] 3 fixture files tồn tại trong `tests/fixtures/`
- [ ] README.md mô tả expected values đầy đủ
- [ ] Dev-A xác nhận có thể dùng fixture để viết test
