"""
Agents Module

Contains all AI agents (decision agents and evaluator agents)
used in the decision-making workflow.
"""

from backend.app.core.agents.decision_agents import (
    DECISION_AGENTS,
    get_agent,
    identify_trigger_agent,
    root_cause_analyzer_agent,
    scope_definition_agent,
    drafting_agent,
    establish_goals_agent,
    identify_information_needed_agent,
    retrieve_information_needed_agent,
    draft_update_agent,
    generation_of_alternatives_agent,
    result_agent,
)

from backend.app.core.agents.evaluator_agents import (
    EVALUATOR_AGENTS,
    get_evaluator,
    list_evaluators,
    identify_trigger_agent_evaluator,
    root_cause_analyzer_agent_evaluator,
    scope_definition_agent_evaluator,
    drafting_agent_evaluator,
    establish_goals_agent_evaluator,
    identify_information_needed_agent_evaluator,
    draft_update_agent_evaluator,
    generation_of_alternatives_agent_evaluator,
)

__all__ = [
    # Decision agents
    "DECISION_AGENTS",
    "get_agent",
    "identify_trigger_agent",
    "root_cause_analyzer_agent",
    "scope_definition_agent",
    "drafting_agent",
    "establish_goals_agent",
    "identify_information_needed_agent",
    "retrieve_information_needed_agent",
    "draft_update_agent",
    "generation_of_alternatives_agent",
    "result_agent",
    # Evaluator agents
    "EVALUATOR_AGENTS",
    "get_evaluator",
    "list_evaluators",
    "identify_trigger_agent_evaluator",
    "root_cause_analyzer_agent_evaluator",
    "scope_definition_agent_evaluator",
    "drafting_agent_evaluator",
    "establish_goals_agent_evaluator",
    "identify_information_needed_agent_evaluator",
    "draft_update_agent_evaluator",
    "generation_of_alternatives_agent_evaluator",
]
