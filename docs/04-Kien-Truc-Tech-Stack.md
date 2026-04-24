# 04 — Kiến Trúc & Tech Stack

**Tên hệ thống:** RoomQS — Room Quantity Surveying Tool  
**Phiên bản tài liệu:** v1.0  
**Nguồn gốc:** Dẫn xuất từ SRS v1.0 + Techstack đã chốt + PRD v1.0  
**Đối tượng đọc:** Tech Lead · Backend Dev · AutoLISP Dev · QA Lead  
**Ngày:** _(cập nhật khi phát hành)_

---

## 1. Mục tiêu kiến trúc

### Kiến trúc phục vụ mục tiêu gì

Kiến trúc này phải giải quyết một bài toán có **hai layer kỹ thuật không đồng nhất**:

1. **Layer CAD (AutoLISP / AutoCAD COM):** Đọc và tương tác trực tiếp với môi trường bản vẽ — nơi duy nhất có thể gọi lệnh BPOLY, bắt điểm người dùng click, và tạo Polyline trực tiếp lên model space.
2. **Layer Python:** Xử lý dữ liệu hình học, tính toán khối lượng, xuất báo cáo — nơi có thư viện mạnh và khả năng test/debug tốt hơn LISP nhiều lần.

Kiến trúc phải cho phép hai layer này **phối hợp mà không bị coupled chặt**, để mỗi bên có thể test, phát triển và thay thế độc lập.

### Nguyên tắc kiến trúc

| Nguyên tắc | Diễn giải thực tế |
|---|---|
| **Separation of Concerns** | AutoLISP chỉ làm "cánh tay CAD"; Python làm "bộ não" xử lý |
| **DXF-first** | Dữ liệu từ bản vẽ được đọc qua DXF/JSON trung gian, không phụ thuộc COM khi có thể |
| **Determinism** | Cùng đầu vào → cùng đầu ra; không dùng state toàn cục, không side effect ẩn |
| **Fail loudly, not silently** | Dữ liệu xấu phải sinh ra warning cụ thể, không âm thầm cho kết quả sai |
| **Testability first** | Domain logic (tính toán, geometry) phải unit-testable hoàn toàn, không phụ thuộc UI hay file system |
| **Single Responsibility** | Mỗi module có một lý do thay đổi duy nhất |
| **Config over hard-code** | Layer name, chiều dày tường tiêu chuẩn, hệ số tính toán phải đặt trong config, không hard-code |

### Non-functional drivers chính

Từ SRS, các NFR sau là **architecture drivers** — tức là ảnh hưởng trực tiếp đến quyết định thiết kế:

- **NFR-03 (Truy vết được):** Mọi kết quả phải gắn được về room_id → cần immutable data pipeline, không mutate object qua nhiều bước.
- **NFR-04 (Nhất quán / Deterministic):** Cùng file DXF + cùng config → cùng output. Cấm dùng random, cấm phụ thuộc thứ tự dict không xác định.
- **NFR-07 (Chịu lỗi có kiểm soát):** Phải phân biệt "phòng lỗi, bỏ qua phòng này" vs "file lỗi, dừng toàn bộ".
- **Deployment:** Đóng gói .exe Windows — ảnh hưởng đến cách import, bundle resource, và dependency management.

---

## 2. Kiến trúc tổng thể

### Mô hình kiến trúc: Layered Architecture + File-based Integration

Đây là desktop app xử lý batch, không phải real-time service. Mô hình phù hợp nhất là **Layered Architecture** kết hợp **File-based Integration** cho điểm giao giữa AutoLISP và Python.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│          PySide6 Desktop UI (Workflow Orchestrator)         │
│   Form nhập params · Progress log · Preview table · Export  │
└───────────────────────────┬─────────────────────────────────┘
                            │ calls
┌───────────────────────────▼─────────────────────────────────┐
│                   APPLICATION LAYER                         │
│              Pipeline Orchestrator (Python)                 │
│  Điều phối thứ tự: parse → recognize → map → calc → export │
└──────┬──────────┬──────────┬───────────┬────────────────────┘
       │          │          │           │
┌──────▼──┐ ┌────▼────┐ ┌───▼───┐ ┌────▼──────┐
│  FILE   │ │  CAD    │ │DOMAIN │ │  EXPORT   │
│ INTAKE  │ │ PARSER  │ │ENGINE │ │  ENGINE   │
│ MODULE  │ │ MODULE  │ │       │ │           │
└──────┬──┘ └────┬────┘ └───┬───┘ └────┬──────┘
       │         │           │          │
┌──────▼─────────▼───────────▼──────────▼──────┐
│               INFRASTRUCTURE LAYER            │
│  File I/O · ezdxf · openpyxl · JSON bridge   │
│  Config loader · Logger · Audit trail        │
└──────────────────────────────────────────────┘

══════════════════════════════════════════════
       FILE-BASED INTEGRATION BOUNDARY
══════════════════════════════════════════════

