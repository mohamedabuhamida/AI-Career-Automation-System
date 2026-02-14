# app/tools/pdf_generator.py

from pathlib import Path
import subprocess
import tempfile


WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"


def generate_pdf_from_html(html: str, output_path: str) -> str:
    """
    Generate PDF from HTML using wkhtmltopdf.
    If PDF generation fails, fallback to saving HTML.
    """

    output_path = Path(output_path)

    # ----------------------------------------
    # 1️⃣ Save HTML temporarily
    # ----------------------------------------
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".html", mode="w", encoding="utf-8"
    ) as f:
        f.write(html)
        html_path = Path(f.name)

    try:
        # ----------------------------------------
        # 2️⃣ Generate PDF via wkhtmltopdf
        # ----------------------------------------
        subprocess.run(
            [
                WKHTMLTOPDF_PATH,
                "--encoding", "utf-8",
                "--enable-local-file-access",
                str(html_path),
                str(output_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print(f"📄 PDF generated successfully: {output_path}")
        return str(output_path)

    except Exception as e:
        # ----------------------------------------
        # 3️⃣ Fallback → Save HTML
        # ----------------------------------------
        print("⚠️ PDF generation failed, falling back to HTML.")
        print(f"Reason: {e}")

        fallback_path = output_path.with_suffix(".html")
        fallback_path.write_text(html, encoding="utf-8")

        print(f"🌐 HTML saved instead: {fallback_path}")
        return str(fallback_path)

    finally:
        # ----------------------------------------
        # 4️⃣ Cleanup temp HTML
        # ----------------------------------------
        try:
            html_path.unlink()
        except Exception:
            pass
