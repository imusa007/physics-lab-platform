import os
import subprocess
from tempfile import NamedTemporaryFile
from textwrap import dedent


def latex_to_html(tex_source: str) -> str:
    """
    Convert LaTeX source -> pretty HTML using Pandoc + MathJax.

    Returns a full HTML fragment that you can drop into Streamlit
    with st.markdown(..., unsafe_allow_html=True).
    """
    # Wrap in a minimal LaTeX document so Pandoc is happier.
    tex_document = (
        dedent(
            r"""
        \documentclass[11pt]{article}
        \usepackage{amsmath, amssymb}
        \usepackage{graphicx}
        \usepackage{hyperref}
        \usepackage{booktabs}
        \begin{document}
        """
        )
        + tex_source
        + "\n\\end{document}\n"
    )

    # Temporary .tex file for pandoc
    with NamedTemporaryFile(suffix=".tex", delete=False) as tf:
        tex_path = tf.name
        tf.write(tex_document.encode("utf-8"))

    try:
        # Call pandoc: LaTeX -> HTML with MathJax support
        # --mathjax tells Pandoc to emit MathJax-compatible HTML
        result = subprocess.run(
            [
                "pandoc",
                tex_path,
                "--from=latex",
                "--to=html",
                "--mathjax",
                "--embed-resources",
                "--strip-comments",
            ],
            check=True,
            capture_output=True,
        )

        html = result.stdout.decode("utf-8")
    except Exception as e:
        # Fallback: show raw LaTeX if pandoc fails
        html = f"""
        <div style="border:1px solid #f00; padding:0.5rem;">
          <strong>LaTeX rendering error:</strong> {e}<br/>
          <pre>{tex_source}</pre>
        </div>
        """
    finally:
        try:
            os.remove(tex_path)
        except OSError:
            pass

    # # Light CSS to make it nicer inside Streamlit
    # styled_html = f"""
    # <style>
    #   .lab-content {{
    #     font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    #     line-height: 1.6;
    #     max-width: 800px;
    #     margin: 0 auto;
    #   }}
    #   .lab-content h1,
    #   .lab-content h2,
    #   .lab-content h3 {{
    #     margin-top: 1.5rem;
    #     margin-bottom: 0.5rem;
    #   }}
    #   .lab-content p {{
    #     margin: 0.4rem 0;
    #   }}
    #   .lab-content ul, .lab-content ol {{
    #     padding-left: 1.4rem;
    #   }}
    # </style>

    # <div class="lab-content">
    #   {html}
    # </div>
    # """

    MATHJAX = """
    <script>
    window.MathJax = {
      tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
      svg: { fontCache: 'global' }
    };
    </script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    """

    styled_html = f"""
    {MATHJAX}
    <style>
      .lab-content {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
      }}
      .lab-content h1, .lab-content h2, .lab-content h3 {{
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
      }}
      .lab-content p {{
        margin: 0.4rem 0;
      }}
    </style>

    <div class="lab-content">
      {html}
    </div>
"""

    return styled_html
