import streamlit as st 
import os 
import sys 
from perform_report_explanation_mistral import explain_radiology_report
from perform_report_generation_chexagent import perform_report_generation_chexagent
import csv
from perform_disease_recommendation_perplexity import perform_disease_recommendation_perplexity
from perform_disease_localization import perform_disease_localization

def tab4_locate_disease():
    
    diseases = [
    "Enlarged Cardiomediastinum",
    "Cardiomegaly",
    "Lung Opacity", "Lung Lesion",
    "Edema", "Consolidation", "Pneumonia", "Atelectasis",
    "Pneumothorax", "Pleural Effusion", "Fracture", "Support Devices"]
    st.markdown("## Localize Disease")
    st.markdown("Please upload an X-ray image, and we will display it below.")
    uploaded_file_loc = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], key="unique_key_2")
    # if uploaded_file_loc is not None:
    #     selected_disease = st.session_state.get("selected_disease", None)
    #     cols = st.columns(len(diseases) // 2)  # Arrange buttons in two rows
    #     for i, disease in enumerate(diseases):
    #         if cols[i % len(cols)].button(disease):
    #             st.session_state["selected_disease"] = disease  # Store the selected disease


    if uploaded_file_loc is not None:
        selected_disease = st.session_state.get("selected_disease", None)

        # Using an expander to tidy up the UI
        with st.expander("Select a Disease"):
            cols = st.columns(2)  # Adjust the number of columns as needed

            # Create buttons in a grid layout
            for i, disease in enumerate(diseases):
                col = cols[i % len(cols)]
                # Use button style to indicate selection
                if col.button(disease, key=f"disease_{i}"):
                    st.session_state["selected_disease"] = disease
                    
    # # Display the currently selected disease outside the expander
    # if selected_disease:
    #     st.write(f"You have selected: **{selected_disease}**")

        # Show selected disease
        if "selected_disease" in st.session_state:
            st.markdown(f"**Selected Disease:** {st.session_state['selected_disease']}")
            # Call disease localization only after a disease is selected
            if st.button("Localize Disease"):
                print(st.session_state["selected_disease"])
                # transform  st.session_state["selected_disease"] to string
                perform_disease_localization(uploaded_file_loc, disease=st.session_state["selected_disease"])
                path_to_localized_disease = "home/cmottez/aiXperts/src/temp/disease_localization.png"
                # Display localized image
                st.image(path_to_localized_disease, caption=st.session_state["selected_disease"], width=500)



