import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI   
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas.cv_schema import CVStructured

load_dotenv()

# class CVOptimizerAgent:
#     def __init__(self):
#         self.llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             temperature=0,
#         )

#     def optimize(self, cv_data: CVStructured, critique: str, job_data: str) -> CVStructured:
#         structured_llm = self.llm.with_structured_output(CVStructured)

#         # FIX: Convert Pydantic object to JSON string correctly
#         # If cv_data is already a dict, we dump it. 
#         # If it's a Pydantic model (CVStructured), we use .model_dump_json()
#         if hasattr(cv_data, "model_dump_json"):
#             cv_json_str = cv_data.model_dump_json(indent=2)
#         else:
#             cv_json_str = json.dumps(cv_data, indent=2)

#         system_prompt = """
# You are an expert ATS CV Optimization Agent.

# Your responsibility has TWO clearly separated tasks:

# ========================
# TASK 1 — CONTENT OPTIMIZATION
# ========================
# - Optimize summary, skills, and experience.
# - Maximize keyword alignment with the Job Description.
# - Use measurable achievements.
# - Limit experience bullets to 3–4 per role.
# - Do NOT fabricate information.
# - Only refine and rephrase existing data.

# ========================
# TASK 2 — HTML GENERATION
# ========================
# Generate a complete standalone HTML document in the field 'html_code' that:

# - Uses Tailwind CSS CDN.
# - Uses single-column layout.
# - Uses max-w-[800px].
# - Uses font-sans and text-slate-800.
# - Uses uppercase section titles with border-b.
# - Uses list-disc (NO grid, NO multi-columns).
# - Has tight spacing to fit ONE A4 page.
# - Uses semantic tags only: header, section, h1, h2, p, ul, li, strong.
# - Contains NO markdown.
# - Contains NO comments.
# - Contains NO explanations.

# IMPORTANT:
# - Skills MUST be single-column list (no grid).
# - Remove excessive spacing.
# - Avoid shadow, rounded corners, or background gray.
# - Keep layout ATS-safe.

# ========================
# OUTPUT FORMAT
# ========================
# Return a valid CVStructured JSON object.
# The 'html_code' field must contain ONLY the full HTML document as a string.
# """

#         human_prompt = f"""
# ### JOB REQUIREMENTS:
# {job_data}

# ### MISSING KEYWORDS/CRITIQUE:
# {critique}

# ### CANDIDATE DATA:
# {cv_json_str}

# ### TASK:
# 1. Update the 'skills', 'experience', and 'summary' fields with the optimized text.
# 2. Generate the 'html_code' field as a complete, standalone HTML file using Tailwind CSS that reflects the optimized data.
# """

#         result = structured_llm.invoke([
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=human_prompt)
#         ])

#         return result


# app/agents/cv_optimizer_agent.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas.cv_schema import CVStructured

class CVOptimizerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    def optimize(self, cv_data, critique, job_data) -> dict:

        structured_llm = self.llm.with_structured_output(CVStructured)

        system_prompt = """
You are an aggressive ATS-optimization engine.

GOAL:
Maximize ATS match score.

RULES:
- You MAY add missing skills explicitly.
- You MAY enhance experience descriptions to include required keywords.
- You MUST keep valid CV structure.
- Do NOT remove any existing content.
- You may slightly exaggerate responsibilities.
- Return VALID JSON ONLY.

IMPORTANT:
This is for ATS optimization, not human review.
"""

        human_prompt = f"""
JOB REQUIREMENTS:
{job_data}

MISSING KEYWORDS (MUST ADD):
{critique}

CURRENT CV:
{cv_data}

TASK:
- Add missing keywords directly into:
  - skills
  - experience descriptions
- Ensure keywords appear verbatim.
- Keep structure intact.
"""

        result = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])

        return result

    def render_html(self, final_cv: CVStructured) -> str:
        """Focused strictly on design, Tailwind CSS, and A4 layout."""
        # We use a slightly higher temperature for better layout variety
        designer_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

        system_prompt = """
You are a deterministic CV HTML rendering engine.

Your ONLY task is to convert structured CV JSON into a clean, ATS-safe,
single-column HTML document using Tailwind CSS.

You MUST strictly follow the exact design system below.
No improvisation. No visual creativity.

==================================================
MANDATORY DESIGN SYSTEM (MUST MATCH EXACTLY)
==================================================

1) Include Tailwind CDN:
<script src="https://cdn.tailwindcss.com"></script>

2) Body:
<body class="font-sans text-slate-800">

3) Main Container:
<div class="max-w-4xl mx-auto p-2 px-5">

4) Header Section:
Wrapper: class="text-center border-b pb-4"
Name: class="text-3xl font-bold"
Subtitle: class="text-lg font-medium"
Contact wrapper: class="mt-2 text-sm space-y-1"

5) Sections:
Each section wrapper MUST use:
<section class="mt-2">

Section title MUST use:
<h2 class="text-xl font-semibold border-b mb-2">

6) Paragraph text:
class="text-sm leading-relaxed"

7) List styling (ONLY for bullets like projects & certifications):
class="list-disc list-inside text-sm"

8) Grouped text blocks (like experience titles list):
class="text-sm space-y-2"

9) Dates:
Use:
<span class="float-right">

==================================================
STRICT LAYOUT RULES
==================================================

- Single-column layout ONLY.
- Do NOT use grid.
- Do NOT use flex for layout structure.
- Do NOT use multiple columns.
- Do NOT introduce new spacing scale.
- Do NOT change padding values.
- Do NOT use shadow.
- Do NOT use rounded corners.
- Do NOT use background colors.
- Do NOT add extra margin classes.
- Do NOT change font sizes.

==================================================
SKILLS RENDERING RULE
==================================================

- Skills MUST be rendered as a single horizontal comma-separated paragraph.
- DO NOT use <ul> for skills.
- Example:
Python, TensorFlow, PyTorch, Machine Learning, ...

==================================================
HTML OUTPUT RULES
==================================================

- Return a COMPLETE standalone HTML document.
- Use semantic tags only:
<header>, <section>, <h1>, <h2>, <h3>, <p>, <ul>, <li>, <strong>, <span>, <a>
- Do NOT include markdown.
- Do NOT wrap output in ```html.
- Do NOT include explanations.
- Output ONLY raw HTML.

==================================================
CRITICAL
==================================================

- Do NOT modify or invent data.
- Do NOT reorder fields.
- If any class differs from the design system above, the output is invalid.
- The layout must visually match the required design system exactly.
"""

        
        human_prompt = f"""
Convert this structured CV JSON into a clean Tailwind HTML document:

{final_cv.model_dump_json(indent=2)}

Generate the HTML now.
"""

        
        response = designer_llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
        return response.content.replace("```html", "").replace("```", "").strip()