import matplotlib.pyplot as plt
import streamlit as st

def scatter(df, x_col, y_col, xlabel=None, ylabel=None):
    if df.empty:
        return
    fig, ax = plt.subplots()
    ax.scatter(df[x_col], df[y_col])
    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel or y_col)
    st.pyplot(fig)
