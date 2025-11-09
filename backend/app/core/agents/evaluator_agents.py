"""
Evaluator Agents Module

This module contains evaluator agents that validate and assess the outputs
of decision-making agents in the decision workflow. Each evaluator agent
uses a specialized model to provide feedback and determine if the output
meets quality standards.

Evaluator agents use EvaluationOutput to provide:
- Boolean pass/fail status
- Detailed feedback
- Suggestions for improvement
"""

from pydantic_ai import Agent

from app.config import get_settings
from app.models.domain import EvaluationOutput
from app.utils.helpers import load_prompt


# Get settings to access evaluation model configuration
settings = get_settings()


# ============================================================================
# EVALUATOR AGENTS - Validate outputs from decision agents
# ============================================================================

# Identify Trigger Evaluator
# Validates that the trigger identification is clear, specific, and actionable
identify_trigger_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("identify_trigger_agent_evaluator.txt"),
)

# Root Cause Analyzer Evaluator
# Validates that root causes are logical, evidence-based, and comprehensive
root_cause_analyzer_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("root_cause_analyzer_agent_evaluator.txt"),
)

# Scope Definition Evaluator
# Validates that the scope is well-defined, realistic, and properly bounded
scope_definition_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("scope_definition_agent_evaluator.txt"),
)

# Drafting Evaluator
# Validates that the draft is structured, coherent, and addresses the problem
drafting_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("drafting_agent_evaluator.txt"),
)

# Establish Goals Evaluator
# Validates that goals are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
establish_goals_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("establish_goals_agent_evaluator.txt"),
)

# Identify Information Needed Evaluator
# Validates that information needs are specific, relevant, and obtainable
identify_information_needed_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("identify_information_needed_agent_evaluator.txt"),
)

# Draft Update Evaluator
# Validates that the updated draft incorporates feedback and shows improvement
draft_update_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("draft_update_agent_evaluator.txt"),
)

# Generation of Alternatives Evaluator
# Validates that alternatives are diverse, viable, and properly evaluated
generation_of_alternatives_agent_evaluator = Agent(
    model=settings.evaluation_model,
    output_type=EvaluationOutput,
    system_prompt=load_prompt("generation_of_alternatives_agent_evaluator.txt"),
)


# ============================================================================
# EVALUATOR REGISTRY
# ============================================================================

EVALUATOR_AGENTS = {
    "identify_trigger": identify_trigger_agent_evaluator,
    "root_cause_analyzer": root_cause_analyzer_agent_evaluator,
    "scope_definition": scope_definition_agent_evaluator,
    "drafting": drafting_agent_evaluator,
    "establish_goals": establish_goals_agent_evaluator,
    "identify_information_needed": identify_information_needed_agent_evaluator,
    "draft_update": draft_update_agent_evaluator,
    "generation_of_alternatives": generation_of_alternatives_agent_evaluator,
}


def get_evaluator(name: str) -> Agent:
    """
    Get an evaluator agent by name.
    
    Args:
        name: The evaluator name (e.g., "identify_trigger", "root_cause_analyzer")
        
    Returns:
        The requested evaluator agent instance
        
    Raises:
        KeyError: If the evaluator name is not found
    """
    if name not in EVALUATOR_AGENTS:
        available = ", ".join(EVALUATOR_AGENTS.keys())
        raise KeyError(
            f"Evaluator '{name}' not found. Available evaluators: {available}"
        )
    return EVALUATOR_AGENTS[name]


def list_evaluators() -> list[str]:
    """
    Get a list of all available evaluator names.
    
    Returns:
        List of evaluator names
    """
    return list(EVALUATOR_AGENTS.keys())
