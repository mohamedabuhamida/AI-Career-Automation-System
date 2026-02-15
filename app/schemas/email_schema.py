# app/schemas/email_schema.py
from pydantic import BaseModel, Field

class EmailDraft(BaseModel):
    subject: str = Field(description="Professional email subject line")
    body: str = Field(description="Personalized email body tailored to the job and candidate")