┌──────────────────────────────────────────────┐
│           AUTOCAD / AUTOLISP LAYER           │
│  Lệnh XR · Lệnh GB · Door Sealing           │
│  BPOLY execution · Polyline generation       │
│  Ghi output.json (room boundaries)           │
└──────────────────────────────────────────────┘
```

### Mô tả các layer

**Presentation Layer (PySide6):**
Chỉ làm một việc: nhận input từ người dùng và hiển thị output. Không chứa business logic. Giao tiếp với Application Layer thông qua signals/slots hoặc callback.

**Application Layer (Pipeline Orchestrator):**
Điều phối thứ tự các bước xử lý. Biết "bước nào chạy sau bước nào" nhưng không biết "bước đó làm thế nào". Mỗi bước là một module độc lập được inject vào.

**Domain Engine:**
Toàn bộ business logic: nhận diện phòng từ geometry, gán cửa vào phòng, tính toán khối lượng theo BR-04/05/06. Đây là phần **không phụ thuộc vào AutoCAD, DXF, hay Excel** — chỉ nhận Python data structures và trả về Python data structures. Toàn bộ unit test tập trung tại đây.

**Infrastructure Layer:**
Tất cả I/O: đọc DXF bằng ezdxf, ghi Excel bằng openpyxl, đọc/ghi JSON, load config YAML. Có thể mock hoàn toàn trong unit test.

**AutoCAD/AutoLISP Layer:**
Tách biệt hoàn toàn khỏi Python runtime. Giao tiếp qua file JSON trung gian. Python không gọi AutoCAD trực tiếp trong luồng chính (trừ khi dùng pyautocad cho advanced integration ở Phase 2).

### Vì sao mô hình này phù hợp với DXF-first

AutoCAD và Python chạy trên hai runtime khác nhau. File JSON trung gian là **single source of truth** cho dữ liệu phòng — không bị phụ thuộc vào version AutoCAD, không bị lỗi khi AutoCAD bận. Python có thể chạy toàn bộ pipeline từ DXF + JSON mà không cần AutoCAD đang mở, giúp test tự động dễ dàng.

---

## 3. Tech Stack đã chọn

### Bảng vai trò từng thành phần

| Thành phần | Version | Vai trò trong hệ thống | Module sử dụng |
|---|---|---|---|
| **Python** | 3.12+ | Runtime chính cho toàn bộ application | Tất cả |
| **ezdxf** | ≥ 1.3 | Đọc file DXF: entities, layers, attributes, text blocks | `cad_parser` |
| **Shapely** | ≥ 2.0 | Tính toán geometry 2D: Polygon area/perimeter/edges, spatial containment, intersection | `geometry_engine`, `door_mapper`, `calc_engine` |
| **pandas** | ≥ 2.1 | Tổng hợp dữ liệu dạng bảng, chuẩn bị data frame trước khi ghi Excel | `export_engine` |
| **openpyxl** | ≥ 3.1 | Ghi file Excel multi-sheet, format cells, merge cells | `export_engine` |
| **PySide6** | ≥ 6.6 | Giao diện desktop: form, progress log, preview table, file picker | `ui` |
| **pytest** | ≥ 7.4 | Unit test cho domain engine và business rules | `tests/` |
| **PyInstaller** | ≥ 6.0 | Đóng gói .exe Windows (onefolder hoặc onefile) | `packaging/` |
| **AutoLISP / Visual LISP** | AutoCAD 2019+ | Tương tác CAD: BPOLY, bắt điểm click, ghi JSON phòng | `lisp/` |
| **pyautocad** | ≥ 0.2 | (Optional / Phase 2) COM automation cho advanced AutoCAD interaction | `cad_bridge` (Phase 2) |

### Dev-only additions (không bundle vào .exe)

| Thành phần | Mục đích |
|---|---|
| **matplotlib** | Debug/preview geometry trong IDE — vẽ Polygon để kiểm tra boundary đúng chưa |
| **numpy** | Tính toán vector trong thuật toán Gross-Overlap (cross product, dot product) nếu Shapely không đủ |
| **PyYAML** | Đọc file config `.yaml` cho layer names và business rule params |
| **rich** | Logging màu sắc trong terminal khi debug pipeline |

> **Lưu ý quan trọng:** ezdxf và Shapely là hai thư viện xử lý hình học — nhưng **chúng không tự nhận diện phòng**. ezdxf đọc ra các LINE/LWPOLYLINE entities rời rạc. Shapely tính toán geometry trên Polygon đã được tạo sẵn. Việc **biến các đường LINE rời thành Polygon khép kín** là bài toán engineering riêng, phải được giải quyết bởi module `room_recognition_engine` với sự hỗ trợ của AutoLISP (BPOLY).

---

## 4. Quyết định kiến trúc chính

### ADR-01: Desktop app thay vì web app hoặc AutoCAD plugin thuần túy

**Quyết định:** Python desktop app (PySide6 .exe) + AutoLISP plugin.

**Lý do:**
- Người dùng làm việc với file cục bộ, không cần server.
- AutoCAD là môi trường bắt buộc để gọi BPOLY — nhưng **toàn bộ logic tính toán không nên nằm trong LISP** vì LISP không có unit test framework, không có pandas/Shapely, và debugging khó.
- Plugin AutoCAD thuần (không có Python) sẽ phải viết toàn bộ bài toán geometry trong LISP — không khả thi với bộ tính toán ma trận và xuất Excel.
- Web app yêu cầu backend server, không phù hợp với môi trường làm việc offline điển hình của QS.

**Trade-off chấp nhận:** Người dùng phải có AutoCAD để chạy phần LISP. Không chạy được trên máy không có AutoCAD.

---

### ADR-02: DXF-first, không dùng DWG trực tiếp

**Quyết định:** Yêu cầu user export DXF từ AutoCAD trước khi dùng Python parser. LISP module sẽ hỗ trợ export tự động nếu cần.

**Lý do:**
- DWG là định dạng proprietary, không có thư viện Python open-source đọc đáng tin cậy.
- ezdxf đọc DXF rất mature và stable.
- DXF 2013 (AC1027) là chuẩn an toàn nhất — support rộng từ AutoCAD 2014 trở lên.

**Xử lý DWG:** AutoLISP sẽ cung cấp lệnh trợ giúp export DXF (`(command "DXFOUT" filename "16" "")`) hoặc user export thủ công qua AutoCAD menu. Python sẽ không xử lý DWG.

**Config:** Dùng DXF version `R2013` (AC1027) làm chuẩn. Ghi rõ trong Quick Guide.

---

### ADR-03: Kiểm soát đơn vị đo

**Quyết định:** Normalize tất cả về **milimét (mm)** ngay tại bước đọc DXF, trước khi đưa vào bất kỳ module nào.

**Cơ chế:**
1. Đọc header DXF `$INSUNITS` — xác định đơn vị gốc.
2. Map sang hệ số chuyển đổi về mm:

| `$INSUNITS` | Đơn vị | Hệ số → mm |
|---|---|---|
| 0 | Unitless | Hỏi user, default = 1.0 (tức là đã là mm) |
| 1 | Inches | 25.4 |
| 2 | Feet | 304.8 |
| 4 | **mm** (phổ biến nhất) | **1.0** |
| 5 | Centimetres | 10.0 |
| 6 | Metres | 1000.0 |

3. Khi xuất Excel, chuyển sang m² / m (chia 1,000,000 cho area, chia 1,000 cho length).

**Invariant:** Mọi coordinate và length trong Python runtime đều là mm (float). Không có exception.

---

### ADR-04: Quản lý cấu hình rule nghiệp vụ

**Quyết định:** Config được lưu trong file `config.yaml` bên cạnh .exe. Không hard-code bất kỳ giá trị nghiệp vụ nào.

**Các param cần config:**

```yaml
# config.yaml
cad:
  dxf_version: "R2013"
  wall_layer_names: ["TUONG", "A-WALL", "WALL", "Tuong"]   # match không phân biệt hoa thường
  door_block_prefixes: ["D", "DW", "S", "CK"]              # prefix mã cửa
  short_segment_threshold_mm: 300.0                         # lọc rác < 300mm trong GB
  standard_wall_thicknesses_mm: [100, 110, 200, 220]       # dùng trong thuật toán XR

calculation:
  default_floor_height_mm: 2800.0                          # chiều cao thông thủy mặc định
  default_wall_thickness_mm: 200.0
  floor_finish_factor: 1.0                                  # hệ số nhân diện tích sàn
  geometry_tolerance_mm: 5.0                                # fuzz tolerance cho parallel/coincident check
  overlap_min_length_mm: 50.0                               # tường chung ngắn hơn ngưỡng này bị bỏ qua

export:
  output_dir: "./output"
  decimal_places: 2
  sheet_names:
    rooms: "Du lieu Phong"
    doors: "Du lieu Cua"
    edges: "Canh Phong"
```

**Rule:** Không cho phép user sửa config.yaml trong UI ở MVP. UI chỉ override `floor_height` và `wall_thickness` cho từng job.

---

### ADR-05: Đảm bảo tính deterministic

**Quyết định:** Pipeline xử lý theo thứ tự deterministic — không dùng set, không dùng dict iteration nếu thứ tự quan trọng.

**Cơ chế:**
- Room list được sắp xếp theo `(centroid_x, centroid_y)` sau khi recognize.
- Door list sắp xếp theo `door_code` alphabetically.
- Edge list per room sắp xếp theo thứ tự vertex của Polyline (giữ nguyên từ LISP).
- Tất cả intermediate results được log với timestamp và input hash để truy vết khi cần.

---

## 5. Module Breakdown

### Module map tổng thể

```
src/
├── intake/           # File intake & validation
├── cad_parser/       # DXF parsing
├── geometry/         # Normalization & Shapely utilities
├── room_engine/      # Room recognition & boundary management
├── door_engine/      # Door detection & room mapping
├── text_extractor/   # Text/tag extraction từ DXF
├── calc_engine/      # Quantity calculation (domain core)
├── validation/       # Warning & validation engine
├── export/           # Excel export
├── ui/               # PySide6 UI
├── pipeline/         # Orchestrator
├── config/           # Config loader
└── utils/            # Logging, audit, shared helpers

lisp/
├── xr.lsp            # Thuật toán Tia X-quang
├── gb.lsp            # Ghost Boundary
└── export_rooms.lsp  # Ghi output.json

