"""
Graph Nodes Module

This module contains all graph nodes (agent and evaluator nodes) that define 
the workflow for the decision-making process. Each node represents a step in 
the decision-making graph and handles both the agent execution and evaluation.

Node Types:
- Agent Nodes: Execute decision-making tasks using specialized agents
- Evaluator Nodes: Validate agent outputs and control workflow branching

The workflow follows this pattern:
1. GetDecision → IdentifyTrigger → Evaluate
2. AnalyzeRootCause → Evaluate
3. ScopeDefinition → Evaluate
4. Drafting → Evaluate
5. EstablishGoals → Evaluate
6. IdentifyInformationNeeded → Evaluate (with optional iteration)
7. UpdateDraft → Evaluate
8. GenerationOfAlternatives → Evaluate
9. Result → Evaluate → End
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from rich.prompt import Prompt

from pydantic_graph import BaseNode, End, GraphRunContext
from pydantic_ai import format_as_xml

from backend.app.models.domain import DecisionState, ResultOutput
from backend.app.core.agents.decision_agents import (
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
    identify_trigger_agent_evaluator,
    root_cause_analyzer_agent_evaluator,
    scope_definition_agent_evaluator,
    drafting_agent_evaluator,
    establish_goals_agent_evaluator,
    identify_information_needed_agent_evaluator,
    draft_update_agent_evaluator,
    generation_of_alternatives_agent_evaluator,
)


# ============================================================================
# AGENT NODES - Execute decision-making tasks
# ============================================================================


@dataclass
class GetDecision(BaseNode[DecisionState]):
    """
    Entry point node that captures the user's decision request.
    
    For CLI: Prompts the user interactively
    For API: Uses pre-populated decision_requested from state
    """
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> IdentifyTrigger:
        # Only prompt if decision_requested is not already set (for API usage)
        if not ctx.state.decision_requested:
            decision_query = Prompt.ask('What is the decision you want me to help?')
            ctx.state.decision_requested = decision_query
        return IdentifyTrigger()


@dataclass
class IdentifyTrigger(BaseNode[DecisionState]):
    """
    Identifies the trigger or catalyst for the decision request.
    Supports re-evaluation with feedback loop.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_IdentifyTrigger:
        base_prompt = f"Here the decision requested by user: {ctx.state.decision_requested}"
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            
        result = await identify_trigger_agent.run(prompt)
        return Evaluate_IdentifyTrigger(answer=result.output)


@dataclass
class AnalyzeRootCause(BaseNode[DecisionState]):
    """
    Analyzes the root cause of the identified trigger.
    Supports re-evaluation with feedback loop.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_AnalyzeRootCause:
        base_prompt = (
            f"Here the decision requested by user: {ctx.state.decision_requested}\n"
            f"Here the identified trigger: {ctx.state.trigger}"
        )
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            
        result = await root_cause_analyzer_agent.run(prompt)
        return Evaluate_AnalyzeRootCause(result.output)


@dataclass
class ScopeDefinition(BaseNode[DecisionState]):
    """
    Defines the scope and boundaries of the decision.
    Supports re-evaluation with feedback loop.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_ScopeDefinition:
        base_prompt = (
            f"Here the decision requested by user: {ctx.state.decision_requested}\n"
            f"Here the identified trigger: {ctx.state.trigger}\n"
            f"Here the root cause analysis: {ctx.state.root_cause}"
        )
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            
        result = await scope_definition_agent.run(prompt)
        return Evaluate_ScopeDefinition(result.output)


