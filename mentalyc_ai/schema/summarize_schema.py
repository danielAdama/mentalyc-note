from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Sequence, Tuple, TypedDict, Union, Any, Dict
from typing import Literal

class AssessmentSummary(BaseModel):
    assessment_type: str = Field(..., description="The type of assessment conducted.")
    severity_classifications: Dict[str, str] = Field(..., description="Severity classifications for both sessions.")
    session_justifications: str = Field(..., description="Overview of the session justifications, highlighting key symptoms and contextual factors.")

class ProgressAnalysis(BaseModel):
    symptom_progress: Dict[str, Literal['Improvement', 'Deterioration', 'Plateau']] = Field(..., description="List each symptom and its corresponding progress.")
    overall_progress_summary: str = Field(..., description="High-level summary of the overall progress.")

class ActionableInsights(BaseModel):
    next_steps: Dict[str, str] = Field(..., description="Recommend tailored next steps for symptoms that plateau or deteriorate.")
    sustain_improvements: Dict[str, str] = Field(..., description="Suggest strategies to sustain improvements for symptoms showing progress.")

class Encouragement(BaseModel):
    motivating_statement: str = Field(..., description="An empathetic and motivating statement to encourage continued effort and resilience.")

class SummarizerOutput(BaseModel):
    assessment_summary: AssessmentSummary = Field(..., description="State the assessment type and summarize the severity classifications for both sessions.")
    progress_analysis: ProgressAnalysis = Field(..., description="List each symptom and its corresponding progress.")
    actionable_insights: ActionableInsights = Field(..., description="Recommend tailored next steps for symptoms that plateau or deteriorate.")
    encouragement: Encouragement = Field(..., description="Include an empathetic and motivating statement to encourage continued effort and resilience.")