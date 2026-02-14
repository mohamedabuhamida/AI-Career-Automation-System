from typing import TypedDict, List, Dict, Any, Optional, Literal


class AgentState(TypedDict, total=False):
    # ======================================================
    # 🔹 USER INPUT
    # ======================================================
    cv_file_path: str
    job_input: str

    # ======================================================
    # 🔹 JOB INPUT DETECTION
    # ======================================================
    job_input_type: Literal["title", "url", "text"]
    is_job_link: bool

    # ======================================================
    # 🔹 JOB HUNTING
    # ======================================================
    job_search_results: List[Dict[str, str]]
    selected_job_index: Optional[int]
    selected_job_url: Optional[str]

    # ======================================================
    # 🔹 RAW TEXT
    # ======================================================
    raw_job_text: Optional[str]

    # ======================================================
    # 🔹 STRUCTURED DATA
    # ======================================================
    cv_structured: Dict[str, Any]
    job_structured: Dict[str, Any]

    # ======================================================
    # 🔹 MATCHING
    # ======================================================
    match_score: int
    missing_keywords: List[str]

    # ======================================================
    # 🔹 OPTIMIZATION LOOP
    # ======================================================
    improvement_plan: Optional[str]
    revision_count: int
    critique_feedback: List[str]

    # ======================================================
    # 🔹 FINAL OUTPUTS
    # ======================================================
    final_cv_content: Optional[Dict[str, Any]]
    generated_pdf_path: Optional[str]
    email_draft: Optional[str]

    # ======================================================
    # 🔹 HUMAN IN LOOP
    # ======================================================
    human_action: Optional[Literal["pending", "selected"]]
    user_feedback: Optional[Literal["approve", "retry"]]

    final_cv_content: Optional[Dict[str, Any]]
    generated_pdf_path: Optional[str]
