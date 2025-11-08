"""
Domain Models - Core business entities

These represent the core concepts in your application domain.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class DecisionState(BaseModel):
    """
    State object that tracks the decision-making process
    
    This is passed through the entire graph execution
    and accumulates information at each step.
    
    WHY PYDANTIC INSTEAD OF DATACLASS:
    - Automatic validation
    - JSON serialization/deserialization
    - Better integration with FastAPI and Pydantic AI
    - Type coercion (strings to ints, etc.)
    - Immutability options (frozen=True)
    """
    
    model_config = ConfigDict(
        # Allow arbitrary types (for complex objects)
        arbitrary_types_allowed=True,
        # Validate on assignment (catch errors early)
        validate_assignment=True,
        # Use enum values instead of enum objects in JSON
        use_enum_values=True,
    )
    
    # User Input
    decision_requested: str = Field(
        default="",
        description="The original decision query from the user"
    )
    
    # Analysis Phase
    trigger: str = Field(
        default="",
        description="Identified trigger for the decision (opportunity, problem, crisis)"
    )
    
    root_cause: str = Field(
        default="",
        description="Root cause analysis using 5 Whys or Fishbone"
    )
    
    scope_definition: str = Field(
        default="",
        description="Defined scope of the decision (what's in/out of scope)"
    )
    
    # Drafting Phase
    decision_drafted: str = Field(
        default="",
        description="Initial drafted decision document"
    )
    
    goals: str = Field(
        default="",
        description="Established goals and success metrics (SMART format)"
    )
    
    stakeholders: str = Field(
        default="",
        description="Identified stakeholders and their interests"
    )
    
    # Information Gathering
    complementary_info: str = Field(
        default="",
        description="Additional information gathered to inform decision"
    )
    
    complementary_info_num: int = Field(
        default=0,
        ge=0,  # Greater than or equal to 0
        description="Number of information items gathered"
    )
    
    # Refinement Phase
    decision_draft_updated: str = Field(
        default="",
        description="Updated decision draft after information gathering"
    )
    
    generated_alternatives: str = Field(
        default="",
        description="Generated alternative options"
    )
    
    alternatives: str = Field(
        default="",
        description="Formatted alternatives with evaluation criteria"
    )
    
    # Final Results
    result: str = Field(
        default="",
        description="The selected decision option"
    )
    
    result_comment: str = Field(
        default="",
        description="Explanation of why this option was selected"
    )
    
    best_alternative_result: str = Field(
        default="",
        description="The best alternative option (runner-up)"
    )
    
    best_alternative_result_comment: str = Field(
        default="",
        description="Explanation of the alternative option"
    )


class ResultOutput(BaseModel):
    """
    Output structure for the final decision result.
    Used by the result agent to return structured decision information.
    """
    
    model_config = ConfigDict(
        use_attribute_docstrings=True,
        json_schema_extra={
            "example": {
                "result": "Implement Redis persistence with Repository Pattern",
                "best_alternative_result": "Use PostgreSQL with SQLAlchemy ORM",
                "result_comment": "Redis provides faster access and simpler setup for our use case",
                "best_alternative_result_comment": "PostgreSQL would offer more complex querying but is overkill"
            }
        }
    )
    
    result: str = Field(
        ...,
        description="The selected option for the decision"
    )
    
    best_alternative_result: str = Field(
        ...,
        description="The best alternative option for the decision"
    )
    
    result_comment: str = Field(
        ...,
        description="Comment on the selection of the result"
    )
    
    best_alternative_result_comment: str = Field(
        ...,
        description="Comment on the selection of the best alternative to result"
    )


class EvaluationOutput(BaseModel):
    """
    Output structure for agent evaluations.
    Used by evaluator agents to provide feedback on agent outputs.
    """
    
    model_config = ConfigDict(
        use_attribute_docstrings=True,
        json_schema_extra={
            "example": {
                "correct": True,
                "comment": "The root cause analysis properly identified the underlying issue using 5 Whys technique"
            }
        }
    )
    
    correct: bool = Field(
        ...,
        description="Whether the answer is correct"
    )
    
    comment: str = Field(
        ...,
        min_length=10,
        description="Comment on the answer with specific feedback"
    )


class ProcessInfo(BaseModel):
    """
    Information about a running decision-making process
    
    WHY PYDANTIC INSTEAD OF DATACLASS:
    - Validation when loading from Redis
    - Consistent serialization format
    - Integration with repository pattern
    """
    
    model_config = ConfigDict(
        # Validate default values
        validate_default=True,
        # Strict type checking
        str_strip_whitespace=True,
    )
    
    process_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier for the process"
    )
    
    status: str = Field(
        ...,
        pattern="^(pending|running|completed|failed)$",
        description="Process status: pending, running, completed, or failed"
    )
    
    result: Optional[DecisionState] = Field(
        default=None,
        description="The complete decision state (only when completed)"
    )
    
    error: Optional[str] = Field(
        default=None,
        description="Error message if process failed"
    )
    
    created_at: Optional[str] = Field(
        default=None,
        description="ISO format timestamp when process was created"
    )
    
    completed_at: Optional[str] = Field(
        default=None,
        description="ISO format timestamp when process completed"
    )
