"""
utils/transcript_parser/txt_parser.py — Simple split-based parser for .txt files.
"""
from typing import List, Dict, Any
from .base import TranscriptParser
from app.core.exceptions import ValidationError

class TxtParser(TranscriptParser):
    def parse(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise ValidationError("File must be valid UTF-8 text.")
            
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        segments = []
        # Assign arbitrary sequential timestamps for plain text where timing isn't available
        for i, line in enumerate(lines):
            segments.append({
                "sequence": i + 1,
                "start_time": float(i * 10),
                "end_time": float((i + 1) * 10),
                "text": line
            })
        return segments
