# This file includes the evaluator states
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


# Evaluate_IdentifyTrigger state, it evaluates the identified trigger for the decision. 
# If the answer is correct, it updates the trigger attribute of the DecisionState and 
# proceeds to the AnalyzeRootCause state. If the answer is incorrect, it returns to the 
# IdentifyTrigger state with evaluation comments.
@dataclass
class Evaluate_IdentifyTrigger(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> IdentifyTrigger | AnalyzeRootCause:
        assert self.answer is not None
        result = await evaluate_identify_trigger_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_requested,
                           'identified trigger for the decision': self.answer})
        )
        if result.output.correct:
            ctx.state.trigger = self.answer
            print("#"*50)
            print("\n Evaluate_IdentifyTrigger")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return AnalyzeRootCause()
        else:
            print("#" * 50)
            print("\n Evaluate_IdentifyTrigger")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return IdentifyTrigger(evaluation = result.output.comment)
        

# Evaluate_AnalyzeRootCause state, it evaluates the analyzed root cause for the decision. 
# If the answer is correct, it updates the root_cause attribute of the DecisionState and 
# proceeds to the ScopeDefinition state. If the answer is incorrect, it returns to the 
# AnalyzeRootCause state with evaluation comments.
@dataclass
class Evaluate_AnalyzeRootCause(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> AnalyzeRootCause | ScopeDefinition:
        assert self.answer is not None
        result = await evaluate_root_cause_analyzer_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_requested,
                           'identified trigger for the decision': ctx.state.trigger,
                           'root cause analysis': self.answer})
        )
        if result.output.correct:
            ctx.state.root_cause = self.answer
            print("#" * 50)
            print("\n Evaluate_AnalyzeRootCause")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return ScopeDefinition()
        else:
            print("#" * 50)
            print("\n Evaluate_AnalyzeRootCause")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return AnalyzeRootCause(evaluation = result.output.comment)
        
        
# Evaluate_ScopeDefinition state, it evaluates the defined scope for the decision. 
# If the answer is correct, it updates the scope_definition attribute of the DecisionState and 
# proceeds to the Drafting state. If the answer is incorrect, it returns to the 
# ScopeDefinition state with evaluation comments.
@dataclass
class Evaluate_ScopeDefinition(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> ScopeDefinition | Drafting:
        assert self.answer is not None
        result = await evaluate_scope_definition_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_requested,
                           'identified trigger for the decision': ctx.state.trigger,
                           'root cause analysis': ctx.state.root_cause,
                           'scope definition': self.answer})
        )
        if result.output.correct:
            ctx.state.scope_definition = self.answer
            print("#" * 50)
            print("\n Evaluate_ScopeDefinition")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return Drafting()
        else:
            print("#" * 50)
            print("\n Evaluate_ScopeDefinition")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return ScopeDefinition(evaluation = result.output.comment)
        
        
# Evaluate_Drafting state, it evaluates the drafted decision. 
# If the answer is correct, it updates the decision_drafted attribute of the DecisionState and 
# proceeds to the EstablishGoals state. If the answer is incorrect, it returns to the 
# Drafting state with evaluation comments.
@dataclass
class Evaluate_Drafting(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> Drafting | EstablishGoals:
        assert self.answer is not None
        result = await evaluate_drafting_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_requested,
                           'identified trigger for the decision': ctx.state.trigger,
                           'root cause analysis': ctx.state.root_cause,
                           'scope definition': ctx.state.scope_definition,
                           'decision drafted': self.answer})
        )
        if result.output.correct:
            ctx.state.decision_drafted = self.answer
            print("#" * 50)
            print("\n Evaluate_Drafting")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return EstablishGoals()
        else:
            print("#" * 50)
            print("\n Evaluate_Drafting")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return Drafting(evaluation = result.output.comment)
        
        
# Evaluate_EstablishGoals state, it evaluates the established goals for the decision. 
# If the answer is correct, it updates the goals attribute of the DecisionState and 
# proceeds to the IdentifyInformationNeeded state. If the answer is incorrect, it returns to the 
# EstablishGoals state with evaluation comments.
@dataclass
class Evaluate_EstablishGoals(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> EstablishGoals | IdentifyInformationNeeded:
        assert self.answer is not None
        result = await evaluate_establish_goals_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_drafted})
        )
        if result.output.correct:
            ctx.state.goals = self.answer
            print("#" * 50)
            print("\n Evaluate_EstablishGoals")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return IdentifyInformationNeeded()
        else:
            print("#" * 50)
            print("\n Evaluate_EstablishGoals")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return EstablishGoals(evaluation = result.output.comment)
        

