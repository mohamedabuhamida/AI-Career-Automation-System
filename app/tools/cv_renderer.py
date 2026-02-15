# def render_cv_html(cv):
#     if hasattr(cv, "model_dump"):
#         data = cv.model_dump()
#     else:
#         data = cv

#     skills = data.get("skills", [])
#     experience = data.get("experience", [])
#     education = data.get("education", [])
#     projects = data.get("projects", [])

#     return f"""
# <!DOCTYPE html>
# <html lang="en">
# <head>
# <meta charset="UTF-8">
# <title>{data.get("full_name", "")} - CV</title>

# <script src="https://cdn.tailwindcss.com"></script>

# <style>
# @page {{
#     size: A4;
#     margin: 16mm;
# }}

# body {{
#     font-family: ui-sans-serif, system-ui, -apple-system;
# }}
# </style>

# </head>

# <body class="bg-white text-gray-800">

# <div class="max-w-[820px] mx-auto px-10 py-10 text-[13px] leading-relaxed">

#     <!-- Header -->
#     <header class="mb-8">
#         <h1 class="text-3xl font-bold tracking-tight">
#             {data.get("full_name", "")}
#         </h1>
#         <p class="text-gray-500 mt-2 text-sm">
#             {data.get("contact", {}).get("email", "")} •
#             {data.get("contact", {}).get("phone", "")} •
#             {data.get("contact", {}).get("location", "")}
#         </p>
#     </header>

#     <!-- Summary -->
#     <section class="mb-8">
#         <h2 class="text-sm font-semibold uppercase tracking-widest text-gray-600 mb-3">
#             Profile
#         </h2>
#         <p class="text-gray-700">
#             {data.get("summary", "")}
#         </p>
#     </section>

#     <!-- Skills as Compact Paragraph Instead of List -->
#     <section class="mb-8">
#         <h2 class="text-sm font-semibold uppercase tracking-widest text-gray-600 mb-3">
#             Core Skills
#         </h2>
#         <p class="text-gray-700">
#             {", ".join(skills)}
#         </p>
#     </section>

#     <!-- Experience -->
#     <section class="mb-8">
#         <h2 class="text-sm font-semibold uppercase tracking-widest text-gray-600 mb-4">
#             Professional Experience
#         </h2>

#         {''.join(f'''
#             <div class="mb-6">
#                 <div class="flex justify-between items-baseline">
#                     <p class="font-semibold text-gray-900">
#                         {exp.get("title", "")}
#                     </p>
#                     <span class="text-xs text-gray-500">
#                         {exp.get("duration", "")}
#                     </span>
#                 </div>

#                 <p class="text-gray-600 mb-2">
#                     {exp.get("company", "")}
#                 </p>

#                 <ul class="list-disc pl-5 space-y-1 text-gray-700">
#                     {''.join(f"<li>{point}</li>" for point in exp.get("description", [])) if isinstance(exp.get("description"), list)
#                     else f"<li>{exp.get('description','')}</li>"}
#                 </ul>
#             </div>
#         ''' for exp in experience if isinstance(exp, dict))}
#     </section>

#     <!-- Projects -->
#     <section class="mb-8">
#         <h2 class="text-sm font-semibold uppercase tracking-widest text-gray-600 mb-4">
#             Selected Projects
#         </h2>

#         {''.join(f'''
#             <div class="mb-6">
#                 <div class="flex justify-between items-baseline">
#                     <p class="font-semibold text-gray-900">
#                         {proj.get("title","")}
#                     </p>
#                     <span class="text-xs text-gray-500">
#                         {proj.get("duration","")}
#                     </span>
#                 </div>

#                 <ul class="list-disc pl-5 space-y-1 text-gray-700 mt-2">
#                     {''.join(f"<li>{point}</li>" for point in proj.get("description", [])) if isinstance(proj.get("description"), list)
#                     else f"<li>{proj.get('description','')}</li>"}
#                 </ul>
#             </div>
#         ''' for proj in projects if isinstance(proj, dict))}
#     </section>

#     <!-- Education -->
#     <section>
#         <h2 class="text-sm font-semibold uppercase tracking-widest text-gray-600 mb-4">
#             Education
#         </h2>

#         {''.join(f'''
#             <div class="mb-4">
#                 <p class="font-semibold text-gray-900">
#                     {edu.get("degree", "")}
#                 </p>
#                 <p class="text-gray-600 text-sm">
#                     {edu.get("institution", "")} • {edu.get("year", "")}
#                 </p>
#             </div>
#         ''' for edu in education if isinstance(edu, dict))}
#     </section>

# </div>

# </body>
# </html>
# """
