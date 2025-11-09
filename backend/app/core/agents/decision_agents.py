"""
Decision-Making Agents

These agents handle the various stages of the decision-making process,
from identifying triggers to generating alternatives and selecting the best option.
"""

from pydantic_ai import Agent
from app.config import get_settings
from app.models.domain import ResultOutput
from app.utils.helpers import load_prompt


# Get application settings
settings = get_settings()


# ============================================================================
# ANALYSIS AGENTS - Understand the decision context
# ============================================================================

# Identify Trigger Agent
# Purpose: Identify what triggered the need for this decision
identify_trigger_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("identify_trigger_agent.txt"),
)


# Root Cause Analyzer Agent
# Purpose: Analyze the underlying root cause of the decision trigger
root_cause_analyzer_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("root_cause_analyzer_agent.txt"),
)


# Scope Definition Agent
# Purpose: Define the boundaries and scope of the decision
scope_definition_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("scope_definition_agent.txt"),
)


# ============================================================================
# DRAFTING AGENTS - Create the initial decision framework
# ============================================================================

# Drafting Agent
# Purpose: Draft the initial decision based on analysis
drafting_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("drafting_agent.txt"),
)


# Establish Goals Agent
# Purpose: Define clear goals for the decision
establish_goals_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("establish_goals_agent.txt"),
)


# ============================================================================
# INFORMATION AGENTS - Gather and process additional information
# ============================================================================

# Identify Information Needed Agent
# Purpose: Determine what additional information is needed
identify_information_needed_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("identify_information_needed_agent.txt"),
)


# Retrieve Information Needed Agent
# Purpose: Retrieve and synthesize the needed information
retrieve_information_needed_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("retrieve_information_needed_agent.txt"),
)


# Draft Update Agent
# Purpose: Update the decision draft with new information
draft_update_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("draft_update_agent.txt"),
)


# ============================================================================
# ALTERNATIVE GENERATION AGENTS - Explore options
# ============================================================================

# Generation of Alternatives Agent
# Purpose: Generate alternative options for the decision
generation_of_alternatives_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("generation_of_alternatives_agent.txt"),
)


# ============================================================================
# RESULT AGENTS - Finalize the decision
# ============================================================================

# Result Agent
# Purpose: Evaluate all options and select the best decision
result_agent = Agent(
    model=settings.model_name,
    system_prompt=load_prompt("result_agent.txt"),
    output_type=ResultOutput,
)


# ============================================================================
# AGENT REGISTRY - For easy access and management
# ============================================================================

DECISION_AGENTS = {
    "identify_trigger": identify_trigger_agent,
    "root_cause_analyzer": root_cause_analyzer_agent,
    "scope_definition": scope_definition_agent,
    "drafting": drafting_agent,
    "establish_goals": establish_goals_agent,
    "identify_information_needed": identify_information_needed_agent,
    "retrieve_information_needed": retrieve_information_needed_agent,
    "draft_update": draft_update_agent,
    "generation_of_alternatives": generation_of_alternatives_agent,
    "result": result_agent,
}


def get_agent(agent_name: str) -> Agent:
    """
    Get an agent by name.
    
    Args:
        agent_name: Name of the agent to retrieve
        
    Returns:
        The requested agent instance
        
    Raises:
        KeyError: If agent name is not found
        
    Example:
        >>> agent = get_agent("identify_trigger")
    """
    if agent_name not in DECISION_AGENTS:
        available = ", ".join(DECISION_AGENTS.keys())
        raise KeyError(
            f"Agent '{agent_name}' not found. "
            f"Available agents: {available}"
        )
    return DECISION_AGENTS[agent_name]
