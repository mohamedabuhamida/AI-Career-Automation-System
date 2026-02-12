from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Optional


class ContactInfo(BaseModel):
    email: Optional[EmailStr] = Field(
        default=None,
        description="Primary professional email address."
    )
    phone: Optional[str] = Field(
        default=None,
        description="Phone number including country code if available."
    )
    linkedin: Optional[HttpUrl] = Field(
        default=None,
        description="LinkedIn profile URL."
    )
    github: Optional[HttpUrl] = Field(
        default=None,
        description="GitHub profile URL."
    )
    portfolio: Optional[HttpUrl] = Field(
        default=None,
        description="Personal portfolio website URL."
    )
    website: Optional[HttpUrl] = Field(
        default=None,
        description="Other professional website link."
    )
    location: Optional[str] = Field(
        default=None,
        description="City and country of residence."
    )


class Experience(BaseModel):
    title: str = Field(
        ...,
        description="Job title or role name. This field is required."
    )
    company: Optional[str] = Field(
        default=None,
        description="Company or organization name."
    )
    description: Optional[str] = Field(
        default=None,
        description="Short summary of responsibilities and achievements."
    )


class Education(BaseModel):
    degree: str = Field(
        ...,
        description="Degree name or qualification. This field is required."
    )
    institution: Optional[str] = Field(
        default=None,
        description="University or educational institution name."
    )


class CVStructured(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Full name of the candidate."
    )
    contact: Optional[ContactInfo] = Field(
        default=None,
        description="Contact information including email, phone, and professional links."
    )
    summary: Optional[str] = Field(
        default=None,
        description="Professional summary or career objective."
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of technical and soft skills."
    )
    experience: List[Experience] = Field(
        default_factory=list,
        description="List of professional work experiences."
    )
    education: List[Education] = Field(
        default_factory=list,
        description="List of educational qualifications."
    )
    projects: List[str] = Field(
        default_factory=list,
        description="List of notable projects with short descriptions."
    )
    certifications: List[str] = Field(
        default_factory=list,
        description="Professional certifications or licenses."
    )
    languages: List[str] = Field(
        default_factory=list,
        description="Languages known with proficiency if available."
    )
