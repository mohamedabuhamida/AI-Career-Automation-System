from pydantic import BaseModel, Field
from typing import List


class MatchResult(BaseModel):
    match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall compatibility score between 0 and 100."
    )

    matched_skills: List[str] = Field(
        default_factory=list,
        description="Skills from CV that match job requirements."
    )

    missing_skills: List[str] = Field(
        default_factory=list,
        description="Required job skills missing from CV."
    )

    reasoning: str = Field(
        ...,
        description="Short explanation for the assigned score."
    )
