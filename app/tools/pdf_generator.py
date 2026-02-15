import os
import io
import uuid
import re
from datetime import datetime
from weasyprint import HTML
from supabase import create_client, Client

# Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def sanitize_filename(name: str) -> str:
    """Removes characters that aren't allowed in filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def generate_pdf_from_html(html_content: str, user_id: str, job_title: str) -> str:
    """
    Fetches user profile, converts HTML to PDF via WeasyPrint, 
    and uploads to Supabase with the name format: 'User Name - Job Title.pdf'
    
    """
    try:
        # 1. Fetch User Profile for naming
        profile_res = supabase.table("profiles") \
            .select("full_name") \
            .eq("id", user_id) \
            .execute()
        
        if profile_res.data and len(profile_res.data) > 0:
            profile = profile_res.data[0]
            display_name = profile.get("full_name", "User")
        else:
            display_name = "User"

        # 2. Construct the specific Filename
        base_filename = f"{display_name} - {job_title}.pdf"
        clean_filename = sanitize_filename(base_filename)

        # 3. Convert HTML to PDF in memory via WeasyPrint
        pdf_buffer = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_buffer)
        pdf_bytes = pdf_buffer.getvalue()
        file_size = len(pdf_bytes)

        # 4. Storage Path: user_id / timestamp-random-name.pdf
        timestamp = int(datetime.now().timestamp())
        storage_path = f"{user_id}/{timestamp}-{uuid.uuid4().hex[:4]}-{clean_filename}"

        # 5. Upload to Supabase Storage
        supabase.storage.from_("cvs").upload(
            path=storage_path,
            file=pdf_bytes,
            file_options={"content-type": "application/pdf", "upsert": "false"}
        )

        # 6. Get a Signed URL (valid for 1 hour)
        

        # 7. Calculate Versioning
        version_query = supabase.table("cvs") \
            .select("version") \
            .eq("user_id", user_id) \
            .order("version", desc=True) \
            .limit(1) \
            .execute()
        
        new_version = (version_query.data[0]['version'] + 1) if version_query.data else 1

        # 8. Insert Record into 'cvs' Table
        db_record = {
            "user_id": user_id,
            "file_url": storage_path,
            "file_name": clean_filename,
            "file_size": file_size,
            "mime_type": "application/pdf",
            "status": "processed",
            "version": new_version,
            "structured_data": {
                "engine": "weasyprint",
                "generated_at": datetime.now().isoformat()
            }
        }
        
        supabase.table("cvs").insert(db_record).execute()

        return storage_path # Return the URL so main.py can print it

    except Exception as e:
        return f"Error generating/uploading CV: {str(e)}"