@dataclass
class Drafting(BaseNode[DecisionState]):
    """
    Creates initial draft of the decision based on previous analyses.
    Supports re-evaluation with feedback loop.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_Drafting:
        base_prompt = (
            f"Here the decision requested by user: {ctx.state.decision_requested}\n"
            f"Here the identified trigger: {ctx.state.trigger}\n"
            f"Here the root cause analysis: {ctx.state.root_cause}\n"
            f"Here the scope definition: {ctx.state.scope_definition}"
        )
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            print("\n\n Drafting Prompt: ", prompt)
            
        result = await drafting_agent.run(prompt)
        return Evaluate_Drafting(result.output)


@dataclass
class EstablishGoals(BaseNode[DecisionState]):
    """
    Establishes SMART goals for the decision.
    Supports re-evaluation with feedback loop.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_EstablishGoals:
        base_prompt = f"Here the decision requested by user: {ctx.state.decision_drafted}"
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            
        result = await establish_goals_agent.run(prompt)
        return Evaluate_EstablishGoals(result.output)


@dataclass
class IdentifyInformationNeeded(BaseNode[DecisionState]):
    """
    Identifies additional information needed for the decision.
    Supports re-evaluation with feedback loop and complementary info iteration.
    """
    
    evaluation: Optional[str] = None
    complementary_info: Optional[bool] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_IdentifyInformationNeeded:
        base_prompt = (
            f"Here the decision requested by user: {ctx.state.decision_drafted}\n"
            f"Here the established goals for the decision: {ctx.state.goals}"
        )
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        elif self.complementary_info:
            prompt = (
                f"{base_prompt}\n"
                f"Here the complementary info about the decision: {ctx.state.complementary_info}"
            )
        else:
            prompt = base_prompt
            
        result = await identify_information_needed_agent.run(prompt)
        return Evaluate_IdentifyInformationNeeded(result.output)


@dataclass
class UpdateDraft(BaseNode[DecisionState]):
    """
    Updates the decision draft with complementary information.
    Supports re-evaluation with feedback loop.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_UpdateDraft:
        base_prompt = f"Here the decision requested by user: {ctx.state.decision_drafted}"
        
        if ctx.state.complementary_info_num > 0:
            base_prompt += f"\nHere the complementary info for the decision: {ctx.state.complementary_info}"
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            
        result = await draft_update_agent.run(prompt)
        return Evaluate_UpdateDraft(result.output)


@dataclass
class GenerationOfAlternatives(BaseNode[DecisionState]):
    """
    Generates alternative options for the decision.
    Supports re-evaluation with feedback loop.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_GenerationOfAlternatives:
        base_prompt = f"Here the decision requested by user: {ctx.state.decision_draft_updated}"
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"Here the current alternatives for this decision: {ctx.state.alternatives}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            
        result = await generation_of_alternatives_agent.run(prompt)
        return Evaluate_GenerationOfAlternatives(result.output)


@dataclass
class Result(BaseNode[DecisionState]):
    """
    Evaluates and selects the best alternative for the decision.
    Produces final decision output with commentary.
    """
    
    evaluation: Optional[str] = None
    
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_Result:
        base_prompt = (
            f"Here the decision requested by user: {ctx.state.decision_draft_updated}\n"
            f"Here the current alternatives for this decision: {ctx.state.alternatives}"
        )
        
        if self.evaluation:
            prompt = (
                f"{base_prompt}\n"
                f"Here the selected result for the decision: {ctx.state.result}\n"
                f"Here the comment on selected result for the decision: {ctx.state.result_comment}\n"
                f"Here the selected best alternative for the decision: {ctx.state.best_alternative_result}\n"
                f"Here the comment on selected best alternative for the decision: {ctx.state.best_alternative_result_comment}\n"
                f"You gave an answer but that was not correct.\n"
                f"Here the evaluation comments from your previous wrong answer: {self.evaluation}\n"
                f"Please fix it and give the correct answer."
            )
        else:
            prompt = base_prompt
            
        result = await result_agent.run(prompt)
        return Evaluate_Result(result.output)


# ============================================================================
# EVALUATOR NODES - Validate outputs and control workflow
# ============================================================================