tests/
```

---

### MOD-01: File Intake

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Tiếp nhận và validate sơ bộ file đầu vào trước khi parse |
| **Input** | File path (DXF), door Excel path (optional), config params từ UI |
| **Output** | `IntakeResult` gồm validated file paths, detected DXF version, unit factor |
| **Trách nhiệm** | Kiểm tra file tồn tại, đúng định dạng, đọc được; detect `$INSUNITS`; kiểm tra DXF version tối thiểu |
| **Dependency** | config loader, ezdxf (header-only read) |
| **Rủi ro** | File DXF bị corrupt hoặc từ phần mềm không phải AutoCAD (BricsCAD, QCAD) → cần test |

---

### MOD-02: CAD Parser

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Trích xuất entities liên quan từ DXF thành Python data structures |
| **Input** | DXF file path, layer config (wall layers, door block prefixes), unit factor |
| **Output** | `RawCADData`: `wall_segments: List[Segment]`, `text_entities: List[TextEntity]`, `door_blocks: List[DoorBlock]` |
| **Trách nhiệm** | Lọc entities theo layer; đọc LINE/LWPOLYLINE từ wall layers; đọc TEXT/MTEXT bất kể layer; đọc INSERT với attributes khớp door_block_prefixes; apply unit factor vào tất cả coordinates |
| **Dependency** | ezdxf, MOD-01, config |
| **Rủi ro** | MTEXT có formatting codes (`\P`, `\f{}`) cần strip trước khi so khớp; block INSERT lồng nhau (nested blocks) cần xử lý riêng |

---

### MOD-03: Geometry Normalization

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Chuẩn hóa tọa độ và geometry data trước khi đưa vào engine |
| **Input** | `RawCADData` từ MOD-02 hoặc room JSON từ LISP |
| **Output** | `NormalizedGeometry`: Shapely objects, đơn vị đã chuẩn, coordinate precision đã round |
| **Trách nhiệm** | Round coordinates về 4 chữ số thập phân (tránh floating point chaos); tạo Shapely `LineString` cho wall segments; tạo Shapely `Polygon` từ LISP Polyline coords; validate `Polygon.is_valid`; auto-fix bằng `buffer(0)` nếu polygon invalid nhẹ |
| **Dependency** | Shapely, MOD-02 |
| **Rủi ro** | Polygon self-intersection từ LISP output → `buffer(0)` fix hầu hết nhưng không phải tất cả; cần log cảnh báo khi phải auto-fix |

---

### MOD-04: Room Recognition Engine

> ⚠️ **Module khó nhất trong hệ thống.** Phần lớn "magic" nằm ở AutoLISP, không phải Python.

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Tạo tập hợp Room objects với Polygon hợp lệ, tên/mã phòng |
| **Input** | `room_boundaries.json` từ LISP (tọa độ Polyline mỗi phòng) + `NormalizedGeometry.text_entities` |
| **Output** | `List[RoomCandidate]`: mỗi item có `polygon: Polygon`, `room_code: str | None`, `room_name: str | None` |
| **Trách nhiệm** | Đọc JSON từ LISP; tạo Shapely Polygon; loại bỏ duplicate (overlap > 95% → coi là trùng); gắn text vào phòng (point-in-polygon lookup); validate mỗi phòng có polygon hợp lệ |
| **Dependency** | MOD-03, text_extractor (MOD-06), config |
| **Rủi ro** | JSON thiếu phòng nếu user bỏ sót click; polygon invalid nếu LISP tạo polyline chéo |

**Quy tắc loại duplicate:**
```
Nếu polygon_A.intersection(polygon_B).area / min(A.area, B.area) > 0.95
→ Giữ polygon có area lớn hơn, log warning "phòng trùng bị loại bỏ"
```

---

### MOD-05: Door Detection & Mapping Engine

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Nhận diện cửa từ DXF, bổ sung từ Excel, gán cửa vào phòng |
| **Input** | `RawCADData.door_blocks` + optional Excel door list + `List[Room]` (đã có polygon) |
| **Output** | `List[Door]` với `related_room_a`, `related_room_b`; cập nhật `Room.related_doors` |
| **Trách nhiệm** | Tạo Door objects từ block attributes; merge với Excel door list nếu có; spatial lookup: với mỗi door position, kiểm tra `polygon.contains(Point(x,y))` hoặc `polygon.distance(Point(x,y)) < tolerance`; phát hiện cửa ranh giới chung |
| **Dependency** | Shapely, MOD-04, pandas (đọc Excel), config |
| **Rủi ro** | Block position không nằm chính xác trong phòng (offset nhỏ) → cần tolerance buffer; cửa nằm ở góc tường có thể gán sai phòng |

**Cơ chế phát hiện cửa ranh giới chung:**
```
Với mỗi door D tại position P:
1. Tìm tất cả phòng R mà R.polygon.distance(P) < BOUNDARY_TOLERANCE (≈ wall_thickness / 2)
2. Nếu chỉ 1 phòng → related_room_a = phòng đó
3. Nếu 2 phòng → related_room_a = phòng gần hơn, related_room_b = phòng còn lại → cờ is_shared_boundary = True
4. Nếu 0 phòng → ValidationIssue(severity=WARNING, "Cửa không gán được vào phòng nào")
```

---

### MOD-06: Text / Tag Extractor

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Trích xuất và phân loại text entities từ DXF |
| **Input** | `RawCADData.text_entities` |
| **Output** | `List[TextTag]`: `{content: str, position: Point, layer: str, height: float}` |
| **Trách nhiệm** | Strip MTEXT formatting codes; normalize whitespace; không phân loại "tên phòng" vs "mã phòng" tại đây (để MOD-04 làm qua point-in-polygon lookup) |
| **Dependency** | MOD-02 |
| **Rủi ro** | Text trùng vị trí (stacked text trong AutoCAD) — lấy text có height cao nhất làm ưu tiên |

---

### MOD-07: Quantity Calculation Engine

> **Core domain logic. 100% phải có unit test. Không phụ thuộc vào bất kỳ I/O nào.**

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Tính toán tất cả số liệu khối lượng cho từng phòng theo BR-04/05/06 |
| **Input** | `List[Room]` (đã có polygon, cửa), `JobParams` (H, t) |
| **Output** | `List[Room]` với đầy đủ: `area`, `perimeter`, `edge_list`, `floor_finish_qty`, `wall_finish_qty`, `total_door_area` |
| **Trách nhiệm** | Tính area (m²) và perimeter (m) từ Shapely; trích xuất edge list từ exterior.coords; tính floor_finish theo BR-04; tính wall_finish theo BR-05 (trừ door area); xử lý BR-06 cho cửa ranh giới chung |
| **Dependency** | Shapely, MOD-04, MOD-05 |
| **Rủi ro** | BR-06 phức tạp — xem chi tiết tại Section 7 |

**Công thức tính toán chính (từ SRS):**

```
floor_finish_qty (m²)  = room.area × floor_finish_factor

wall_finish_qty (m²)   = (room.perimeter × H)
                         − Σ(door.area for door in single_room_doors)
                         − Σ(door.area × 2 for door in shared_boundary_doors
                              where both_rooms_in_scope)
                         − Σ(door.area × 1 for door in shared_boundary_doors
                              where only_this_room_in_scope)