# Evaluate_IdentifyInformationNeeded state, it evaluates the identified information needed for the decision. 
# If the answer is correct, it proceeds to the UpdateDraft state. If the answer is incorrect, 
# it retrieves the needed information and updates the complementary_info attribute of the DecisionState,
# then returns to the IdentifyInformationNeeded state.
@dataclass
class Evaluate_IdentifyInformationNeeded(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> IdentifyInformationNeeded | UpdateDraft:
        assert self.answer is not None
        result = await evaluate_identify_information_needed_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_drafted})
        )
        if result.output.correct or (ctx.state.complementary_info_num >= 3):
            print("#" * 50)
            print("\n Evaluate_IdentifyInformationNeeded")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return UpdateDraft()
        else:
            info_needed = self.answer
            result = await retrieve_information_needed_agent.run(
                format_as_xml({'decision requested': ctx.state.decision_drafted,
                               'info needed': info_needed})
            )
            ctx.state.complementary_info += "\n" + result.output
            ctx.state.complementary_info_num += 1
            print("#" * 50)
            print("\n Evaluate_IdentifyInformationNeeded")
            print("\n Information Retrieved Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output + "\n")
            print("#" * 50 + "\n")
            return IdentifyInformationNeeded(complementary_info=True)
        
        
# Evaluate_UpdateDraft state, it evaluates the updated draft of the decision. 
# If the answer is correct, it updates the decision_draft_updated attribute of the DecisionState and 
# proceeds to the GenerationOfAlternatives state. If the answer is incorrect, it returns to the 
# UpdateDraft state with evaluation comments.
@dataclass
class Evaluate_UpdateDraft(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> UpdateDraft | GenerationOfAlternatives:
        assert self.answer is not None
        result = await evaluate_draft_update_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_drafted})
        )
        if result.output.correct:
            ctx.state.decision_draft_updated = self.answer
            print("#" * 50)
            print("\n Evaluate_UpdateDraft")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return GenerationOfAlternatives()
        else:
            print("#" * 50)
            print("\n Evaluate_UpdateDraft")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return UpdateDraft(evaluation = result.output.comment)
        
        
# Evaluate_GenerationOfAlternatives state, it evaluates the generated alternatives for the decision. 
# If the answer is correct, it updates the alternatives attribute of the DecisionState and 
# proceeds to the Result state. If the answer is incorrect, it returns to the 
# GenerationOfAlternatives state with evaluation comments.
@dataclass
class Evaluate_GenerationOfAlternatives(BaseNode[DecisionState, None, str]):
    answer: str

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> GenerationOfAlternatives | Result:
        assert self.answer is not None
        result = await evaluate_draft_update_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_drafted})
        )
        if result.output.correct:
            ctx.state.alternatives = self.answer
            print("#" * 50)
            print("\n Evaluate_GenerationOfAlternatives")
            print("\n Correct Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return Result()
        else:
            print("#" * 50)
            print("\n Evaluate_GenerationOfAlternatives")
            print("\n Wrong Answer \n")
            print("#" * 50 + "\n")
            print("\nAnswer: " + self.answer + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return GenerationOfAlternatives(evaluation = result.output.comment)
        
        
# Evaluate_Result state, it evaluates the final decision result. 
# If the answer is correct, it updates the result attributes of the DecisionState and 
# ends the decision-making process. If the answer is incorrect, it returns to the 
# Result state with evaluation comments.
@dataclass
class Evaluate_Result(BaseNode[DecisionState, None, str]):
    answer: ResultOutput

    async def run(
        self,
        ctx: GraphRunContext[DecisionState],
    ) -> Result | End:
        assert self.answer is not None
        result = await evaluate_draft_update_agent.run(
            format_as_xml({'decision requested': ctx.state.decision_drafted})
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
            print("\nSelected Decision: " + self.answer.result + "\n\n")
            print("\nSelected Decision Comment: " + self.answer.result_comment + "\n\n")
            print("\nAlternative Decision: " + self.answer.best_alternative_result + "\n\n")
            print("\nAlternative Decision Comment: " + self.answer.best_alternative_result_comment + "\n\n")
            print("\nEvaluation: " + result.output.comment + "\n")
            print("#" * 50 + "\n")
            return Result(evaluation = result.output.comment)