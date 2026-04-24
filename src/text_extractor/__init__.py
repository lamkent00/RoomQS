"""
__init__.py — Text Extractor Module (MOD-06)
"""

from .models import TextTag
from .processor import process_text_entities, strip_mtext_formatting

__all__ = ["TextTag", "process_text_entities", "strip_mtext_formatting"]
