import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import matplotlib.pyplot as plt

BACKEND = "http://localhost:5001"

st.title("Physics Lab Platform")

MATHJAX_SNIPPET = """
<script>
window.MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
  svg: { fontCache: 'global' }
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

# Inject MathJax into the page once
# st.markdown(MATHJAX_SNIPPET, unsafe_allow_html=True)

# Load labs
try:
    labs = requests.get(f"{BACKEND}/labs", timeout=5).json()
except Exception as e:
    st.error(f"Could not connect to backend at {BACKEND}: {e}")
    st.stop()

lab = st.selectbox("Choose a lab", labs)

# Load instructions (HTML placeholder)
resp = requests.get(f"{BACKEND}/lab/{lab}/html")
html = resp.json().get("html", "")
# st.markdown(html, unsafe_allow_html=True)
components.html(html, height=800, scrolling=True)

st.subheader("Enter your data")
df = st.data_editor(pd.DataFrame({"t": [], "x": []}), num_rows="dynamic")

if not df.empty:
    st.subheader("Plot")
    fig, ax = plt.subplots()
    ax.scatter(df["t"], df["x"])
    ax.set_xlabel("t (s)")
    ax.set_ylabel("x (m)")
    st.pyplot(fig)

st.subheader("Write-up")
student_name = st.text_input("Student name")
section = st.text_input("Section")
analysis = st.text_area("Analysis")
conclusion = st.text_area("Conclusion")

if st.button("Generate PDF report"):
    # Convert table to a simple LaTeX tabular
    if df.empty:
        table_latex = "No data submitted."
    else:
        table_latex = df.to_latex(index=False)

    payload = {
        "student_name": student_name,
        "section": section,
        "analysis": analysis,
        "conclusion": conclusion,
        "table_latex": table_latex,
    }

    with st.spinner("Requesting PDF from backend..."):
        r = requests.post(f"{BACKEND}/lab/{lab}/pdf", json=payload)
    if r.status_code == 200:
        st.success("PDF generated!")
        st.download_button(
            "Download lab_report.pdf",
            data=r.content,
            file_name="lab_report.pdf",
            mime="application/pdf",
        )
    else:
        st.error(f"Backend error: {r.status_code} - {r.text}")
