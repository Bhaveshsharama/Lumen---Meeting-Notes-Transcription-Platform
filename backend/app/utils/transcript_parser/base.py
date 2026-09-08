"""
utils/transcript_parser/base.py — Abstract Strategy for transcript parsers.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class TranscriptParser(ABC):
    @abstractmethod
    def parse(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Parses raw file bytes into a list of dictionaries.
        Each dict should match the TranscriptSegment model:
        {
            "sequence": int,
            "start_time": float,
            "end_time": float,
            "text": str
        }
        """
        pass
