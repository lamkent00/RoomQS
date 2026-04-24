# DXF Test Fixtures

Thư mục này chứa file DXF dùng để test module `cad_parser` (T1-03, T1-04, T1-05).

## Fixture 1: `simple_rooms.dxf`

**Mô tả:** Synthetic file với 3 phòng hình chữ nhật.

| Thuộc tính | Giá trị |
|---|---|
| `$INSUNITS` | `4` (mm) → `unit_factor = 1.0` |
| DXF version | R2013 |

**Layers:**
| Layer | Mô tả |
|---|---|
| `TUONG` | Layer tường (wall layer) |
| `TEXT_LAYER` | Layer text nhãn phòng |
| `OTHER` | Layer phụ — phải bị exclude khỏi wall_segments |

**Entity count (expected values):**
| Entity type | Layer | Số lượng | Ghi chú |
|---|---|---|---|
| `LINE` | `TUONG` | 8 | Phòng A: 4 LINE, Phòng B: 4 LINE |
| `LWPOLYLINE` | `TUONG` | 1 | Phòng C: 1 LWPOLYLINE closed → 4 segments |
| `TEXT` | `TEXT_LAYER` | 3 | "PHONG NGU", "WC", "PHONG KHACH" |
| `MTEXT` | `TEXT_LAYER` | 1 | `{\fArial|b0|i0|c0|p34;PHONG KHACH MTEXT}` |
| `LINE` | `OTHER` | 1 | Phải bị exclude — không phải wall layer |

**Expected parse_dxf() output (unit_factor=1.0):**
- `wall_segments`: **12 Segment** (8 từ LINE + 4 từ LWPOLYLINE closed)
- `text_entities`: **4 RawTextEntity** (3 TEXT + 1 MTEXT)
- `door_blocks`: `[]`

**Tọa độ phòng (mm):**
- Phòng A (PHONG NGU): `(0,0)` → `(3000,0)` → `(3000,2500)` → `(0,2500)`
- Phòng B (WC): `(3000,0)` → `(6000,0)` → `(6000,2500)` → `(3000,2500)`
- Phòng C (PHONG KHACH): `(0,2500)` → `(6000,2500)` → `(6000,5000)` → `(0,5000)`

---

## Fixture 2: `corrupt.dxf`

**Mô tả:** File DXF bị truncate, không phải DXF hợp lệ.

**Expected behavior:** `ezdxf.readfile()` phải raise `ezdxf.DXFError`.

---

## Ghi chú

- Fixtures tạo bằng script: `tests/fixtures/create_fixtures.py`
- Chạy `python tests/fixtures/create_fixtures.py` để tái tạo fixtures nếu cần
- `real_sample.dxf` — chưa có (phụ thuộc T0-01 Sprint 0); sẽ bổ sung khi có file DXF thực
