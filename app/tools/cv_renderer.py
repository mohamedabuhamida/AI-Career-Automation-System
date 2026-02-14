# app/tools/cv_renderer.py

def render_cv_html(cv):
    if hasattr(cv, "model_dump"):
        data = cv.model_dump()
    else:
        data = cv

    skills = data.get("skills", [])
    experience = data.get("experience", [])
    education = data.get("education", [])
    projects = data.get("projects", [])

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{data.get("full_name", "")} - CV</title>

    <!-- Bootstrap CDN -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    >

    <style>
        body {{
            font-size: 14px;
            line-height: 1.6;
        }}
        h1, h2, h3 {{
            color: #0d6efd;
        }}
        .section {{
            margin-bottom: 24px;
        }}
    </style>
</head>

<body class="container my-5">

    <header class="mb-4">
        <h1>{data.get("full_name", "")}</h1>
        <p class="text-muted">
            {data.get("contact", {}).get("email", "")} |
            {data.get("contact", {}).get("phone", "")} |
            {data.get("contact", {}).get("location", "")}
        </p>
    </header>

    <section class="section">
        <h2>Professional Summary</h2>
        <p>{data.get("summary", "")}</p>
    </section>

    <section class="section">
        <h2>Skills</h2>
        <ul class="row">
            {''.join(f'<li class="col-4">{skill}</li>' for skill in skills)}
        </ul>
    </section>

    <section class="section">
        <h2>Experience</h2>
        {''.join(f'''
            <div class="mb-3">
                <h5>{exp.get("title", "")} – {exp.get("company", "")}</h5>
                <small class="text-muted">{exp.get("duration", "")}</small>
                <p>{exp.get("description", "")}</p>
            </div>
        ''' for exp in experience if isinstance(exp, dict))}
    </section>

    <section class="section">
        <h2>Education</h2>
        {''.join(f'''
            <p>
                <strong>{edu.get("degree", "")}</strong><br>
                {edu.get("institution", "")} – {edu.get("year", "")}
            </p>
        ''' for edu in education if isinstance(edu, dict))}
    </section>

    <section class="section">
        <h2>Projects</h2>
        {''.join(
            f'<p>{proj}</p>' if isinstance(proj, str)
            else f'<p><strong>{proj.get("title","")}</strong>: {proj.get("description","")}</p>'
            for proj in projects
        )}
    </section>

</body>
</html>
"""
