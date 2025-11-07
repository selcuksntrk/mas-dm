# Helper functions
from pathlib import Path


def load_prompt(filename: str) -> str:
    """Load a system prompt from a text file."""
    prompt_path = Path(__file__).parent / "system_prompts" / filename
    return prompt_path.read_text(encoding="utf-8")