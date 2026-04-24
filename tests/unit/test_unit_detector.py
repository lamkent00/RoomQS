"""
tests/unit/test_unit_detector.py

Unit tests for src/intake/unit_detector.py (T1-04 — AC-01 … AC-05).
All tests mock ezdxf.readfile to avoid requiring a real DXF file.
"""

import logging
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from src.intake.unit_detector import detect_unit_factor


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_doc(insunits: Optional[int]) -> MagicMock:
    """Return a mock ezdxf Document with the given $INSUNITS value in the header."""
    doc = MagicMock()
    if insunits is None:
        # Simulate missing key → ezdxf header.get returns default 0
        doc.header.get.return_value = 0
    else:
        doc.header.get.return_value = insunits
    return doc


# ---------------------------------------------------------------------------
# AC-01: $INSUNITS=4 (mm) → factor = 1.0
# ---------------------------------------------------------------------------

def test_insunits_4_mm():
    """AC-01: Millimetres → factor 1.0, unit_name 'millimetres'."""
    with patch("src.intake.unit_detector.ezdxf.readfile", return_value=_make_doc(4)):
        factor, unit_name = detect_unit_factor("dummy.dxf")
    assert factor == 1.0
    assert unit_name == "millimetres"


# ---------------------------------------------------------------------------
# AC-02: $INSUNITS=6 (metres) → factor = 1000.0
# ---------------------------------------------------------------------------

def test_insunits_6_metres():
    """AC-02: Metres → factor 1000.0, unit_name 'metres'."""
    with patch("src.intake.unit_detector.ezdxf.readfile", return_value=_make_doc(6)):
        factor, unit_name = detect_unit_factor("dummy.dxf")
    assert factor == 1000.0
    assert unit_name == "metres"


# ---------------------------------------------------------------------------
# AC-03: $INSUNITS=1 (inches) → factor = 25.4
# ---------------------------------------------------------------------------

def test_insunits_1_inches():
    """AC-03: Inches → factor 25.4, unit_name 'inches'."""
    with patch("src.intake.unit_detector.ezdxf.readfile", return_value=_make_doc(1)):
        factor, unit_name = detect_unit_factor("dummy.dxf")
    assert factor == 25.4
    assert unit_name == "inches"


# ---------------------------------------------------------------------------
# AC-04: $INSUNITS=0 → factor = 1.0 + log warning
# ---------------------------------------------------------------------------

def test_insunits_0_unitless_returns_default(caplog):
    """AC-04a: Unitless → factor 1.0."""
    with patch("src.intake.unit_detector.ezdxf.readfile", return_value=_make_doc(0)):
        with caplog.at_level(logging.WARNING, logger="src.intake.unit_detector"):
            factor, unit_name = detect_unit_factor("dummy.dxf")
    assert factor == 1.0
    assert unit_name == "unitless"


def test_insunits_0_emits_warning(caplog):
    """AC-04b: Unitless → log warning containing expected message."""
    with patch("src.intake.unit_detector.ezdxf.readfile", return_value=_make_doc(0)):
        with caplog.at_level(logging.WARNING, logger="src.intake.unit_detector"):
            detect_unit_factor("dummy.dxf")
    warning_messages = [r.message for r in caplog.records if r.levelno == logging.WARNING]
    assert any("Don vi ve khong xac dinh" in msg for msg in warning_messages), (
        f"Expected warning not found. Got: {warning_messages}"
    )


# ---------------------------------------------------------------------------
# Additional coverage: other valid $INSUNITS codes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "insunits, expected_factor, expected_name",
    [
        (2, 304.8, "feet"),
        (5, 10.0, "centimetres"),
    ],
)
def test_other_known_insunits(insunits, expected_factor, expected_name):
    """Feet and centimetres map correctly."""
    with patch("src.intake.unit_detector.ezdxf.readfile", return_value=_make_doc(insunits)):
        factor, unit_name = detect_unit_factor("dummy.dxf")
    assert factor == expected_factor
    assert unit_name == expected_name


# ---------------------------------------------------------------------------
# Edge case: unknown $INSUNITS code → fallback 1.0 + warning
# ---------------------------------------------------------------------------

def test_unknown_insunits_fallback(caplog):
    """Unknown $INSUNITS code → factor 1.0, log warning."""
    with patch("src.intake.unit_detector.ezdxf.readfile", return_value=_make_doc(99)):
        with caplog.at_level(logging.WARNING, logger="src.intake.unit_detector"):
            factor, unit_name = detect_unit_factor("dummy.dxf")
    assert factor == 1.0
    assert unit_name == "unknown"
    warning_messages = [r.message for r in caplog.records if r.levelno == logging.WARNING]
    assert any("99" in msg for msg in warning_messages)


# ---------------------------------------------------------------------------
# AC-05 (implicit): DXF read exception propagates unchanged
# ---------------------------------------------------------------------------

def test_dxf_read_error_propagates():
    """DXFError from ezdxf propagates to caller (not silently swallowed)."""
    import ezdxf

    with patch(
        "src.intake.unit_detector.ezdxf.readfile",
        side_effect=ezdxf.DXFError("bad file"),
    ):
        with pytest.raises(ezdxf.DXFError):
            detect_unit_factor("corrupt.dxf")