@dataclass
class Evaluate_IdentifyTrigger(BaseNode[DecisionState, None, str]):
    """
    Evaluates the identified trigger.
    If correct: updates state and proceeds to AnalyzeRootCause
    If incorrect: returns to IdentifyTrigger with feedback
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> IdentifyTrigger | AnalyzeRootCause:
        assert self.answer is not None
        
        result = await identify_trigger_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_requested,
                'identified trigger for the decision': self.answer
            })
        )
        
        if result.output.correct:
            ctx.state.trigger = self.answer
            print("#" * 50)
            print("\n Evaluate_IdentifyTrigger")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return AnalyzeRootCause()
        else:
            print("#" * 50)
            print("\n Evaluate_IdentifyTrigger")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return IdentifyTrigger(evaluation=result.output.comment)


@dataclass
class Evaluate_AnalyzeRootCause(BaseNode[DecisionState, None, str]):
    """
    Evaluates the root cause analysis.
    If correct: updates state and proceeds to ScopeDefinition
    If incorrect: returns to AnalyzeRootCause with feedback
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> AnalyzeRootCause | ScopeDefinition:
        assert self.answer is not None
        
        result = await root_cause_analyzer_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_requested,
                'identified trigger for the decision': ctx.state.trigger,
                'root cause analysis': self.answer
            })
        )
        
        if result.output.correct:
            ctx.state.root_cause = self.answer
            print("#" * 50)
            print("\n Evaluate_AnalyzeRootCause")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return ScopeDefinition()
        else:
            print("#" * 50)
            print("\n Evaluate_AnalyzeRootCause")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return AnalyzeRootCause(evaluation=result.output.comment)


@dataclass
class Evaluate_ScopeDefinition(BaseNode[DecisionState, None, str]):
    """
    Evaluates the scope definition.
    If correct: updates state and proceeds to Drafting
    If incorrect: returns to ScopeDefinition with feedback
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> ScopeDefinition | Drafting:
        assert self.answer is not None
        
        result = await scope_definition_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_requested,
                'identified trigger for the decision': ctx.state.trigger,
                'root cause analysis': ctx.state.root_cause,
                'scope definition': self.answer
            })
        )
        
        if result.output.correct:
            ctx.state.scope_definition = self.answer
            print("#" * 50)
            print("\n Evaluate_ScopeDefinition")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return Drafting()
        else:
            print("#" * 50)
            print("\n Evaluate_ScopeDefinition")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return ScopeDefinition(evaluation=result.output.comment)


@dataclass
class Evaluate_Drafting(BaseNode[DecisionState, None, str]):
    """
    Evaluates the decision draft.
    If correct: updates state and proceeds to EstablishGoals
    If incorrect: returns to Drafting with feedback
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> Drafting | EstablishGoals:
        assert self.answer is not None
        
        result = await drafting_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_requested,
                'identified trigger for the decision': ctx.state.trigger,
                'root cause analysis': ctx.state.root_cause,
                'scope definition': ctx.state.scope_definition,
                'decision drafted': self.answer
            })
        )
        
        if result.output.correct:
            ctx.state.decision_drafted = self.answer
            print("#" * 50)
            print("\n Evaluate_Drafting")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return EstablishGoals()
        else:
            print("#" * 50)
            print("\n Evaluate_Drafting")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return Drafting(evaluation=result.output.comment)


