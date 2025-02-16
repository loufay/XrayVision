
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image

from perform_report_explanation_mistral import explain_radiology_report
from webapp.tab1_welcome import tab1_welcome
from webapp.tab2_add_personal_data import tab2_add_personal_data
from webapp.tab3_xray_analysis import tab3_xray_analysis
from webapp.tab4_simplify_radreport import tab4_simplify_radreport

# Init all models

def main():
    st.set_page_config(page_title="Main", page_icon=":computer:", layout="wide")
    # CSS to inject custom styles
    st.markdown("""
    <style>
    a { color: blue; } /* Changes the color of links */
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>DiagnoseMe</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Read Your Rays, Right Away</h3>", unsafe_allow_html=True)
    # Tabs
    tabs = st.tabs(["Home", "Personal Information", "Read Your Rays", "Explain Report"])
    tab1, tab2, tab3, tab4 = tabs
    with tab1:
        tab1_welcome()
    with tab2:
        tab2_add_personal_data()
        
        
    with tab3:
        tab3_xray_analysis()
    # with tab4:
    #     # TODO: Change to predicted diseases
    #     diseases = [
    #     "Enlarged Cardiomediastinum",
    #     "Cardiomegaly",
    #     "Lung Opacity", "Lung Lesion",
    #     "Edema", "Consolidation", "Pneumonia", "Atelectasis",
    #     "Pneumothorax", "Pleural Effusion", "Fracture", "Support Devices"]
    #     st.markdown("## Localize Disease")
    #     st.markdown("Please upload an X-ray image, and we will display it below.")
    #     uploaded_file_loc = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], key="unique_key_1")
    #     if uploaded_file_loc is not None:
    #         selected_disease = st.session_state.get("selected_disease", None)
    #         cols = st.columns(len(diseases) // 2)  # Arrange buttons in two rows
    #         for i, disease in enumerate(diseases):
    #             if cols[i % len(cols)].button(disease):
    #                 st.session_state["selected_disease"] = disease  # Store the selected disease
    #         # Show selected disease
    #         if "selected_disease" in st.session_state:
    #             st.markdown(f"**Selected Disease:** {st.session_state['selected_disease']}")
    #             # Call disease localization only after a disease is selected
    #             if st.button("Localize Disease"):
    #                 print(st.session_state["selected_disease"])
    #                 # transform  st.session_state["selected_disease"] to string
    #                 perform_disease_localization(uploaded_file_loc, disease=st.session_state["selected_disease"])
    #                 path_to_localized_disease = "home/cmottez/aiXperts/src/temp/disease_localization.png"
    #                 # Display localized image
    #                 st.image(path_to_localized_disease, caption='Localized Disease.', use_container_width=True)
    with tab4:
        tab4_simplify_radreport()


    if __name__ == "__main__":
        main()