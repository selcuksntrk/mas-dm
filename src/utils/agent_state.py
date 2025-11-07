# This file includes the agent states
from dataclasses import dataclass

from rich.prompt import Prompt

from pydantic_graph import (
    BaseNode,
    End,
    Graph,
    GraphRunContext,
)

from utils.agents import *
from src.utils.memory_state import DecisionState


# GetDecision state, it prompts the user for the decision they want help with and
# stores it in the decision_requested attribute of the DecisionState.
@dataclass
class GetDecision(BaseNode[DecisionState]):
    async def run(self, ctx: GraphRunContext[DecisionState]) -> IdentifyTrigger:
        decision_query = Prompt.ask('What is the decision you want me to help?')
        ctx.state.decision_requested = decision_query
        return IdentifyTrigger()
    

# IdentifyTrigger state, it uses the identify_trigger_agent to identify the trigger for the decision.
@dataclass
class IdentifyTrigger(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_IdentifyTrigger:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await identify_trigger_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            result = await identify_trigger_agent.run(prompt)

        return Evaluate_IdentifyTrigger(answer=result.output)
    
    
# AnalyzeRootCause state, it uses the root_cause_analyzer_agent to 
# analyze the root cause of the decision trigger.
@dataclass
class AnalyzeRootCause(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_AnalyzeRootCause:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            prompt += "\n Here the identified trigger: " + ctx.state.trigger
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await root_cause_analyzer_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            prompt += "\n Here the identified trigger: " + ctx.state.trigger
            result = await root_cause_analyzer_agent.run(prompt)

        return Evaluate_AnalyzeRootCause(result.output)
    

# ScopeDefinition state, it uses the scope_definition_agent to 
# define the scope of the decision.
@dataclass
class ScopeDefinition(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_ScopeDefinition:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            prompt += "\n Here the identified trigger: " + ctx.state.trigger
            prompt += "\n Here the root cause analysis: " + ctx.state.root_cause
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " +  self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await scope_definition_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            prompt += "\n Here the identified trigger: " + ctx.state.trigger
            prompt += "\n Here the root cause analysis: " + ctx.state.root_cause
            result = await scope_definition_agent.run(prompt)

        return Evaluate_ScopeDefinition(result.output)
    
    
# Drafting state, it uses the drafting_agent to 
# draft the decision based on the previous analyses.
@dataclass
class Drafting(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_Drafting:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            prompt += "\n Here the identified trigger: " + ctx.state.trigger
            prompt += "\n Here the root cause analysis: " + ctx.state.root_cause
            prompt += "\n Here the scope definition: " + ctx.state.scope_definition
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await drafting_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_requested
            prompt += "\nHere the identified trigger: " + ctx.state.trigger
            prompt += "\nHere the root cause analysis: " + ctx.state.root_cause
            prompt += "\nHere the scope definition: " + ctx.state.scope_definition
            print("\n\n Drafting Prompt: ", prompt)
            result = await drafting_agent.run(prompt)

        return Evaluate_Drafting(result.output)
    

# EstablishGoals state, it uses the establish_goals_agent to 
# establish the goals for the decision.
@dataclass
class EstablishGoals(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_EstablishGoals:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_drafted
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await establish_goals_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_drafted
            result = await establish_goals_agent.run(prompt)

        return Evaluate_EstablishGoals(result.output)


# IdentifyInformationNeeded state, it uses the identify_information_needed_agent to 
# identify the information needed to make the decision.
@dataclass
class IdentifyInformationNeeded(BaseNode[DecisionState]):
    evaluation: str | None = None
    complementary_info: bool | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_IdentifyInformationNeeded:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_drafted
            prompt += "\n Here the established goals for the decision: " + ctx.state.goals
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await identify_information_needed_agent.run(prompt)
        elif self.complementary_info is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_drafted
            prompt += "\n Here the complementary info about the decision: " + ctx.state.complementary_info
            prompt += "\n Here the established goals for the decision: " + ctx.state.goals
            result = await identify_information_needed_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_drafted
            prompt += "\n Here the established goals for the decision: " + ctx.state.goals
            result = await identify_information_needed_agent.run(prompt)

        return Evaluate_IdentifyInformationNeeded(result.output)
    
    
# UpdateDraft state, it uses the draft_update_agent to 
# update the decision draft based on the complementary information.
@dataclass
class UpdateDraft(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_UpdateDraft:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_drafted
            if ctx.state.complementary_info_num > 0:
                prompt += "\n Here the complementary info for the decision: " + ctx.state.complementary_info
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await draft_update_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_drafted
            if ctx.state.complementary_info_num > 0:
                prompt += "\n Here the complementary info for the decision: " + ctx.state.complementary_info
            result = await draft_update_agent.run(prompt)

        return Evaluate_UpdateDraft(result.output)
    

# GenerationOfAlternatives state, it uses the generation_of_alternatives_agent to 
# generate alternatives for the decision.
@dataclass
class GenerationOfAlternatives(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_GenerationOfAlternatives:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_draft_updated
            prompt += "\n Here the current alternatives for this decision: " + ctx.state.alternatives
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await generation_of_alternatives_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_draft_updated
            result = await generation_of_alternatives_agent.run(prompt)

        return Evaluate_GenerationOfAlternatives(result.output)
    

# Result state, it uses the result_agent to 
# evaluate and select the best alternative for the decision.
@dataclass
class Result(BaseNode[DecisionState]):
    evaluation: str | None = None
    async def run(self, ctx: GraphRunContext[DecisionState]) -> Evaluate_Result:
        if self.evaluation is not None:
            prompt = "Here the decision requested by user: " + ctx.state.decision_draft_updated
            prompt += "\n Here the current alternatives for this decision: " + ctx.state.alternatives
            prompt += "\n Here the selected result for the decision: " + ctx.state.result
            prompt += "\n Here the comment on selected result for the decision: " + ctx.state.result_comment
            prompt += "\n Here the selected best alternative for the decision: " + ctx.state.best_alternative_result
            prompt += "\n Here the comment on selected best alternative for the decision: " + ctx.state.best_alternative_result_comment
            prompt += "\n you gave an answer but that was not correct. "
            prompt += "\n here the evaluation comments from your previous wrong answer: " + self.evaluation
            prompt += "\n Please fix it and give the correct answer."
            result = await result_agent.run(prompt)
        else:
            prompt = "Here the decision requested by user: " + ctx.state.decision_draft_updated
            prompt += "\n Here the current alternatives for this decision: " + ctx.state.alternatives
            result = await result_agent.run(prompt)

        return Evaluate_Result(result.output)