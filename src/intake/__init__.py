"""
src/intake/__init__.py

Public API của module intake (MOD-01).
"""

from .models import IntakeResult
from .unit_detector import detect_unit_factor

__all__ = ["detect_unit_factor", "IntakeResult"]