```

---

### MOD-08: Validation & Warning Engine

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Phát hiện và ghi lại mọi vấn đề dữ liệu; không dừng pipeline trừ lỗi critical |
| **Input** | State của pipeline tại mỗi bước |
| **Output** | `List[ValidationIssue]` |
| **Trách nhiệm** | Validate từng BR; kiểm tra room có polygon hợp lệ (BR-01); kiểm tra door có data tối thiểu (BR-02); cảnh báo phòng không có tên/mã; cảnh báo cửa không gán được phòng; cảnh báo diện tích âm hoặc bất thường |
| **Dependency** | Mọi module domain |
| **Rủi ro** | Nếu validation quá nghiêm ngặt (fail-fast cho mọi warning) sẽ làm pipeline không chạy được với bản vẽ thực tế thường xuyên có vài entity lỗi |

**Phân loại severity (xem thêm Section 10):**

| Severity | Hành vi | Ví dụ |
|---|---|---|
| `CRITICAL` | Dừng pipeline ngay | DXF không đọc được; không có phòng nào |
| `ERROR` | Bỏ qua entity lỗi, tiếp tục | Phòng không có polygon hợp lệ |
| `WARNING` | Ghi log, tiếp tục | Phòng không có tên/mã; cửa không gán được phòng |
| `INFO` | Ghi log, không hiển thị UI | Phòng trùng bị loại bỏ; auto-fix polygon |

---

### MOD-09: Report Export Engine

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Xuất file Excel multi-sheet từ processed data |
| **Input** | `List[Room]`, `List[Door]`, `ExportConfig` |
| **Output** | File `.xlsx` tại `output_dir` |
| **Trách nhiệm** | Tạo DataFrame cho từng sheet (phòng/cửa/cạnh); format header; merge cells; set column width; round số; ghi file |
| **Dependency** | pandas, openpyxl |
| **Rủi ro** | openpyxl merge cell có thể conflict với frozen panes; test trên Excel thực |

---

### MOD-10: UI / Workflow Orchestration

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Giao diện người dùng và điều phối pipeline |
| **Input** | User actions (button clicks, form inputs) |
| **Output** | Hiển thị log, progress, preview table; trigger export |
| **Trách nhiệm** | Form nhập params; file picker cho DXF và door Excel; nút chạy pipeline (chạy trong QThread để không block UI); log panel real-time; preview table Room list; nút xuất Excel |
| **Dependency** | PySide6, MOD-pipeline |
| **Rủi ro** | Pipeline phải chạy trong QThread — không được call UI từ worker thread |

---

### MOD-11: Pipeline Orchestrator

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Điều phối thứ tự các bước xử lý, truyền state giữa modules |
| **Input** | `JobParams` từ UI |
| **Output** | `PipelineResult` chứa rooms, doors, issues, status |
| **Trách nhiệm** | Khởi tạo và gọi từng module theo thứ tự; truyền output của bước trước làm input bước sau; emit signals về progress cho UI; bắt exception tại mỗi bước và chuyển thành `ValidationIssue` nếu recoverable |
| **Dependency** | Tất cả modules domain |
| **Rủi ro** | Lỗi exception không được handle đúng sẽ crash UI thread |

---

### MOD-12: Config & Logging

| Trường | Nội dung |
|---|---|
| **Mục tiêu** | Load config, provide logger, ghi audit trail |
| **Input** | `config.yaml` file path |
| **Output** | `Config` object (singleton), `Logger` |
| **Trách nhiệm** | Parse YAML; validate required keys; provide typed config access; setup file logger + console logger; ghi job audit log (input hash, timestamp, counts) |
| **Dependency** | PyYAML |
| **Rủi ro** | Config missing key → cần clear error message, không để KeyError crash tại runtime |

---

## 6. Business Flow / Processing Flow

```
USER
 │
 ▼
[1] CHỌN FILE & NHẬP PARAMS (UI Form)
    ├── DXF file path
    ├── Door Excel path (optional)
    ├── Floor height H (mm)
    ├── Wall thickness t (mm)
    └── Layer config (nếu cần override)
 │
 ▼
[2] FILE INTAKE & VALIDATION (MOD-01)
    ├── Kiểm tra file tồn tại và đọc được
    ├── Detect $INSUNITS → unit_factor
    └── CRITICAL nếu không đọc được → Dừng, hiện lỗi
 │
 ▼
[3] CAD PARSE (MOD-02)
    ├── Đọc wall segments từ wall layers
    ├── Đọc text entities (tất cả layers)
    └── Đọc door INSERT blocks
 │
 ▼
[4] GEOMETRY NORMALIZATION (MOD-03)
    ├── Apply unit_factor → tất cả coords thành mm
    ├── Round tọa độ 4 chữ số
    └── Tạo Shapely LineString cho wall segments
 │
 ▼
[5] LOAD ROOM BOUNDARIES TỪ LISP OUTPUT
    ├── Đọc room_boundaries.json (đã được LISP ghi trước)
    ├── Tạo Shapely Polygon cho mỗi phòng
    ├── Validate is_valid; auto-fix buffer(0) nếu cần
    └── ERROR nếu 0 phòng hợp lệ → Dừng với cảnh báo
 │
 ▼
[6] GẮN TEXT VÀO PHÒNG (MOD-04 + MOD-06)
    ├── Point-in-polygon lookup: text_position ∈ polygon?
    ├── Gắn room_name và room_code
    └── WARNING nếu phòng không có text
 │
 ▼
[7] LOẠI BỎ PHÒNG TRÙNG (MOD-04)
    └── Overlap > 95% → giữ lớn hơn, log WARNING
 │
 ▼
[8] DOOR DETECTION & MAPPING (MOD-05)
    ├── Tạo Door objects từ block attributes
    ├── Merge door data từ Excel nếu có
    ├── Spatial assignment: door → room(s)
    ├── Flag is_shared_boundary nếu thuộc 2 phòng
    └── WARNING nếu cửa không gán được phòng
 │
 ▼
[9] QUANTITY CALCULATION (MOD-07)
    ├── area, perimeter, edge_list cho mỗi phòng
    ├── floor_finish_qty (BR-04)
    ├── wall_finish_qty (BR-05, trừ cửa)
    └── Áp dụng BR-06 cho shared boundary doors
 │
 ▼
[10] VALIDATION FINAL (MOD-08)
    ├── Kiểm tra business rules toàn bộ
    ├── Compile toàn bộ ValidationIssue list
    └── Phân loại và sort theo severity
 │
 ▼
[11] HIỂN THỊ KẾT QUẢ & CẢNH BÁO (UI)
    ├── Preview table: rooms với area, perimeter, door count
    ├── Warning panel: liệt kê toàn bộ issues
    └── Cho phép user review trước khi export
 │
 ▼
[12] EXPORT EXCEL (MOD-09) — khi user click "Xuất"
    ├── Sheet "Du lieu Phong" (FR-19)
    ├── Sheet "Du lieu Cua" (FR-20)
    └── Sheet "Canh Phong" (FR-21)
 │
 ▼
[13] MỞ FILE EXCEL (UI)
     └── os.startfile(output_path) trên Windows
