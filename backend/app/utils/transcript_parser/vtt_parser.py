"""
utils/transcript_parser/vtt_parser.py — Simple parser for .vtt subtitle files.
"""
import re
from typing import List, Dict, Any
from .base import TranscriptParser
from app.core.exceptions import ValidationError

# Pattern: "Speaker Name: rest of text"
_SPEAKER_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*):\s*(.+)$")

class VttParser(TranscriptParser):
    def _parse_time(self, time_str: str) -> float:
        """Converts HH:MM:SS.mmm or MM:SS.mmm to seconds."""
        parts = time_str.split(":")
        if len(parts) == 3:
            h, m, s = parts
        elif len(parts) == 2:
            h = 0
            m, s = parts
        else:
            raise ValueError(f"Unexpected time format: {time_str!r}")
        return int(h) * 3600 + int(m) * 60 + float(s)

    def parse(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        # Normalize line endings to LF so split works on Windows-saved files
        text = file_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")

        if not text.startswith("WEBVTT"):
            raise ValidationError("Invalid VTT format: missing WEBVTT header")

        time_pattern = re.compile(
            r"(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})"
            r"\s+-->\s+"
            r"(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})"
        )

        segments: List[Dict[str, Any]] = []
        sequence = 1

        # Split on blank lines — works now that endings are normalised
        for block in text.split("\n\n"):
            block = block.strip()
            if not block:
                continue

            lines = block.split("\n")

            # Locate the timestamp line
            time_match = None
            content_start = 0
            for i, line in enumerate(lines):
                m = time_pattern.search(line)
                if m:
                    time_match = m
                    content_start = i + 1
                    break

            if not time_match or content_start >= len(lines):
                continue

            start = self._parse_time(time_match.group(1))
            end = self._parse_time(time_match.group(2))
            raw_content = " ".join(lines[content_start:]).strip()

            if not raw_content:
                continue

            # Extract speaker from "Speaker: text" format
            speaker_id = None
            text_content = raw_content
            speaker_match = _SPEAKER_RE.match(raw_content)
            if speaker_match:
                speaker_id = speaker_match.group(1).strip()
                text_content = speaker_match.group(2).strip()

            segments.append({
                "sequence": sequence,
                "start_time": start,
                "end_time": end,
                "speaker_id": speaker_id,
                "text": text_content,
            })
            sequence += 1

        return segments
