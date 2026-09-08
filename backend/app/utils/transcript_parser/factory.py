"""
utils/transcript_parser/factory.py — Factory choosing parser by format.
"""
from typing import Type
from .base import TranscriptParser
from .txt_parser import TxtParser
from .vtt_parser import VttParser
from .json_parser import JsonParser
from app.core.exceptions import ValidationError

class ParserFactory:
    _parsers = {
        "txt": TxtParser,
        "vtt": VttParser,
        "json": JsonParser
    }

    @classmethod
    def get_parser(cls, format: str) -> TranscriptParser:
        format = format.lower()
        parser_cls = cls._parsers.get(format)
        if not parser_cls:
            raise ValidationError(f"Unsupported format: {format}")
        return parser_cls()