```

---

## 7. Thuật toán / Strategy cho các bài toán khó

### 7.1. Room Boundary Recognition

**Vấn đề:** ezdxf trả về hàng nghìn LINE/LWPOLYLINE entities rời rạc từ bản vẽ. Không có API nào tự động gom chúng thành Polygon phòng.

**Giải pháp chốt: AutoLISP-first với 2 thuật toán**

**Thuật toán XR (X-Ray — phòng vuông vức):**
1. User click 1 điểm P bên trong phòng.
2. LISP bắn 4 tia từ P theo OX+, OX−, OY+, OY−.
3. Với mỗi tia: `ssget "F"` lọc chỉ LINE/LWPOLYLINE từ wall layers.
4. Sort các giao điểm theo khoảng cách từ P → từ gần đến xa.
5. Duyệt cặp giao điểm liên tiếp: nếu khoảng cách ≈ một trong `standard_wall_thicknesses` (fuzz 5mm) → đây là cặp mép tường. Lấy mép gần P hơn làm "mép trong".
6. Tính giao điểm của 4 mép trong bằng hàm `inters` → 4 đỉnh góc.
7. Vẽ LWPOLYLINE đỏ, closed, lineweight 0.4mm.

**Giới hạn XR:** Chỉ đúng với phòng hình chữ nhật hoặc gần vuông vức. Phòng L-shape, đa giác → dùng GB.

**Thuật toán GB (Ghost Boundary — phòng phức tạp):**
1. User quét cửa sổ chọn vùng chứa phòng (chấp nhận chọn cả rác).
2. LISP lọc: chỉ giữ LINE/LWPOLYLINE có length > `short_segment_threshold` (300mm).
3. LISP gọi `-BOUNDARY` với Boundary Set là tập vừa lọc (lệnh `"A" "S" ss_clean "" "N" "O" "P" ""`).
4. AutoCAD tự tính ra LWPOLYLINE khép kín từ các nét tường.
5. LISP validate kết quả là LWPOLYLINE, gắn màu đỏ và lineweight.

**Xử lý bản vẽ "bẩn":** GB lọc `length < 300mm` loại bỏ được nét hatch ký hiệu, dim tick, text leader ngắn. Nội thất (giường, tủ) thường là block INSERT, không phải LINE → không ảnh hưởng đến ssget lọc LINE.

**Door Sealing** (cần thiết trước khi chạy BPOLY):
1. LISP tìm tất cả INSERT block cửa trên đường biên phòng.
2. Lấy 2 điểm mép cửa (từ block size và insertion point).
3. Vẽ LINE tạm nối kín khoảng hở.
4. Chạy BPOLY.
5. Xóa LINE tạm.

**Ghi JSON từ LISP:**
```lisp
;; Sau khi có tất cả Polyline phòng, ghi ra JSON
;; Format: [{"room_index": 0, "vertices": [[x1,y1],[x2,y2],...]}]
```
Python đọc JSON này và tạo Shapely Polygon.

---

### 7.2. Wall-to-Polygon / Closed Boundary Inference (Python-side fallback)

**Khi nào cần:** Nếu không có AutoCAD (test environment, batch processing DXF-only), Python cần tự tạo Polygon từ wall segments.

**Strategy:** Đây là bài toán khó — không giải triệt để trong MVP. Fallback strategy:
1. Lấy `wall_segments` từ MOD-02.
2. Dùng Shapely `ops.unary_union` để merge các LineString có điểm chung.
3. Dùng `polygonize` từ Shapely để tìm Polygon từ network of lines.
4. Filter Polygon có area > threshold (loại bỏ polygon nhỏ do rác).

**Giới hạn:** `polygonize` chỉ hoạt động tốt nếu wall network thực sự kín. Bản vẽ thực có hở tại cửa → sẽ thất bại. Do đó, luồng chính vẫn phải qua AutoLISP. Python fallback chỉ dùng cho development/testing.

---

### 7.3. Gắn Text vào Room Polygon

**Algorithm:**
```
FOR EACH text_entity IN text_entities:
    point = Point(text_entity.position.x, text_entity.position.y)
    FOR EACH room IN rooms:
        IF room.polygon.contains(point):
            candidates[room].append(text_entity.content)
            BREAK  # một text chỉ thuộc 1 phòng

FOR EACH room:
    texts = candidates.get(room, [])
    room.room_code = classify_as_code(texts)   # pattern matching: chữ+số, ngắn
    room.room_name = classify_as_name(texts)   # còn lại
```

**Phân biệt code vs name:**
- `room_code`: match regex `^[A-Z]{1,3}\d{1,3}$` (ví dụ: P01, WC, LR02).
- `room_name`: text có ít nhất 2 từ hoặc dài hơn 4 ký tự mà không match code pattern.
- Nếu có cả 2 loại text trong 1 phòng → lấy cả 2.
- Nếu chỉ có 1 text → gán vào `room_name`; `room_code` = None (log WARNING).

---

### 7.4. Xác định Cửa thuộc 1 hay 2 Phòng

```
door_position = Point(door.insertion_x, door.insertion_y)

matching_rooms = []
FOR EACH room IN rooms:
    # Kiểm tra contains (cửa bên trong phòng)
    IF room.polygon.contains(door_position):
        matching_rooms.append(room)
        CONTINUE
    
    # Kiểm tra distance (cửa sát biên)
    IF room.polygon.exterior.distance(door_position) < wall_thickness / 2:
        matching_rooms.append(room)

IF len(matching_rooms) == 0:
    → ValidationIssue WARNING "Cửa [code] không gán được phòng"
    
IF len(matching_rooms) == 1:
    door.related_room_a = matching_rooms[0]
    door.is_shared_boundary = False
    
IF len(matching_rooms) == 2:
    door.related_room_a = matching_rooms[0]
    door.related_room_b = matching_rooms[1]
    door.is_shared_boundary = True
    
IF len(matching_rooms) > 2:
    → ValidationIssue WARNING "Cửa [code] khớp > 2 phòng, kiểm tra geometry"
    door.related_room_a = matching_rooms[0]  # lấy phòng gần nhất
```

---

### 7.5. Xử lý Rule Cửa trên Ranh Giới Chung (BR-06)

**Bài toán:** Cửa C nằm giữa Phòng A và Phòng B. Khi tính `wall_finish_qty`:
- Phòng A: phải trừ diện tích mặt tường tại vị trí cửa C.
- Phòng B: phải trừ diện tích mặt tường tại vị trí cửa C.
- Không được trừ từ tường chung 2 lần khi tính tổng toàn mặt bằng.

**Implementation:**
```python
def calculate_wall_finish(room, job_params, all_rooms_in_scope):
    base = room.perimeter * job_params.floor_height
    
    for door in room.related_doors:
        if not door.is_shared_boundary:
            # BR-05: cửa đơn → trừ 1 lần
            base -= door.area
        else:
            # BR-06: cửa ranh giới chung
            # Luôn trừ phần diện tích của phía này
            base -= door.area
            # Nếu phòng kia cũng trong phạm vi → nó sẽ trừ lần nữa ở phía đó
            # Không cần làm thêm gì — mỗi phòng tự trừ phần của mình
    
    return base
