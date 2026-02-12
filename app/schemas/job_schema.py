from pydantic import BaseModel, Field
from typing import List, Optional


class JobStructured(BaseModel):
    title: Optional[str] = Field(
        default=None,
        description="Job title or role name."
    )

    required_skills: List[str] = Field(
        default_factory=list,
        description="Mandatory technical skills required for the job."
    )

    preferred_skills: List[str] = Field(
        default_factory=list,
        description="Optional or nice-to-have skills."
    )

    responsibilities: List[str] = Field(
        default_factory=list,
        description="Key job responsibilities."
    )

    required_experience_years: Optional[int] = Field(
        default=None,
        description="Minimum required years of experience."
    )

    education_requirements: Optional[str] = Field(
    default=None,
    description="Required degree. Return short concise text without line breaks."
)

    salary_range: Optional[str] = Field(
        default=None,
        description="Offered salary range for the position."
    )
    location: Optional[str] = Field(
        default=None,
        description="City and country where the job is located."
    )
    company: Optional[str] = Field(
        default=None,
        description="Name of the hiring company or organization."
    )
    