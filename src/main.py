
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
#from perform_report_explanation_mistral import explain_radiology_report
from webapp.tab1_welcome import tab1_welcome
from webapp.tab2_personalize import tab2_add_personal_data
from webapp.tab3_xray_analysis import tab3_xray_analysis
from webapp.tab4_locate_disease import tab4_locate_disease
from webapp.tab5_radreport import tab5_radreport
# Init all models
st.set_page_config(page_title="Main", page_icon=":computer:", layout="wide")
def main():
    # CSS to inject custom styles
    st.markdown("""
    <style>
    a { color: blue; } /* Changes the color of links */
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Welcome to XRayVision</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Read Your X-rays, Right Away</h3>", unsafe_allow_html=True)
    # Tabs
    tabs = st.tabs(["Home", "Personal Information", "Read Your X-rays","Locate Disease", "Explain Report"])
    tab1, tab2, tab3, tab4, tab5 = tabs
    with tab1:
        tab1_welcome()
    with tab2:
        tab2_add_personal_data()
    with tab3:
        tab3_xray_analysis()
    with tab4:
        tab4_locate_disease()
    with tab5:
        tab5_radreport()
if __name__ == "__main__":
    main()