```

**Lưu ý BR-06 về tường thô (V_xay):** Khi tính tổng toàn mặt bằng, cần trừ thêm `L_chung × H × t`. Công thức này áp dụng khi có yêu cầu tính khối xây tường thô — MVP chưa tính `V_xay` (chỉ tính diện tích tô trát bề mặt). **Ghi nhận để Phase 2.**

---

### 7.6. Xử lý Dữ liệu CAD Không Sạch

| Vấn đề | Cơ chế xử lý |
|---|---|
| Nét rác ngắn < 300mm | GB filter theo length threshold |
| Block nội thất (giường, tủ) | ssget lọc chỉ LINE/LWPOLYLINE; block là INSERT → bị lọc tự nhiên |
| Cửa làm hở biên tường | Door Sealing trong LISP |
| HATCH, DIM, LEADER | ssget filter theo entity type |
| Text chồng text (stacked) | Lấy text có height cao nhất tại cùng vị trí |
| Polygon self-intersecting | `Polygon.buffer(0)` auto-fix nhẹ; log INFO |
| Tọa độ float precision noise | Round 4 chữ số thập phân tại MOD-03 |
| MTEXT với format codes | Strip regex trước khi dùng: `re.sub(r'\\[^;]+;', '', text)` |

---

## 8. Data Model

### Entity: `Room`

| Field | Type | Ý nghĩa | Nguồn | Ràng buộc |
|---|---|---|---|---|
| `internal_room_id` | `str` (UUID) | ID nội bộ duy nhất | Auto-generated | NOT NULL, UNIQUE |
| `room_code` | `str \| None` | Mã phòng (VD: P01, WC) | Text từ DXF | Nullable; WARNING nếu None |
| `room_name` | `str \| None` | Tên phòng (VD: Phòng Ngủ) | Text từ DXF | Nullable; WARNING nếu None |
| `polygon` | `Shapely.Polygon` | Đường bao 2D của phòng | LISP JSON → Shapely | NOT NULL; is_valid == True |
| `area_mm2` | `float` | Diện tích (mm²) | Computed: polygon.area | > 0 |
| `area_m2` | `float` | Diện tích (m²) | area_mm2 / 1e6 | > 0 |
| `perimeter_mm` | `float` | Chu vi (mm) | Computed: polygon.length | > 0 |
| `perimeter_m` | `float` | Chu vi (m) | perimeter_mm / 1000 | > 0 |
| `edge_list` | `List[Edge]` | Danh sách cạnh | Extracted từ polygon.exterior.coords | len >= 3 |
| `applied_height_mm` | `float` | Chiều cao tính toán (mm) | JobParams hoặc override | > 0 |
| `related_doors` | `List[Door]` | Cửa liên quan | MOD-05 assignment | Có thể rỗng |
| `total_door_area_m2` | `float` | Tổng diện tích cửa | Σ door.area_m2 | >= 0 |
| `floor_finish_qty_m2` | `float` | Khối lượng hoàn thiện sàn | BR-04 | >= 0 |
| `wall_finish_qty_m2` | `float` | Khối lượng bề mặt tường | BR-05/06 | >= 0 |
| `source_polyline_vertices` | `List[Tuple[float,float]]` | Tọa độ gốc từ LISP | LISP JSON | NOT NULL; dùng để audit |
| `validation_issues` | `List[ValidationIssue]` | Issues gắn với phòng này | MOD-08 | Có thể rỗng |

---

### Entity: `Door`

| Field | Type | Ý nghĩa | Nguồn | Ràng buộc |
|---|---|---|---|---|
| `internal_door_id` | `str` (UUID) | ID nội bộ | Auto-generated | NOT NULL |
| `door_code` | `str` | Mã cửa (D1, DW, S2...) | Block attribute hoặc Excel | NOT NULL; BR-02 |
| `door_name` | `str \| None` | Tên cửa | Block attribute hoặc Excel | Nullable |
| `width_mm` | `float` | Chiều rộng (mm) | Block attribute hoặc Excel | > 0; BR-02 |
| `height_mm` | `float` | Chiều cao (mm) | Block attribute hoặc Excel | > 0; BR-02 |
| `area_m2` | `float` | Diện tích cửa (m²) | width_mm × height_mm / 1e6 | > 0 |
| `position` | `Shapely.Point` | Vị trí insertion point | Block INSERT từ DXF | NOT NULL |
| `related_room_a` | `str \| None` | internal_room_id phòng thứ nhất | MOD-05 | Nullable nếu unassigned |
| `related_room_b` | `str \| None` | internal_room_id phòng thứ hai | MOD-05 | Nullable nếu không phải ranh giới chung |
| `is_shared_boundary` | `bool` | True nếu cửa nằm giữa 2 phòng | MOD-05 | default False |
| `source` | `Literal["dxf_block", "excel_input"]` | Nguồn dữ liệu | MOD-05 | NOT NULL |

---

### Entity: `Edge`

| Field | Type | Ý nghĩa | Nguồn | Ràng buộc |
|---|---|---|---|---|
| `internal_room_id` | `str` | FK → Room | MOD-07 | NOT NULL |
| `edge_index` | `int` | Thứ tự cạnh (0-based) | polygon.exterior.coords | >= 0 |
| `start_point` | `Tuple[float, float]` | Tọa độ điểm đầu (mm) | polygon.exterior.coords | NOT NULL |
| `end_point` | `Tuple[float, float]` | Tọa độ điểm cuối (mm) | polygon.exterior.coords | NOT NULL |
| `length_mm` | `float` | Chiều dài cạnh (mm) | Computed | > 0 |
| `length_m` | `float` | Chiều dài cạnh (m) | length_mm / 1000 | > 0 |

---

### Entity: `ProcessingJob`

| Field | Type | Ý nghĩa | Nguồn | Ràng buộc |
|---|---|---|---|---|
| `job_id` | `str` (UUID) | Job ID | Auto-generated | NOT NULL |
| `created_at` | `datetime` | Thời điểm chạy | Auto | NOT NULL |
| `dxf_file_path` | `str` | Đường dẫn file DXF | UI input | NOT NULL |
| `dxf_file_hash` | `str` | SHA256 của file DXF | Computed | NOT NULL; dùng để audit |
| `room_json_path` | `str` | Đường dẫn room_boundaries.json từ LISP | Pipeline | NOT NULL |
| `door_excel_path` | `str \| None` | Đường dẫn door Excel | UI input | Nullable |
| `floor_height_mm` | `float` | Chiều cao áp dụng | UI input | > 0 |
| `wall_thickness_mm` | `float` | Chiều dày tường | UI input | > 0 |
| `unit_factor` | `float` | Hệ số đơn vị | MOD-01 | > 0 |
| `status` | `Literal["running","completed","failed"]` | Trạng thái | Pipeline | NOT NULL |
| `room_count` | `int` | Số phòng nhận diện được | Pipeline result | >= 0 |
| `door_count` | `int` | Số cửa | Pipeline result | >= 0 |
| `issue_count` | `int` | Số issues | MOD-08 | >= 0 |
| `output_excel_path` | `str \| None` | Đường dẫn file Excel output | MOD-09 | Nullable nếu chưa export |

---

### Entity: `ValidationIssue`

| Field | Type | Ý nghĩa | Ràng buộc |
|---|---|---|---|
| `issue_id` | `str` | ID duy nhất | NOT NULL |
| `severity` | `Literal["CRITICAL","ERROR","WARNING","INFO"]` | Mức độ | NOT NULL |
| `code` | `str` | Error code (VD: ROOM_NO_POLYGON, DOOR_UNASSIGNED) | NOT NULL |
| `message` | `str` | Message tiếng Việt không dấu | NOT NULL |
| `entity_type` | `Literal["room","door","edge","file"] \| None` | Entity liên quan | Nullable |
| `entity_id` | `str \| None` | ID của entity lỗi | Nullable |
| `context` | `dict \| None` | Thông tin bổ sung | Nullable |

---

## 9. Internal Contract / API Contract

Vì đây là desktop app, "API" là interface giữa các Python modules. Dùng Python dataclasses hoặc Pydantic models làm contract.

### Contract: `IntakeResult`

```python
@dataclass
class IntakeResult:
    dxf_path: str
    door_excel_path: Optional[str]
    unit_factor: float            # hệ số nhân để convert về mm
    dxf_version: str              # VD: "R2013"
    is_valid: bool
    errors: List[str]             # errors nếu is_valid == False
```

### Contract: `RawCADData`

```python
@dataclass
class RawCADData:
    wall_segments: List[Segment]        # [(x1,y1,x2,y2), ...]
    text_entities: List[TextEntity]     # [TextEntity(content, position, height), ...]
    door_blocks: List[DoorBlock]        # [DoorBlock(code, attrs, position), ...]
    source_file: str
    applied_unit_factor: float
```

### Contract: `PipelineResult`

```python
@dataclass
class PipelineResult:
    job: ProcessingJob
    rooms: List[Room]
    doors: List[Door]
    issues: List[ValidationIssue]
    status: Literal["completed", "completed_with_warnings", "failed"]
    
    @property
    def critical_issues(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == "CRITICAL"]
    
    @property
    def has_blocker(self) -> bool:
        return any(i.severity in ("CRITICAL", "ERROR") for i in self.issues)
