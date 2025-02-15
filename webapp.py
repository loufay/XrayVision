import streamlit as st
import plotly.express as px
import numpy as np

def main():
    st.set_page_config(page_title="aiXpert", page_icon=":computer:", layout="wide")
    st.markdown("<h1 style='text-align: center; color: black;'>aiXpert</h1>", unsafe_allow_html=True)

    # Create Tabs
    tabs = st.tabs(["Home", "Data Distribution Explorer", "Data Correlation Explorer"])

    # Access each tab using indexing
    with tabs[0]:  # Home tab
        st.markdown("## Welcome to the Treehack!")
        st.markdown("2025")
        st.markdown("C+L <3 hi")

if __name__ == "__main__":
    if "processComplete" not in st.session_state:
        st.session_state["processComplete"] = None
    main()
