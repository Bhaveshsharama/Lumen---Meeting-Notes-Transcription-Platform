"""
utils/transcript_parser/json_parser.py — Simple parser for pre-structured .json transcripts.
"""
import json
from typing import List, Dict, Any
from .base import TranscriptParser
from app.core.exceptions import ValidationError

class JsonParser(TranscriptParser):
    def parse(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        try:
            data = json.loads(file_bytes)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format")
            
        if not isinstance(data, list):
            raise ValidationError("JSON body must be an array of segments")
            
        segments = []
        for i, item in enumerate(data):
            try:
                segments.append({
                    "sequence": i + 1,
                    "start_time": float(item["start_time"]),
                    "end_time": float(item["end_time"]),
                    "text": str(item["text"])
                })
            except (KeyError, ValueError):
                raise ValidationError(f"Segment at index {i} is missing required fields or has invalid types")
                
        return segments