```

### Contract: Pipeline Steps

Mỗi pipeline step tuân theo interface:

```python
class PipelineStep(Protocol):
    def run(self, state: PipelineState) -> PipelineState:
        """
        Nhận state hiện tại, xử lý, trả về state mới.
        KHÔNG mutate state đầu vào.
        Nếu lỗi không recoverable: raise PipelineCriticalError
        Nếu lỗi recoverable: thêm vào state.issues, trả về state
        """
        ...
```

Thứ tự pipeline steps:
```
IntakeStep → ParseStep → NormalizeStep → LoadRoomBoundariesStep
→ TextExtractionStep → RoomFinalizationStep → DoorDetectionStep
→ DoorMappingStep → CalculationStep → ValidationStep → ExportStep
```

### Error Schema

```python
@dataclass
class PipelineCriticalError(Exception):
    code: str
    message: str
    step: str
    cause: Optional[Exception] = None
```

---

## 10. Error Handling & Validation Strategy

### Phân loại lỗi và hành vi

| Severity | Trigger | Hành vi | Hiển thị UI |
|---|---|---|---|
| `CRITICAL` | DXF không đọc được; 0 phòng hợp lệ sau recognize | Dừng pipeline, trả về lỗi ngay | Modal error dialog |
| `ERROR` | Polygon invalid không fix được; phòng không có geometry | Bỏ qua entity lỗi, tiếp tục pipeline | Dòng đỏ trong log panel |
| `WARNING` | Phòng không có tên/mã; cửa không gán được phòng | Log và tiếp tục | Dòng vàng trong log panel |
| `INFO` | Polygon auto-fixed; duplicate room loại bỏ | Log, không hiển thị UI | Chỉ trong log file |

### Nguyên tắc fail-fast vs skip-and-continue

**Fail-fast (dừng pipeline):**
- Không đọc được DXF (file corrupt, version quá cũ).
- Không có phòng nào hợp lệ (user chưa chạy LISP hoặc JSON không tồn tại).
- Config thiếu required keys.

**Skip-and-continue (bỏ qua entity lỗi):**
- Phòng cụ thể không có polygon hợp lệ → bỏ phòng đó, tiếp tục với các phòng khác.
- Cửa thiếu width/height → bỏ cửa đó, log WARNING.
- Text không gán được phòng → log WARNING, tiếp tục.

### Logging

```
logs/
├── roomqs_{date}_{jobid}.log     # Full debug log
└── roomqs_{date}_{jobid}_audit.json  # Audit trail (job params + counts + hashes)
```

Log format: `{timestamp} [{severity}] [{step}] [{entity_id}] {message}`

---

## 11. Testing Strategy

### Unit Test (pytest)

**Target: Domain Engine hoàn toàn không phụ thuộc I/O.**

```
tests/
├── unit/
│   ├── test_calc_engine.py         # BR-04, BR-05, BR-06 với mock Room/Door
│   ├── test_door_mapper.py         # Spatial assignment logic
│   ├── test_room_dedup.py          # Duplicate detection logic
│   ├── test_text_classifier.py     # room_code vs room_name classification
│   ├── test_geometry_normalize.py  # unit conversion, polygon validation
│   └── test_validation_engine.py   # Issue generation cho từng rule
```

**Yêu cầu coverage:** ≥ 90% cho `calc_engine.py` và `door_mapper.py`.

### Integration Test

```
tests/
├── integration/
│   ├── test_dxf_parser.py          # Parse sample DXF fixtures
│   ├── test_pipeline_full.py       # End-to-end với sample DXF + mock LISP JSON
│   └── test_excel_export.py        # Verify Excel output structure
```

### Golden File Test

**Mục đích:** Đảm bảo output không thay đổi khi refactor.

```
tests/
├── golden/
│   ├── fixtures/
│   │   ├── simple_3room.dxf        # 3 phòng vuông vức, 2 cửa
│   │   ├── simple_3room.json       # room_boundaries từ LISP
│   │   └── door_list.xlsx          # door data
│   └── expected/
│       ├── simple_3room_rooms.json # Expected room output
│       └── simple_3room_excel.xlsx # Expected Excel output
```

Run: `pytest tests/golden/ --update-golden` để cập nhật expected output sau khi confirm thay đổi có chủ đích.

### Test Dữ liệu Xấu

```
tests/
├── bad_data/
│   ├── test_missing_room_text.py   # Phòng không có text
│   ├── test_unclosed_boundary.py   # Polygon không hợp lệ
│   ├── test_missing_door_attr.py   # Door block thiếu attributes
│   ├── test_zero_area_room.py      # Polygon hợp lệ nhưng area ≈ 0
│   └── test_duplicate_rooms.py     # 2 polygon overlap > 95%
```

**Tiêu chí:** Tất cả bad data test phải tạo ra `ValidationIssue` phù hợp, **không được crash**.

### Test Export Excel

```python
# Verify structure, không phụ thuộc format pixel
def test_excel_has_correct_sheets(output_excel):
    wb = openpyxl.load_workbook(output_excel)
    assert "Du lieu Phong" in wb.sheetnames
    assert "Du lieu Cua" in wb.sheetnames
    assert "Canh Phong" in wb.sheetnames

def test_excel_room_sheet_columns(output_excel):
    ws = openpyxl.load_workbook(output_excel)["Du lieu Phong"]
    headers = [ws.cell(1, c).value for c in range(1, 12)]
    assert "Ma Phong" in headers
    assert "Dien Tich (m2)" in headers
