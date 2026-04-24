"""
cad_parser — MOD-02: CAD Parser

Public API của module:
  - parse_dxf: đọc file DXF, trả về RawCADData chuẩn hóa mm
  - LayerConfig: cấu hình layer filter
  - RawCADData, Segment, RawTextEntity: data models

Không import Shapely, text_extractor, UI tại đây.
"""

from src.cad_parser.dxf_reader import LayerConfig, parse_dxf
from src.cad_parser.models import RawCADData, RawTextEntity, Segment

__all__ = [
    "parse_dxf",
    "LayerConfig",
    "RawCADData",
    "Segment",
    "RawTextEntity",
]
