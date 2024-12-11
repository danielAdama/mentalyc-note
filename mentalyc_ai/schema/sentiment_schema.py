from pydantic import BaseModel, Field
from typing import Literal

class SentimentClassificationOutput(BaseModel):
    classification: Literal['anxious', 'depressed'] = Field(..., description="The classification of the session text.")
    justification: str = Field(..., description="Explain the reasoning behind the classification, citing specific details from the session text.")