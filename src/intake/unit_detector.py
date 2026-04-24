"""
src/intake/unit_detector.py

Detect $INSUNITS from DXF header and return the corresponding unit_factor (mm basis).
All coordinates in Python runtime are expected to be in millimetres (mm).

ADR-03 mapping:
  0  = unitless       → factor 1.0  (default, log warning)
  1  = inches         → factor 25.4
  2  = feet           → factor 304.8
  4  = millimetres    → factor 1.0
  5  = centimetres    → factor 10.0
  6  = metres         → factor 1000.0
"""

import logging
from typing import Tuple

import ezdxf

logger = logging.getLogger(__name__)

# $INSUNITS code → (unit_factor, unit_name)
_INSUNITS_MAP: dict[int, Tuple[float, str]] = {
    0: (1.0, "unitless"),
    1: (25.4, "inches"),
    2: (304.8, "feet"),
    4: (1.0, "millimetres"),
    5: (10.0, "centimetres"),
    6: (1000.0, "metres"),
}

_UNKNOWN_FALLBACK: Tuple[float, str] = (1.0, "unknown")


def detect_unit_factor(filepath: str) -> Tuple[float, str]:
    """Read the DXF file header and return (unit_factor, unit_name).

    The unit_factor multiplied by any raw coordinate value yields millimetres.

    Args:
        filepath: Absolute or relative path to the DXF file.

    Returns:
        Tuple of (unit_factor: float, unit_name: str).

    Raises:
        ezdxf.DXFError: If the file cannot be opened or is not a valid DXF.
        FileNotFoundError: If the file does not exist.
    """
    doc = ezdxf.readfile(filepath)
    insunits: int = int(doc.header.get("$INSUNITS", 0))

    if insunits == 0:
        logger.warning(
            "Don vi ve khong xac dinh ($INSUNITS=0) — su dung mac dinh 1.0 (mm). "
            "Kiem tra lai file DXF: %s",
            filepath,
        )

    factor, unit_name = _INSUNITS_MAP.get(insunits, _UNKNOWN_FALLBACK)

    if insunits not in _INSUNITS_MAP:
        logger.warning(
            "$INSUNITS=%d khong duoc ho tro — fallback ve 1.0 (mm). File: %s",
            insunits,
            filepath,
        )

    return factor, unit_name
