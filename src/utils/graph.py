# This file includes the graph definition for the multi agent decision making process

from pydantic_graph import Graph

from src.utils.agent_state import (
    GetDecision,
    IdentifyTrigger,
    AnalyzeRootCause,
    ScopeDefinition,
    Drafting,
    EstablishGoals,
    IdentifyInformationNeeded,
    UpdateDraft,
    GenerationOfAlternatives,
    Result
    )

from src.utils.evaluator_state import (
    Evaluate_IdentifyTrigger,       
    Evaluate_AnalyzeRootCause,
    Evaluate_ScopeDefinition,
    Evaluate_Drafting,
    Evaluate_EstablishGoals,
    Evaluate_IdentifyInformationNeeded,
    Evaluate_UpdateDraft,
    Evaluate_GenerationOfAlternatives,
    Evaluate_Result
    )

from src.utils.memory_state import DecisionState


# Defining the decision-making graph with nodes and state type
decision_graph = Graph(
    nodes=(GetDecision, IdentifyTrigger, Evaluate_IdentifyTrigger, AnalyzeRootCause,
           Evaluate_AnalyzeRootCause, ScopeDefinition, Evaluate_ScopeDefinition,
           Drafting, Evaluate_Drafting, EstablishGoals, Evaluate_EstablishGoals,
           IdentifyInformationNeeded, Evaluate_IdentifyInformationNeeded,
           UpdateDraft, Evaluate_UpdateDraft, GenerationOfAlternatives,
           Evaluate_GenerationOfAlternatives, Result, Evaluate_Result), state_type=DecisionState
)