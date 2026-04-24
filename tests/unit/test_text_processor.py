"""
tests/unit/test_text_processor.py

Unit tests cho module src/text_extractor/ (MOD-06).
Kiểm tra các rule strip MTEXT formatting và việc chuyển đổi RawTextEntity -> TextTag.
Thuần Python, không gọi file DXF thực và không dùng ezdxf.
"""

import pytest

from src.cad_parser.models import RawTextEntity
from src.text_extractor.models import TextTag
from src.text_extractor.processor import process_text_entities, strip_mtext_formatting


# ---------------------------------------------------------------------------
# Các test case cho hàm `strip_mtext_formatting` (AC-01 -> AC-03)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw_text, expected", [
    # AC-01: Plain text (TEXT entity)
    ("PHONG NGU", "PHONG NGU"),
    ("WC", "WC"),
    
    # AC-02: MTEXT cơ bản với curly braces và formatting bắt đầu bằng `\` kết thúc bằng `;`
    ("{\\fArial;PHONG NGU}", "PHONG NGU"),
    ("{\\fArial|b0|i0|c0|p34;PHONG KHACH}", "PHONG KHACH"),
    ("{\\C1;RED TEXT}", "RED TEXT"),
    ("{\\H1.5x;BIG TEXT}", "BIG TEXT"),
    
    # AC-03: MTEXT chứa newline (`\P` hoặc `\p`)
    ("\\PPHONG NGU", "PHONG NGU"),
    ("PHONG\\P  NGU  ", "PHONG NGU"),
    ("{\\fArial;PHONG\\PWC}", "PHONG WC"),
    
    # Các trường hợp phức tạp hỗn hợp
    ("{\\fArial|b0|i0;\\C2;\\PPHONG\\P NGU}", "PHONG NGU"),
    ("{\\LUnderlined Text}", "Underlined Text"),
    ("{\\W0.8;Width Text}", "Width Text"),
    
    # Khoảng trắng và dấu xuống dòng bình thường
    ("  TEXT   \n  \n  123  ", "TEXT 123"),
    
    # Chuỗi rỗng / None (nếu code gọi pass vào None thì exception, nhưng rỗng thì "")
    ("", ""),
])
def test_strip_mtext_formatting(raw_text: str, expected: str):
    """Kiểm tra logic loại bỏ MTEXT formatting codes theo nhiều pattern."""
    assert strip_mtext_formatting(raw_text) == expected


# ---------------------------------------------------------------------------
# Test logic `process_text_entities` (AC-04, AC-05)
# ---------------------------------------------------------------------------

def test_process_text_entities_passthrough_fields():
    """AC-04: position và layer được truyền qua mà không thay đổi."""
    raw_entities = [
        RawTextEntity(raw_content="{\\fArial;ROOM 1}", position=(100.0, 200.0), layer="TUONG"),
        RawTextEntity(raw_content="ROOM 2", position=(50.5, 0.0), layer="TEXT_LAYER")
    ]
    
    tags = process_text_entities(raw_entities)
    
    assert len(tags) == 2
    
    # Assert các nội dung (đã xử lý)
    assert tags[0].content == "ROOM 1"
    assert tags[1].content == "ROOM 2"
    
    # Assert giữ nguyên position
    assert tags[0].position == (100.0, 200.0)
    assert tags[1].position == (50.5, 0.0)
    
    # Assert giữ nguyên layer
    assert tags[0].layer == "TUONG"
    assert tags[1].layer == "TEXT_LAYER"


def test_process_text_entities_filters_empty():
    """Kiểm tra xem hàm có loại bỏ những text trở thành rỗng sau khi bị strip hay không."""
    raw_entities = [
        RawTextEntity(raw_content="{\\fArial;}", position=(0.0, 0.0), layer="L1"),
        RawTextEntity(raw_content="   \\P   ", position=(1.0, 1.0), layer="L2"),
        RawTextEntity(raw_content="VALID", position=(2.0, 2.0), layer="L3"),
    ]
    
    tags = process_text_entities(raw_entities)
    
    assert len(tags) == 1
    assert tags[0].content == "VALID"
