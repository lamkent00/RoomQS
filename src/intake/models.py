"""
src/intake/models.py

Data models for the File Intake module (MOD-01).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class IntakeResult:
    """Immutable result returned by the File Intake module after reading a DXF header.

    Attributes:
        file_path:   Path of the DXF file that was read.
        dxf_version: DXF version string, e.g. "AC1015" (R2000).
        unit_factor: Multiply raw coordinates by this value to get millimetres.
        unit_name:   Human-readable name of the detected unit, e.g. "millimetres".
    """

    file_path: str
    dxf_version: str
    unit_factor: float
    unit_name: str