```

---

## 12. Cấu trúc thư mục dự án

```
roomqs/
│
├── src/                               # Application source
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── loader.py                  # Load & validate config.yaml
│   │   └── models.py                  # Config dataclasses
│   │
│   ├── intake/
│   │   ├── __init__.py
│   │   └── file_validator.py          # MOD-01
│   │
│   ├── cad_parser/
│   │   ├── __init__.py
│   │   ├── dxf_reader.py              # MOD-02: ezdxf wrapper
│   │   ├── entity_filter.py           # Filter by layer, type
│   │   └── models.py                  # RawCADData, Segment, TextEntity, DoorBlock
│   │
│   ├── geometry/
│   │   ├── __init__.py
│   │   ├── normalizer.py              # MOD-03: unit conversion, rounding
│   │   └── shapely_utils.py           # Helper: polygon_from_vertices, fix_polygon
│   │
│   ├── room_engine/
│   │   ├── __init__.py
│   │   ├── boundary_loader.py         # Đọc room_boundaries.json từ LISP
│   │   ├── deduplicator.py            # FR-06: loại bỏ duplicate polygon
│   │   └── room_builder.py            # Gắn text, tạo Room objects
│   │
│   ├── text_extractor/
│   │   ├── __init__.py
│   │   ├── mtext_cleaner.py           # Strip MTEXT format codes
│   │   └── tag_classifier.py          # Phân biệt room_code vs room_name
│   │
│   ├── door_engine/
│   │   ├── __init__.py
│   │   ├── door_parser.py             # Tạo Door từ DXF block + Excel
│   │   └── door_mapper.py             # MOD-05: spatial assignment
│   │
│   ├── calc_engine/
│   │   ├── __init__.py
│   │   ├── geometry_calc.py           # area, perimeter, edges từ Shapely
│   │   └── quantity_calc.py           # BR-04, BR-05, BR-06
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── validators.py              # Từng validator function
│   │   └── models.py                  # ValidationIssue dataclass
│   │
│   ├── export/
│   │   ├── __init__.py
│   │   ├── excel_builder.py           # Build DataFrame, call openpyxl
│   │   └── sheet_formatters.py        # Format headers, column widths
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── orchestrator.py            # MOD-11: điều phối các steps
│   │   ├── steps.py                   # Từng PipelineStep implementation
│   │   └── state.py                   # PipelineState dataclass
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py             # PySide6 MainWindow
│   │   ├── params_form.py             # Form nhập tham số
│   │   ├── log_panel.py               # Log/progress display
│   │   ├── preview_table.py           # Room preview table
│   │   └── worker.py                  # QThread worker cho pipeline
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                   # Setup logging
│       └── file_hash.py               # SHA256 cho audit
│
├── lisp/                              # AutoLISP files
│   ├── xr.lsp                         # Thuật toán Tia X-quang
│   ├── gb.lsp                         # Ghost Boundary
│   ├── door_seal.lsp                  # Door Sealing utility
│   └── export_rooms.lsp               # Ghi room_boundaries.json
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── golden/
│   │   ├── fixtures/
│   │   └── expected/
│   └── bad_data/
│
├── packaging/
│   ├── roomqs.spec                    # PyInstaller spec file
│   └── build.bat                      # Build script Windows
│
├── docs/
│   ├── quick-guide.md
│   └── lisp-setup.md
│
├── config.yaml                        # Default config (đi kèm .exe)
├── requirements.txt                   # Production deps
├── requirements-dev.txt               # Dev deps (pytest, matplotlib, etc.)
├── pyproject.toml                     # Project metadata
└── README.md
```

---

## 13. Rủi ro kỹ thuật và Trade-off

### RT-01: Dependency vào chất lượng bản vẽ

**Rủi ro:** Bản vẽ thực tế có rác, layer naming không chuẩn, wall lines không liên tục → thuật toán nhận diện phòng thất bại.

**Trade-off chấp nhận:** MVP yêu cầu bản vẽ "đủ sạch" — wall layer được đặt tên nhất quán và tường về cơ bản liên tục. Không giải quyết bản vẽ cực kỳ messy trong MVP.

**Mitigation:** Config layer name linh hoạt (BL-08); threshold lọc rác (300mm) trong config; Door Sealing cho hở tại cửa; log rõ khi thất bại.

---

### RT-02: Khó khăn Preview DXF trong App Python

**Vấn đề:** Không có thư viện "kéo thả ra là có DXF viewer" cho Python. QPainter trong PySide6 có thể vẽ LineString từ Shapely nhưng cần tự code toàn bộ zoom, pan, layer toggle.

**Quyết định MVP:** **Không làm DXF preview** trong MVP. Thay bằng preview table (Room list với diện tích). Developer có thể dùng matplotlib trong dev environment để debug geometry.

**Phase 2:** Nếu cần, dùng `ezdxf.addons.drawing` (render DXF sang matplotlib figure) nhúng vào PySide6 qua `FigureCanvasQTAgg`.

---

### RT-03: Packaging .exe

**Vấn đề:**
- Shapely có DLL native (GEOS). PyInstaller cần collect đúng DLL.
- PySide6 lớn (~50–100MB sau bundle).
- Antivirus có thể block .exe không signed.

**Mitigation:**
- Dùng `--collect-all shapely` và `--collect-all ezdxf` trong spec file.
- Test .exe trên máy sạch Windows 10/11 ngay từ Sprint 1 (BL-03).
- Cung cấp hướng dẫn whitelist antivirus.
- Phase 2: Code signing bằng self-signed cert hoặc mua cert nếu deploy rộng.

---

### RT-04: Performance

**Vấn đề:** Mặt bằng lớn (100+ phòng) có thể chậm nếu spatial lookup O(n²).

**Mitigation MVP:** Sắp xếp rooms theo bounding box trước khi spatial lookup (chỉ check phòng có bounding box overlap với door position). Với ≤ 50 phòng, brute force O(n²) vẫn đủ nhanh.

**Ngưỡng:** Mặt bằng ≤ 100 phòng phải xử lý xong trong < 60 giây. Nếu vượt ngưỡng → log WARNING và đề xuất spatial indexing (Shapely STRtree) ở Phase 2.

---

### RT-05: Antivirus False Positive

**Thực tế:** PyInstaller .exe không signed thường bị Windows Defender hoặc AV doanh nghiệp flag là "Unknown Publisher" hoặc thậm chí quarantine.

**Mitigation:** Hướng dẫn trong Quick Guide; build với `--exclude-module` các module không cần để giảm entropy; dùng onefolder thay vì onefile (onefolder ít bị flag hơn).

---

### RT-06: Maintainability của LISP Code

**Vấn đề:** AutoLISP không có package manager, không có unit test framework, debugging khó.

**Mitigation:**
- Giữ LISP chỉ làm "CAD interaction" — không có business logic ở LISP.
- Comment code bằng tiếng Việt không dấu.
- Mỗi file LISP chỉ làm 1 việc (xr.lsp, gb.lsp tách biệt).
- Tất cả business rules được test ở Python, không ở LISP.

---

## 14. Kiến nghị triển khai

### Technical Spikes cần làm trước Sprint 2

| Spike | Mục tiêu | Tiêu chí thành công | Timeline |
|---|---|---|---|
| **Spike-01: PyInstaller + Shapely + PySide6** | Verify bundle được .exe trên máy sạch | .exe mở được, không crash, Shapely import thành công | Sprint 1, 2 ngày |
| **Spike-02: BPOLY reliability với bản vẽ thực** | Chạy GB trên ≥ 3 file bản vẽ thực | ≥ 2/3 file tạo được Polygon cho ≥ 80% phòng | Sprint 2, 3 ngày |
| **Spike-03: ezdxf đọc block attributes** | Verify đọc được door attributes đúng | Đọc được code/width/height từ sample block | Sprint 1, 1 ngày |

---

### Prototype cần làm sớm nhất

1. **AutoLISP XR command** — chạy được trên AutoCAD thực, tạo Polyline đỏ. Không thể tiếp tục mà không có cái này.
2. **LISP → JSON export** — ghi tọa độ Polyline ra file. Là điểm giao giữa 2 hệ thống.
3. **Python đọc JSON → Shapely Polygon** — validate geometry pipeline hoạt động đầu cuối.

---

### Data Sample cần thu thập trước Sprint 2

| Sample | Mục đích |
|---|---|
| ≥ 1 file DXF bản vẽ mặt bằng thực (căn hộ 3–5 phòng) | Test XR trên môi trường thực |
| ≥ 1 file có phòng L-shape hoặc giật cấp | Test GB |
| ≥ 1 file có cửa block với attributes đầy đủ | Test door detection |
| ≥ 1 file "bẩn" (có nội thất, hatch, text rác) | Test noise resilience |

**Ưu tiên tuyệt đối:** Nếu không có file thực trước Sprint 2, team phải tự vẽ file test trong AutoCAD. Không nên chờ.

---

### Tiêu chí chứng minh Feasibility (Prototype Review — cuối Sprint 2)

- [ ] Lệnh XR tạo được Polyline cho ≥ 3 phòng vuông vức trong 1 file DXF thực.
- [ ] LISP ghi được `room_boundaries.json` hợp lệ.
- [ ] Python đọc JSON và tạo Shapely Polygon hợp lệ (`is_valid == True`).
- [ ] Tính được area và perimeter từ Polygon, sai lệch < 1% so với đo tay.
- [ ] PyInstaller .exe bundle thành công, chạy được trên máy không có Python.

Nếu đến cuối Sprint 2 mà một trong 5 tiêu chí trên không đạt → **dừng lại, triage kỹ thuật ngay**, không tiếp tục Sprint 3 cho đến khi có plan xử lý rõ ràng.

---

*Tài liệu này cần được Tech Lead review và ký tắt trước Sprint 1 kickoff. Bất kỳ thay đổi kiến trúc sau Sprint 3 phải có ADR (Architecture Decision Record) kèm theo.*
