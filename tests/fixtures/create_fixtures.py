"""
create_fixtures.py — Script tạo synthetic DXF test fixtures cho T1-03/T1-04/T1-05

Chạy một lần để tạo file DXF tại tests/fixtures/.
Không phải production code — chỉ dùng trong môi trường dev/CI.

Usage:
    python tests/fixtures/create_fixtures.py
"""

from __future__ import annotations

import pathlib

import ezdxf
from ezdxf import units

FIXTURE_DIR = pathlib.Path(__file__).parent


def create_simple_rooms_dxf() -> None:
    """
    simple_rooms.dxf:
    - $INSUNITS = 4 (mm) → unit_factor = 1.0
    - Layer tường: "TUONG"
    - 3 phòng hình chữ nhật:
        * Phòng A: (0,0)→(3000,0)→(3000,2500)→(0,2500) → 4 LINE trên TUONG
        * Phòng B: (3000,0)→(6000,0)→(6000,2500)→(3000,2500) → 4 LINE trên TUONG
        * Phòng C: (0,2500)→(6000,2500)→(6000,5000)→(0,5000) → 1 LWPOLYLINE closed trên TUONG
    - Tổng LINE trên TUONG: 8 (Phòng A: 4 + Phòng B: 4)
    - Tổng LWPOLYLINE trên TUONG: 1 (Phòng C — closed → 4 segments khi parse)
    - Tổng wall_segments sau parse_dxf(): 12 (8 LINE + 4 LWPOLYLINE segments)
    - 1 LINE trên layer OTHER: bị exclude khỏi wall_segments
    - 3 TEXT entities: "PHONG NGU", "WC", "PHONG KHACH" trên TEXT_LAYER
    - 1 MTEXT entity: "{\\fArial|b0|i0|c0|p34;PHONG KHACH MTEXT}" trên TEXT_LAYER
    """
    doc = ezdxf.new(dxfversion="R2013")
    doc.header["$INSUNITS"] = units.MM  # 4

    # Tạo layer
    doc.layers.add("TUONG", color=7)
    doc.layers.add("TEXT_LAYER", color=2)
    doc.layers.add("OTHER", color=3)

    msp = doc.modelspace()

    # ---- Phòng A: (0,0)–(3000,2500) ----
    _add_room_lines(msp, 0, 0, 3000, 2500, "TUONG")

    # ---- Phòng B: (3000,0)–(6000,2500) ----
    _add_room_lines(msp, 3000, 0, 6000, 2500, "TUONG")

    # ---- Phòng C: dùng LWPOLYLINE (0,2500)–(6000,5000) ----
    _add_room_lwpolyline(msp, 0, 2500, 6000, 5000, "TUONG")

    # ---- TEXT entities ----
    msp.add_text(
        "PHONG NGU",
        dxfattribs={"insert": (1500, 1250), "height": 200, "layer": "TEXT_LAYER"},
    )
    msp.add_text(
        "WC",
        dxfattribs={"insert": (4500, 1250), "height": 200, "layer": "TEXT_LAYER"},
    )
    msp.add_text(
        "PHONG KHACH",
        dxfattribs={"insert": (3000, 3750), "height": 200, "layer": "TEXT_LAYER"},
    )

    # ---- MTEXT entity (có formatting codes) ----
    msp.add_mtext(
        r"{\fArial|b0|i0|c0|p34;PHONG KHACH MTEXT}",
        dxfattribs={"insert": (3000, 3500), "char_height": 200, "layer": "TEXT_LAYER"},
    )

    # ---- Entity trên layer OTHER (phải bị exclude khỏi wall_segments) ----
    msp.add_line((0, 0), (1000, 0), dxfattribs={"layer": "OTHER"})

    path = FIXTURE_DIR / "simple_rooms.dxf"
    doc.saveas(str(path))
    print(f"[OK] Created: {path}")
    print(
        "     Expected: 12 LINE segments (TUONG) + 4 LWPOLYLINE segments (TUONG)"
        " + 3 TEXT + 1 MTEXT"
    )


def create_corrupt_dxf() -> None:
    """
    corrupt.dxf: file DXF bị truncate — ezdxf phải raise DXFError khi đọc.
    """
    path = FIXTURE_DIR / "corrupt.dxf"
    path.write_bytes(b"This is NOT a valid DXF file\x00\x01\x02")
    print(f"[OK] Created: {path}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _add_room_lines(
    msp,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    layer: str,
) -> None:
    """Thêm 4 LINE tạo thành hình chữ nhật (x0,y0)–(x1,y1) vào modelspace."""
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for i in range(4):
        msp.add_line(
            corners[i],
            corners[(i + 1) % 4],
            dxfattribs={"layer": layer},
        )


def _add_room_lwpolyline(
    msp,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    layer: str,
) -> None:
    """Thêm 1 LWPOLYLINE closed hình chữ nhật (x0,y0)–(x1,y1)."""
    points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    create_simple_rooms_dxf()
    create_corrupt_dxf()
    print("\nAll fixtures created at:", FIXTURE_DIR)
