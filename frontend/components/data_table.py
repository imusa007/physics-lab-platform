import pandas as pd
import streamlit as st

def data_table(initial=None):
    if initial is None:
        initial = pd.DataFrame()
    return st.data_editor(initial, num_rows="dynamic")
