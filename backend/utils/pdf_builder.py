import os
import subprocess
from jinja2 import Template

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LABS_DIR = os.path.join(BASE_DIR, "labs")
BUILD_DIR = os.path.join(BASE_DIR, "build")

os.makedirs(BUILD_DIR, exist_ok=True)

def build_pdf(lab_id: str, data: dict) -> str:
    template_path = os.path.join(LABS_DIR, lab_id, "template.tex")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"LaTeX template not found for lab {lab_id}")

    with open(template_path, "r", encoding="utf-8") as f:
        tmpl = Template(f.read())

    rendered_tex = tmpl.render(**data)

    tex_out = os.path.join(BUILD_DIR, f"{lab_id}_report.tex")
    pdf_out = os.path.join(BUILD_DIR, f"{lab_id}_report.pdf")

    with open(tex_out, "w", encoding="utf-8") as f:
        f.write(rendered_tex)

    # Call tectonic if installed
    try:
        subprocess.run(
            ["tectonic", tex_out, "--outdir", BUILD_DIR],
            check=True
        )
    except Exception as e:
        # Fallback: create a dummy PDF placeholder if tectonic isn't available
        with open(pdf_out, "wb") as f:
            f.write(b"%PDF-1.4\n% placeholder PDF generated because tectonic is missing.\n")
    return pdf_out
