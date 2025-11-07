# This module defines the ResultOutput model used to represent the output 
# state of a decision-making process.
from groq import BaseModel



# Defining the ResultOutput model with relevant fields and descriptions
class ResultOutput(BaseModel, use_attribute_docstrings=True):
    result: str
    """The selected option for the decision"""
    best_alternative_result: str
    """The best alternative option for the decision"""
    result_comment: str
    """Comment on the selection of the result"""
    best_alternative_result_comment: str
    """Comment on the selection of the best alternative to result"""