@dataclass
class Evaluate_EstablishGoals(BaseNode[DecisionState, None, str]):
    """
    Evaluates the established goals.
    If correct: updates state and proceeds to IdentifyInformationNeeded
    If incorrect: returns to EstablishGoals with feedback
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> EstablishGoals | IdentifyInformationNeeded:
        assert self.answer is not None
        
        result = await establish_goals_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_drafted
            })
        )
        
        if result.output.correct:
            ctx.state.goals = self.answer
            print("#" * 50)
            print("\n Evaluate_EstablishGoals")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return IdentifyInformationNeeded()
        else:
            print("#" * 50)
            print("\n Evaluate_EstablishGoals")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return EstablishGoals(evaluation=result.output.comment)


@dataclass
class Evaluate_IdentifyInformationNeeded(BaseNode[DecisionState, None, str]):
    """
    Evaluates the identified information needs.
    If correct OR max iterations (3): proceeds to UpdateDraft
    If incorrect: retrieves info and returns to IdentifyInformationNeeded
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> IdentifyInformationNeeded | UpdateDraft:
        assert self.answer is not None
        
        result = await identify_information_needed_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_drafted
            })
        )
        
        if result.output.correct or (ctx.state.complementary_info_num >= 3):
            print("#" * 50)
            print("\n Evaluate_IdentifyInformationNeeded")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return UpdateDraft()
        else:
            # Retrieve additional information
            info_needed = self.answer
            result = await retrieve_information_needed_agent.run(
                format_as_xml({
                    'decision requested': ctx.state.decision_drafted,
                    'info needed': info_needed
                })
            )
            ctx.state.complementary_info += "\n" + result.output
            ctx.state.complementary_info_num += 1
            print("#" * 50)
            print("\n Evaluate_IdentifyInformationNeeded")
            print("\n Information Retrieved Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output}\n")
            print("#" * 50 + "\n")
            return IdentifyInformationNeeded(complementary_info=True)


@dataclass
class Evaluate_UpdateDraft(BaseNode[DecisionState, None, str]):
    """
    Evaluates the updated draft.
    If correct: updates state and proceeds to GenerationOfAlternatives
    If incorrect: returns to UpdateDraft with feedback
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> UpdateDraft | GenerationOfAlternatives:
        assert self.answer is not None
        
        result = await draft_update_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_drafted
            })
        )
        
        if result.output.correct:
            ctx.state.decision_draft_updated = self.answer
            print("#" * 50)
            print("\n Evaluate_UpdateDraft")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return GenerationOfAlternatives()
        else:
            print("#" * 50)
            print("\n Evaluate_UpdateDraft")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return UpdateDraft(evaluation=result.output.comment)


@dataclass
class Evaluate_GenerationOfAlternatives(BaseNode[DecisionState, None, str]):
    """
    Evaluates the generated alternatives.
    If correct: updates state and proceeds to Result
    If incorrect: returns to GenerationOfAlternatives with feedback
    """
    
    answer: str
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> GenerationOfAlternatives | Result:
        assert self.answer is not None
        
        result = await generation_of_alternatives_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_drafted
            })
        )
        
        if result.output.correct:
            ctx.state.alternatives = self.answer
            print("#" * 50)
            print("\n Evaluate_GenerationOfAlternatives")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return Result()
        else:
            print("#" * 50)
            print("\n Evaluate_GenerationOfAlternatives")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nAnswer: {self.answer}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return GenerationOfAlternatives(evaluation=result.output.comment)


@dataclass
class Evaluate_Result(BaseNode[DecisionState, None, str]):
    """
    Evaluates the final decision result.
    If correct: updates state and ends the workflow
    If incorrect: returns to Result with feedback
    """
    
    answer: ResultOutput
    
    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> Result | End:
        assert self.answer is not None
        
        result = await draft_update_agent_evaluator.run(
            format_as_xml({
                'decision requested': ctx.state.decision_drafted
            })
        )
        
        if result.output.correct:
            ctx.state.result = self.answer.result
            ctx.state.result_comment = self.answer.result_comment
            ctx.state.best_alternative_result = self.answer.best_alternative_result
            ctx.state.best_alternative_result_comment = self.answer.best_alternative_result_comment
            return End(True)
        else:
            print("#" * 50)
            print("\n Evaluate_Result")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print(f"\nSelected Decision: {self.answer.result}\n\n")
            print(f"\nSelected Decision Comment: {self.answer.result_comment}\n\n")
            print(f"\nAlternative Decision: {self.answer.best_alternative_result}\n\n")
            print(f"\nAlternative Decision Comment: {self.answer.best_alternative_result_comment}\n\n")
            print(f"\nEvaluation: {result.output.comment}\n")
            print("#" * 50 + "\n")
            return Result(evaluation=result.output.comment)
