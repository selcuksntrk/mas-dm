"""
Graph Module

Contains the graph definition, nodes, and execution logic for the
multi-agent decision-making workflow.
"""

from app.core.graph.executor import (
    decision_graph,
    run_decision_graph,
    get_graph_mermaid,
    get_graph_structure,
)

from app.core.graph.nodes import (
    # Agent nodes
    GetDecision,
    IdentifyTrigger,
    AnalyzeRootCause,
    ScopeDefinition,
    Drafting,
    EstablishGoals,
    IdentifyInformationNeeded,
    UpdateDraft,
    GenerationOfAlternatives,
    Result,
    # Evaluator nodes
    Evaluate_IdentifyTrigger,
    Evaluate_AnalyzeRootCause,
    Evaluate_ScopeDefinition,
    Evaluate_Drafting,
    Evaluate_EstablishGoals,
    Evaluate_IdentifyInformationNeeded,
    Evaluate_UpdateDraft,
    Evaluate_GenerationOfAlternatives,
    Evaluate_Result,
)

__all__ = [
    # Graph execution
    "decision_graph",
    "run_decision_graph",
    "get_graph_mermaid",
    "get_graph_structure",
    # Agent nodes
    "GetDecision",
    "IdentifyTrigger",
    "AnalyzeRootCause",
    "ScopeDefinition",
    "Drafting",
    "EstablishGoals",
    "IdentifyInformationNeeded",
    "UpdateDraft",
    "GenerationOfAlternatives",
    "Result",
    # Evaluator nodes
    "Evaluate_IdentifyTrigger",
    "Evaluate_AnalyzeRootCause",
    "Evaluate_ScopeDefinition",
    "Evaluate_Drafting",
    "Evaluate_EstablishGoals",
    "Evaluate_IdentifyInformationNeeded",
    "Evaluate_UpdateDraft",
    "Evaluate_GenerationOfAlternatives",
    "Evaluate_Result",
]
