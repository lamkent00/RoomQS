# DXF Test Fixtures

Thư mục này chứa file DXF dùng để test module `cad_parser` (T1-03), `intake` (T1-04), `text_extractor` (T1-05).

Script tái tạo fixtures synthetic: `python tests/fixtures/create_fixtures.py`

---

## Fixture 1: `simple_rooms.dxf` ⭐ PRIMARY TEST FIXTURE

**Mô tả:** Synthetic file tạo bằng ezdxf — 3 phòng hình chữ nhật, dùng cho toàn bộ unit test T1-03/T1-04/T1-05.

| Thuộc tính | Giá trị |
|---|---|
| `$INSUNITS` | `4` (mm) → `unit_factor = 1.0` |
| DXF version | R2013 |
| Tạo bởi | `create_fixtures.py` |

### Layers

| Layer | Màu | Mô tả |
|---|---|---|
| `TUONG` | 7 (trắng) | Layer tường — wall layer chính |
| `TEXT_LAYER` | 2 (vàng) | Layer text nhãn phòng |
| `OTHER` | 3 (xanh lá) | Layer phụ — phải bị exclude khỏi `wall_segments` |

### Entity count (expected values)

| Entity type | Layer | Số lượng | Ghi chú |
|---|---|---|---|
| `LINE` | `TUONG` | **8** | Phòng A: 4 LINE, Phòng B: 4 LINE |
| `LINE` | `OTHER` | **1** | Phải bị exclude — không phải wall layer |
| `LWPOLYLINE` | `TUONG` | **1** | Phòng C: 1 LWPOLYLINE closed 4 điểm → 4 segments |
| `TEXT` | `TEXT_LAYER` | **3** | `"PHONG NGU"`, `"WC"`, `"PHONG KHACH"` |
| `MTEXT` | `TEXT_LAYER` | **1** | `{\fArial\|b0\|i0\|c0\|p34;PHONG KHACH MTEXT}` |

### Expected `parse_dxf()` output (unit_factor=1.0)

| Field | Giá trị |
|---|---|
| `wall_segments` | **12 Segment** (8 LINE trên TUONG + 4 từ LWPOLYLINE closed) |
| `text_entities` | **4 RawTextEntity** (3 TEXT + 1 MTEXT, raw chưa strip) |
| `door_blocks` | `[]` |

### Tọa độ phòng (mm)

| Phòng | Góc dưới-trái | Góc trên-phải | Entity type |
|---|---|---|---|
| Phòng A (PHONG NGU) | `(0, 0)` | `(3000, 2500)` | 4 LINE |
| Phòng B (WC) | `(3000, 0)` | `(6000, 2500)` | 4 LINE |
| Phòng C (PHONG KHACH) | `(0, 2500)` | `(6000, 5000)` | 1 LWPOLYLINE closed |

### Tọa độ TEXT entities (mm)

| Content | Position (x, y) | Layer |
|---|---|---|
| `"PHONG NGU"` | `(1500.0, 1250.0)` | `TEXT_LAYER` |
| `"WC"` | `(4500.0, 1250.0)` | `TEXT_LAYER` |
| `"PHONG KHACH"` | `(3000.0, 3750.0)` | `TEXT_LAYER` |
| `"{\fArial\|b0\|i0\|c0\|p34;PHONG KHACH MTEXT}"` | `(3000.0, 3500.0)` | `TEXT_LAYER` |

---

## Fixture 2: `corrupt.dxf`

**Mô tả:** File không phải DXF hợp lệ — nội dung là chuỗi bytes ngẫu nhiên.

**Expected behavior:**
- `ezdxf.readfile()` raise `OSError` (hoặc `ezdxf.DXFError`) — cả hai đều acceptable.
- Test trong `test_dxf_reader.py::TestAC07ErrorHandling` dùng `pytest.raises((ezdxf.DXFError, OSError))`.

**Lý do raise `OSError` thay vì `DXFError`:**
ezdxf phát hiện file không bắt đầu đúng định dạng DXF (header không có `0\nSECTION`) ngay từ đầu và raise `OSError("File is not a DXF file")` trước khi vào code path parse.

---

## Fixture 3: `banve.dxf` (Real Sample — Production DXF)

**Mô tả:** File DXF thực từ dự án, dùng để kiểm tra khả năng đọc file thực tế.

| Thuộc tính | Giá trị |
|---|---|
| `$INSUNITS` | Không có (N/A) → `unit_factor` fallback về `1.0` + warning |
| DXF version | AC1032 (AutoCAD 2018+) |
| File size | ~10.9 MB |

### Entity count (thực tế đọc được)

| Entity type | Số lượng |
|---|---|
| `LINE` | 3,401 |
| `LWPOLYLINE` | 478 |
| `MTEXT` | 283 |
| `TEXT` | 316 |
| `INSERT` | 549 |
| `DIMENSION` | 920 |
| `HATCH` | 151 |
| `ARC` | 47 |
| `CIRCLE` | 37 |
| `ELLIPSE` | 74 |
| `LEADER` | 85 |
| `ACAD_TABLE` | 1 |

### Layer names (49 layers, 20 đầu tiên)

`0`, `DEFPOINTS`, `01-WALL`, `02-TEXT`, `08-HATCH`, `04-TRUC`, `06-THAY VUA`, `09-DIMOUT`, `13-VATDUNG`, `03-KYHIEU`, `07-HATCH`, `11 CUA`, `00 gach chiu lua`, `HATCH`, `CUA`, `SectionCutEdges`, `14 KHUAT`, `dim`, `ghichu`, `15 TEXT`, ...

**Wall layer candidate:** `01-WALL` (chứa phần lớn LINE/LWPOLYLINE của tường).

---

## Fixture 4: `real_sample.dxf`

**Mô tả:** Copy của `banve.dxf` — dùng với tên chuẩn theo Ticket Brief T1-06.
Cùng nội dung, cùng expected values với `banve.dxf` ở trên.

---

## Ghi chú kỹ thuật

- Fixtures synthetic (`simple_rooms.dxf`, `corrupt.dxf`) tạo bằng script: `tests/fixtures/create_fixtures.py`
- Chạy `python tests/fixtures/create_fixtures.py` để tái tạo nếu cần
- `banve.dxf` / `real_sample.dxf` là file thực — KHÔNG tái tạo được bằng script
- Tất cả test hiện tại dùng `simple_rooms.dxf` (synthetic) để có kết quả deterministic
