# This file includes the agent definitions for the multi agent decision making process

from pathlib import Path
from pydantic_ai import Agent, RunContext

from src.config import get_settings

# Get settings to access model configuration
settings = get_settings()

# Helper function to load system prompts from text files
def load_prompt(filename: str) -> str:
    """Load a system prompt from a text file."""
    prompt_path = Path(__file__).parent / "agent_system_prompts" / filename
    return prompt_path.read_text(encoding="utf-8")


# Identify Trigger Agent system prompt
identify_trigger_prompt = load_prompt("identify_trigger_agent.txt")

# Identify Trigger Agent
identify_trigger_agent = Agent(
    settings.model_name,
    system_prompt=identify_trigger_prompt,
)


# Root Cause Analyzer Agent system prompt
root_cause_analyzer_prompt = load_prompt("root_cause_analyzer_agent.txt")

# Root Cause Analyzer Agent
root_cause_analyzer_agent = Agent(
    settings.model_name,
    system_prompt=root_cause_analyzer_prompt,
)


# Scope Definition Agent system prompt
scope_definition_agent_prompt = load_prompt("scope_definition_agent.txt")

# Scope Definition Agent
scope_definition_agent = Agent(
    settings.model_name,
    system_prompt=scope_definition_agent_prompt,
)

# Drafting Agent system prompt
drafting_agent_prompt = load_prompt("drafting_agent.txt")

# Drafting Agent
drafting_agent = Agent(
    settings.model_name,
    system_prompt=drafting_agent_prompt,
)
