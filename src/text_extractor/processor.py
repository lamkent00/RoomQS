"""
processor.py — Text Extractor Logic (MOD-06)

Trích xuất và làm sạch text entities.
Nhận input là danh sách RawTextEntity (từ cad_parser) và trả về danh sách TextTag.
Đảm bảo tất cả MTEXT formatting codes bị loại bỏ.
"""

import re
from typing import List

from src.cad_parser.models import RawTextEntity
from src.text_extractor.models import TextTag


def strip_mtext_formatting(raw: str) -> str:
    """
    Loại bỏ các mã định dạng (formatting codes) của MTEXT.
    
    Ví dụ:
        '{\\fArial;PHONG NGU}' -> 'PHONG NGU'
        '\\PPHONG NGU' -> 'PHONG NGU'
    
    Args:
        raw: Chuỗi text gốc (có thể chứa MTEXT formatting).
        
    Returns:
        Chuỗi text đã được làm sạch và chuẩn hóa khoảng trắng.
    """
    if not raw:
        return ""

    # 1. Thay thế \P hoặc \p (MTEXT newline) và newline thực (\n) bằng khoảng trắng
    text = re.sub(r'(?i)\\p|\n', ' ', raw)

    # 2. Xóa các lệnh định dạng bắt đầu bằng '\' và kết thúc bằng ';'
    # Ví dụ: \fArial|b0|i0|c0|p34; hoặc \C1; hoặc \H1.5x;
    text = re.sub(r'\\[A-Za-z][^;]*;', '', text)

    # 3. Xóa các lệnh định dạng đơn giản (không có ';')
    # Ví dụ: \L (bắt đầu gạch dưới), \l (kết thúc gạch dưới), \O, \o, \W...
    text = re.sub(r'\\[LlOoKkXxWwA-Za-z]', '', text)

    # 4. Xóa các dấu ngoặc nhọn '{' và '}' (MTEXT grouping)
    text = re.sub(r'[{}]', '', text)

    # 5. Chuẩn hóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def process_text_entities(raw_entities: List[RawTextEntity]) -> List[TextTag]:
    """
    Chuyển đổi danh sách RawTextEntity thành TextTag.
    Áp dụng strip_mtext_formatting cho từng text entity.
    
    Args:
        raw_entities: Danh sách các entity chữ thô (có thể chứa MTEXT formatting).
        
    Returns:
        Danh sách các TextTag đã làm sạch (bỏ qua những text rỗng sau khi làm sạch).
    """
    tags: List[TextTag] = []
    for raw_ent in raw_entities:
        cleaned_text = strip_mtext_formatting(raw_ent.raw_content)
        if cleaned_text:  # Chỉ giữ lại các text có nội dung hợp lệ
            tags.append(
                TextTag(
                    content=cleaned_text,
                    position=raw_ent.position,
                    layer=raw_ent.layer,
                )
            )
    return tags
