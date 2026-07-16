from typing import Dict

from pydantic import BaseModel


class QuestionResult(BaseModel):
    label: str
    is_question: bool
    score: float


class QuestionResponse(BaseModel):
    classifications: Dict[str, QuestionResult]
    model: str
    elapsed: float
