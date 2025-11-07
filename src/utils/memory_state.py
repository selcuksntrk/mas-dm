#This file includes the memory state dataclass for decision making process

#Importing necessary modules
from dataclasses import dataclass




@dataclass
class DecisionState:
    decision_requested: str = ""
    trigger: str = ""
    root_cause: str = ""
    scope_definition: str = ""
    decision_drafted: str = ""
    goals: str = ""
    stakeholders: str = ""
    generated_alternatives: str = ""
    complementary_info: str = ""
    complementary_info_num: int = 0
    decision_draft_updated: str = ""
    alternatives: str = ""
    result: str = ""
    result_comment: str = ""
    best_alternative_result: str = ""
    best_alternative_result_comment: str = ""