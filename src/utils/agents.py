# This file includes the agent definitions for the multi agent decision making process

from pydantic_ai import Agent, RunContext

from src.config import get_settings
from src.utils.result_output_state import ResultOutput
from src.utils.helpers import load_prompt


# Get settings to access model configuration
settings = get_settings()




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


# Establish Goals Agent system prompt
establish_goals_agent_prompt = load_prompt("establish_goals_agent.txt")

# Establish Goals Agent
establish_goals_agent = Agent(
    settings.model_name,
    system_prompt=establish_goals_agent_prompt,
)


# Generate Alternative Agents system prompt
generate_alternative_agents_prompt = load_prompt("generate_alternative_agents.txt")

# Generate Alternative Agents
generate_alternative_agents = Agent(
    settings.model_name,
    system_prompt=generate_alternative_agents_prompt,
)


# Identify Information Needed Agent system prompt
identify_information_needed_agent_prompt = load_prompt("identify_information_needed_agent.txt")

# Identify Information Needed Agent
identify_information_needed_agent = Agent(
    settings.model_name,
    system_prompt=identify_information_needed_agent_prompt,
)


# Retrieve Information Needed Agent system prompt
retrieve_information_needed_agent_prompt = load_prompt("retrieve_information_needed_agent.txt")

# Retrieve Information Needed Agent
retrieve_information_needed_agent = Agent(
    settings.model_name,
    system_prompt=retrieve_information_needed_agent_prompt,
)


# Draft Update Agent system prompt
draft_update_agent_prompt = load_prompt("draft_update_agent.txt")

# Draft Update Agent
draft_update_agent = Agent(
    settings.model_name,
    system_prompt=draft_update_agent_prompt,
)


# Generation of Alternatives Agent system prompt
generation_of_alternatives_agent_prompt = load_prompt("generation_of_alternatives_agent.txt")

# Generation of Alternatives Agent
generation_of_alternatives_agent = Agent(
    settings.model_name,
    system_prompt=generation_of_alternatives_agent_prompt,
)


# Result Agent system prompt
result_agent_prompt = load_prompt("result_agent.txt")

# Result Agent
result_agent = Agent(
    settings.model_name,
    system_prompt=result_agent_prompt,
    output_tyepe=ResultOutput,
)