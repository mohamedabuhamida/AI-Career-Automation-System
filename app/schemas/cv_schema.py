from pydantic import BaseModel
from typing import List, Optional


class Experience(BaseModel):
    title: str
    company: Optional[str] = None
    description: Optional[str] = None


class Education(BaseModel):
    degree: str
    institution: Optional[str] = None


class CVStructured(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[Education] = []
    projects: List[str] = []
