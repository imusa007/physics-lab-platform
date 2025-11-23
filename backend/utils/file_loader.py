import os
from .latex_to_html import latex_to_html

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LABS_DIR = os.path.join(BASE_DIR, "labs")

def load_lab_tex(lab_id: str) -> str:
    path = os.path.join(LABS_DIR, lab_id, "instructions.tex")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Lab instructions not found for: {lab_id}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_lab_html(lab_id: str) -> str:
    tex = load_lab_tex(lab_id)
    return latex_to_html(tex)
