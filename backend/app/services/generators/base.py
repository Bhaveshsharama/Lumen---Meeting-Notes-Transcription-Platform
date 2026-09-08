"""
services/generators/base.py — Abstract strategy for Summary Generation.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class SummaryGenerator(ABC):
    @abstractmethod
    def generate(self, transcript_text: str) -> Dict[str, Any]:
        """
        Takes raw transcript text and returns a dict with:
        {
            "overview": str,
            "topics": [{"title": str, "start_time": float}],
            "action_items": [{"text": str, "source_timestamp": float}]
        }
        """
        pass
