from pydantic import BaseModel, Field
from typing import List, Optional

class JobStructured(BaseModel):
    title: str = Field(
        description="The official job title. Keep it short."
    )
    
    company: Optional[str] = Field(
        default=None, 
        description="Name of the hiring company."
    )
    
    summary: str = Field(
        description="A brief 2-sentence summary of what the role is about."
    )

    required_skills: List[str] = Field(
        default_factory=list,
        description="List of MUST-HAVE technical skills only (e.g., Python, AWS, Docker)."
    )

    soft_skills: List[str] = Field(
        default_factory=list,
        description="List of soft skills (e.g., Communication, Leadership)."
    )

    responsibilities: List[str] = Field(
        default_factory=list,
        description="Key daily responsibilities."
    )

    required_experience_years: Optional[int] = Field(
        default=0,
        description="Minimum years of experience as an integer (e.g., 3). If not found, return 0."
    )

    education: Optional[str] = Field(
    default=None,
    description=(
        "Minimum required degree ONLY. "
        "Max 10 words. Example: 'Bachelor in Computer Science'. "
        "Do NOT include newlines or extra text."
    )

    
    )
    contact_email: Optional[str] = Field(
    default=None,
    description="Contact email found in the job description if available."
)


