from pydantic import BaseModel, Field
from typing import List, Optional

# --- Sub-Models ---
class ContactInfo(BaseModel):
    email: Optional[str] = Field(description="Email address")
    phone: Optional[str] = Field(description="Phone number")
    linkedin: Optional[str] = Field(description="LinkedIn profile URL")
    github: Optional[str] = Field(description="GitHub profile URL")
    portfolio: Optional[str] = Field(description="Portfolio website URL")
    location: Optional[str] = Field(description="City, Country")

class Experience(BaseModel):
    title: str = Field(description="Job title")
    company: Optional[str] = Field(description="Company name")
    duration: Optional[str] = Field(description="Start and End dates (e.g., 'Jan 2020 - Present')")
    description: Optional[str] = Field(description="Summary of responsibilities and achievements")

class Education(BaseModel):
    degree: str = Field(description="Degree name")
    institution: Optional[str] = Field(description="University name")
    year: Optional[str] = Field(description="Year of graduation")

# --- Main Model ---
class CVStructured(BaseModel):
    full_name: Optional[str] = Field(description="Candidate's full name")
    contact: Optional[ContactInfo] = Field(description="Contact details")
    summary: Optional[str] = Field(description="Professional summary")
    skills: List[str] = Field(default_factory=list, description="Technical and soft skills")
    experience: List[Experience] = Field(default_factory=list, description="Work history")
    education: List[Education] = Field(default_factory=list, description="Academic background")
    projects: List[str] = Field(default_factory=list, description="Project descriptions")
    certifications: List[str] = Field(default_factory=list, description="Professional certificates")
    languages: List[str] = Field(default_factory=list, description="Languages spoken")
    
    # --- New Field ---
    # html_code: Optional[str] = Field(
    #     description="A complete, standalone ATS-friendly HTML string representing this CV. Use semantic tags, single-column layout, using Tailwind CSS"
    # )