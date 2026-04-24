"""
dxf_reader.py — CAD Parser Core (MOD-02)

Điểm duy nhất trong hệ thống tương tác với ezdxf entities.
Output là RawCADData — tất cả coordinates đã được chuẩn hóa sang mm.

Rules (theo kiến trúc):
- KHÔNG gọi Shapely.
- KHÔNG gọi text_extractor (MOD-06).
- KHÔNG gọi UI.
- KHÔNG tự đọc $INSUNITS — unit_factor nhận từ caller (MOD-01).
- KHÔNG parse INSERT block cửa — dành cho Sprint 2.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import ezdxf
from ezdxf.document import Drawing

from src.cad_parser.models import RawCADData, RawTextEntity, Segment

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Config type — giữ tối giản, chỉ cần wall_layer_names cho Sprint 1
# ---------------------------------------------------------------------------


@dataclass
class LayerConfig:
    """
    Cấu hình layer để lọc entity khi parse DXF.

    Attributes:
        wall_layer_names: Tập layer được xem là "tường".
                          So sánh không phân biệt hoa thường (case-insensitive).
    """

    wall_layer_names: list[str] = field(
        default_factory=lambda: ["TUONG", "A-WALL", "WALL", "Tuong"]
    )

    def is_wall_layer(self, layer_name: str) -> bool:
        """Trả về True nếu layer_name thuộc danh sách wall layers."""
        return layer_name.upper() in {name.upper() for name in self.wall_layer_names}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_dxf(
    filepath: str,
    layer_config: LayerConfig,
    unit_factor: float,
) -> RawCADData:
    """
    Đọc file DXF và trả về RawCADData với coordinates đã chuẩn hóa sang mm.

    Args:
        filepath:     Đường dẫn tuyệt đối đến file DXF.
        layer_config: Cấu hình layer (wall layers, v.v.).
        unit_factor:  Hệ số nhân để chuyển đổi về mm (do MOD-01 cung cấp).
                      Ví dụ: 25.4 nếu DXF dùng inch, 1.0 nếu đã là mm.

    Returns:
        RawCADData với:
          - wall_segments: LINE + LWPOLYLINE từ wall layers, coordinates × unit_factor.
          - text_entities: TEXT + MTEXT từ mọi layer, position × unit_factor.
          - door_blocks:   [] (Sprint 2).

    Raises:
        ezdxf.DXFError:      File DXF bị corrupt hoặc không đọc được.
        ezdxf.DXFVersionError: DXF version không được hỗ trợ.
        FileNotFoundError:   File không tồn tại.
        ValueError:          unit_factor <= 0.
    """
    if unit_factor <= 0:
        raise ValueError(f"unit_factor phải > 0, nhận được: {unit_factor}")

    logger.info("Bắt đầu parse DXF: %s (unit_factor=%.4f)", filepath, unit_factor)

    # ezdxf.readfile raises ezdxf.DXFError hoặc OSError nếu file corrupt/không hợp lệ
    try:
        doc: Drawing = ezdxf.readfile(filepath)
    except ezdxf.DXFError:
        logger.error("File DXF bi corrupt hoac khong hop le: %s", filepath)
        raise
    except OSError as exc:
        # ezdxf raise OSError("File is not a DXF file") cho file khong dung dinh dang
        if "not a DXF" in str(exc) or "DXF" in str(exc):
            logger.error("File khong phai dinh dang DXF: %s", filepath)
            raise
        # FileNotFoundError la subclass cua OSError
        logger.error("Loi khi mo file DXF: %s - %s", filepath, exc)
        raise

    msp = doc.modelspace()

    wall_segments: list[Segment] = []
    text_entities: list[RawTextEntity] = []

    for entity in msp:
        dxf_type = entity.dxftype()

        # ------------------------------------------------------------------
        # LINE → 1 Segment
        # ------------------------------------------------------------------
        if dxf_type == "LINE":
            if layer_config.is_wall_layer(entity.dxf.layer):
                start = _apply_factor_2d(entity.dxf.start, unit_factor)
                end = _apply_factor_2d(entity.dxf.end, unit_factor)
                wall_segments.append(
                    Segment(start=start, end=end, layer=entity.dxf.layer)
                )

        # ------------------------------------------------------------------
        # LWPOLYLINE → N-1 Segments (mỗi cặp điểm kề nhau tạo 1 segment)
        # Note: LWPOLYLINE.get_points() trả về (x, y, start_width, end_width, bulge)
        # ------------------------------------------------------------------
        elif dxf_type == "LWPOLYLINE":
            if layer_config.is_wall_layer(entity.dxf.layer):
                _extract_lwpolyline_segments(entity, unit_factor, wall_segments)

        # ------------------------------------------------------------------
        # TEXT → 1 RawTextEntity (mọi layer)
        # ------------------------------------------------------------------
        elif dxf_type == "TEXT":
            position = _apply_factor_2d(entity.dxf.insert, unit_factor)
            text_entities.append(
                RawTextEntity(
                    raw_content=entity.dxf.text,
                    position=position,
                    layer=entity.dxf.layer,
                )
            )

        # ------------------------------------------------------------------
        # MTEXT → 1 RawTextEntity (mọi layer) — raw_content chưa strip
        # ------------------------------------------------------------------
        elif dxf_type == "MTEXT":
            position = _apply_factor_2d(entity.dxf.insert, unit_factor)
            text_entities.append(
                RawTextEntity(
                    raw_content=entity.text,  # .text là property, không phải dxf attr
                    position=position,
                    layer=entity.dxf.layer,
                )
            )

    logger.info(
        "Parse xong: %d wall segments, %d text entities",
        len(wall_segments),
        len(text_entities),
    )

    return RawCADData(
        wall_segments=wall_segments,
        text_entities=text_entities,
        door_blocks=[],
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _apply_factor_2d(
    point: object,
    factor: float,
) -> tuple[float, float]:
    """
    Nhân x, y của point với factor và trả về tuple (x_mm, y_mm).
    Bỏ qua chiều z nếu có (DXF 2D entities).
    """
    # ezdxf trả về Vec3 hoặc UCS — cả hai đều hỗ trợ indexing [0], [1]
    return (float(point[0]) * factor, float(point[1]) * factor)


def _extract_lwpolyline_segments(
    entity: object,
    unit_factor: float,
    out: list[Segment],
) -> None:
    """
    Trích xuất các Segment từ LWPOLYLINE và append vào out.
    Hỗ trợ closed polyline (nối điểm cuối → điểm đầu).

    LWPOLYLINE.get_points() format: [(x, y, start_width, end_width, bulge), ...]
    Chỉ lấy x, y (index 0, 1).
    """
    raw_points = list(entity.get_points())  # list of tuple(x, y, sw, ew, bulge)

    if len(raw_points) < 2:
        logger.warning(
            "LWPOLYLINE trên layer '%s' có < 2 điểm, bỏ qua.",
            entity.dxf.layer,
        )
        return

    # Tạo danh sách (x_mm, y_mm)
    pts: list[tuple[float, float]] = [
        (float(p[0]) * unit_factor, float(p[1]) * unit_factor)
        for p in raw_points
    ]

    # Nối các điểm kề nhau thành Segment
    for i in range(len(pts) - 1):
        out.append(Segment(start=pts[i], end=pts[i + 1], layer=entity.dxf.layer))

    # Nếu polyline closed → nối điểm cuối về điểm đầu
    if entity.closed:
        out.append(Segment(start=pts[-1], end=pts[0], layer=entity.dxf.layer))
