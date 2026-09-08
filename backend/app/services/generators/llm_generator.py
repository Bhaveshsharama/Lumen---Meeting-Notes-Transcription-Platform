"""
services/generators/llm_generator.py — Groq LLM integration.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from groq import Groq
from .base import SummaryGenerator
from .mock_generator import MockSummaryGenerator

# Load .env from backend/ directory
_backend_dir = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(dotenv_path=_backend_dir / ".env", override=True)


class LLMSummaryGenerator(SummaryGenerator):
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY", "").strip()
        self.mock_fallback = MockSummaryGenerator()
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def generate(self, transcript_text: str) -> Dict[str, Any]:
        if not self.api_key:
            print("Warning: GROQ_API_KEY missing. Falling back to Mock generator.")
            return self.mock_fallback.generate(transcript_text)

        prompt = f"""Extract the following information from the meeting transcript below and format your response EXCLUSIVELY as valid, parsable JSON matching this schema:
{{
    "overview": "A 2-3 sentence overall summary.",
    "topics": [{{"title": "Chapter name", "start_time": 0.0}}],
    "action_items": [{{"text": "Task description", "source_timestamp": 0.0}}]
}}

Transcript:
{transcript_text}"""

        try:
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a specialized JSON meeting summarizer. Output ONLY raw JSON, with no markdown codeblocks or preamble."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                stream=True,
                stop=None,
            )

            response_text = ""
            for chunk in completion:
                response_text += chunk.choices[0].delta.content or ""

            response_text = response_text.strip()
            # Strip markdown code fences if the model wraps its response
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                    
            return json.loads(response_text)

        except Exception as e:
            print(f"LLM Generation failed: {e}. Falling back to mock.")
            return self.mock_fallback.generate(transcript_text)
