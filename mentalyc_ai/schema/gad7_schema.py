from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Sequence, Tuple, TypedDict, Union, Any, Dict
from typing import Literal

class GAD7Output(BaseModel):
    gad_7_scoring_table: Dict[str, int] = Field(..., description="A table mapping the client's symptoms and corresponding responses to the seven GAD-7 items.")
    total_gad_7_score: int = Field(..., description="Sum of the scores for all seven questions.")
    anxiety_severity_classification: Literal['Minimal anxiety', 'Mild anxiety', 'Moderate anxiety', 'Severe anxiety'] = Field(..., description="Based on the total GAD-7 score.")
    justification: str = Field(..., description="Explanation of how the client's session details were mapped to the GAD-7 items.")