"""
models.py — Cad Parser Data Models (MOD-02)

Các dataclass trung gian giữa ezdxf output và các module xử lý tiếp theo.
Đơn vị: tất cả coordinates đã là mm (sau khi apply unit_factor trong dxf_reader).

Rule:
- Không import ezdxf tại đây.
- Không import Shapely.
- Không import bất kỳ module src khác.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Segment:
    """
    Đại diện cho một đoạn thẳng (LINE hoặc một cạnh của LWPOLYLINE).

    Attributes:
        start: Tọa độ điểm đầu (x, y) tính bằng mm.
        end:   Tọa độ điểm cuối (x, y) tính bằng mm.
        layer: Tên layer trong DXF (giữ nguyên, không normalize).
    """

    start: tuple[float, float]
    end: tuple[float, float]
    layer: str


@dataclass(frozen=True)
class RawTextEntity:
    """
    Đại diện cho một text entity (TEXT hoặc MTEXT) đọc thẳng từ DXF.
    Nội dung chưa strip MTEXT formatting — việc đó là trách nhiệm của MOD-06.

    Attributes:
        raw_content: Nội dung text gốc, có thể chứa MTEXT formatting codes.
        position:    Vị trí insertion point (x, y) tính bằng mm.
        layer:       Tên layer trong DXF.
    """

    raw_content: str
    position: tuple[float, float]
    layer: str


@dataclass
class RawCADData:
    """
    Output chuẩn của MOD-02 (cad_parser). Tất cả coordinates đã được
    nhân unit_factor và biểu diễn bằng mm.

    Attributes:
        wall_segments:  Danh sách đoạn thẳng từ wall layers (LINE + LWPOLYLINE edges).
        text_entities:  Danh sách text entities thô từ mọi layer (TEXT + MTEXT).
        door_blocks:    Placeholder cho INSERT block cửa — Sprint 2 sẽ populate.
    """

    wall_segments: list[Segment] = field(default_factory=list)
    text_entities: list[RawTextEntity] = field(default_factory=list)
    door_blocks: list = field(default_factory=list)  # Sprint 2 — kiểu sẽ định nghĩa sau
