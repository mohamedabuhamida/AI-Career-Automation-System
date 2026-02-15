import os
import base64
import requests
from supabase import create_client

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas.email_schema import EmailDraft

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class EmailAgent:
    def __init__(self):
        # Using temperature 0.7 for a more natural, human-sounding email
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    def draft_email(self, cv_data, job_data, is_backup=False) -> EmailDraft:
        """
        Generates a personalized subject line and body for the job application.
        """
        structured_llm = self.llm.with_structured_output(EmailDraft)
        
        system_prompt = """
You are a professional job application assistant.

Your task is to write a professional, concise job application email.

Requirements:
- Write a clear subject line.
- Keep the email between 120–180 words.
- Maximum 3 short paragraphs.
- Start by clearly stating the job title being applied for.
- Highlight the candidate's strong background in Python and machine learning.
- Mention experience with TensorFlow, PyTorch, LLMs, Prompt Engineering, and RAG if relevant.
- Emphasize experience in building and deploying end-to-end AI systems.
- Clearly state that the CV is attached.
- Tone: professional, confident, and direct.
- Avoid overly dramatic or exaggerated phrases.
- The email should sound natural and human-written.
- End with the candidate's full name only.
"""

        
        human_prompt = f"""
        CANDIDATE NAME: {cv_data.full_name}
        JOB TITLE: {job_data.title}
        COMPANY: {job_data.company if job_data.company else 'Hiring Team'}
        JOB SUMMARY: {job_data.summary}
        OPTIMIZED SKILLS: {", ".join(cv_data.skills[:10])}
        
        Write the subject line and email body.
        """
        
        return structured_llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])

    def send_gmail(self, draft: EmailDraft, recipient_email: str, storage_path: str, refresh_token: str, candidate_name: str):
        """
        Uses the Refresh Token to generate an Access Token and send the email.
        Matches the Next.js logic of using the refresh flow.
        """
        # 1. Initialize Credentials using ONLY the refresh token
        # The 'token' (access token) is initially None; the library will fetch it.
        
        signed_url_res = supabase.storage.from_("cvs").create_signed_url(
            storage_path,
            600 
        )

        pdf_url = signed_url_res["signedURL"]
        
        creds = Credentials(
            token=None, 
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
        )

        # 2. Force Refresh (Optional but recommended to verify the token works)
        # This is the Python equivalent of oauth2Client.getAccessToken() in your JS code
        creds.refresh(Request())
        print(f"✅ Generated Fresh Access Token: {creds.token[:10]}...")

        try:
            service = build('gmail', 'v1', credentials=creds)

            # 3. Download the PDF CV
            response = requests.get(pdf_url)
            
            if response.status_code != 200:
                raise Exception("Failed to download CV from storage.")

            # 4. Construct Multipart Email (Matches Next.js logic but with attachment)
            message = MIMEMultipart()
            message['to'] = recipient_email
            message['subject'] = draft.subject
            message.attach(MIMEText(draft.body, 'plain'))

            # Add PDF Attachment
            part = MIMEApplication(response.content, _subtype="pdf")
            part.add_header('Content-Disposition', 'attachment', filename=f"CV_{candidate_name}.pdf")
            message.attach(part)

            # 5. Encode to Base64 (URL safe)
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            # 6. Send via Gmail API
            return service.users().messages().send(
                userId='me', 
                body={'raw': raw_message}
            ).execute()

        except Exception as e:
            print(f"❌ Gmail API Error: {str(e)}")
            raise e