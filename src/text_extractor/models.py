"""
models.py — Text Extractor Data Models (MOD-06)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextTag:
    """
    Đại diện cho một text entity sau khi đã được trích xuất và làm sạch (strip formatting).

    Attributes:
        content: Nội dung text đã được làm sạch (ví dụ: 'PHONG NGU').
        position: Tọa độ (x, y) bằng mm, kế thừa từ RawTextEntity.
        layer: Tên layer trong DXF, kế thừa từ RawTextEntity.
    """

    content: str
    position: tuple[float, float]
    layer: str
