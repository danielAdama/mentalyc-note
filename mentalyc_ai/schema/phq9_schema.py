from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Sequence, Tuple, TypedDict, Union, Any, Dict
from typing import Literal

class PHQ9Output(BaseModel):
    phq_9_scoring_table: Dict[str, int] = Field(..., description="A table mapping the client's symptoms and corresponding responses to the nine PHQ-9 items.")
    total_phq_9_score: int = Field(..., description="Sum of the scores for all nine questions.")
    depression_severity_classification: Literal['Minimal depression', 'Mild depression', 'Moderate depression', 'Moderately severe depression', 'Severe depression'] = Field(..., description="Based on the total PHQ-9 score.")
    flag_for_question_9: Literal['No immediate intervention required', 'Immediate intervention required'] = Field(..., description="Highlight if the client's response to question 9 requires immediate action.")
    justification: str = Field(..., description="Explanation of how the client's session details were mapped to the PHQ-9 items.")