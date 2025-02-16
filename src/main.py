
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
from perform_disease_prediction_torchxrayvision import torch_x_ray_prediction
from perform_disease_prediction_mi2 import perform_disease_prediction_mi2
from perform_disease_prediction_chexagent import perform_disease_prediction_chexagent
from perform_disease_localization import perform_disease_localization
from perform_report_explanation_mistral import explain_radiology_report
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
    tabs = st.tabs(["Home", "Personal Information", "Read Your Rays", "Localize Disease", "Explain Report"])
    tab1, tab2, tab3, tab4, tab5 = tabs
    with tab1:
        st.markdown(
            """
            <h3 style="text-align: left;">
                Welcome to DiagnoseMe!  </h3>
            <div style="text-align: left;">
                <p>
                Have you recently had an X-ray and are seeking feedback? <br>
                Already consulted a doctor but looking for a second opinion? <br>
                <strong style="font-size: 20px;">You're in the right place!</strong>
            </div>
            <div style="text-align: left;">
                <p>
            At DiagnoseMe, we provide instant, expert analysis of your X-ray images, helping you understand your health better and faster. Join us today and start making more informed health decisions!
            </div>
            """,
            unsafe_allow_html=True
    )
    with tab2:
        st.markdown(
            """
            <div style="text-align: left;">
                <p>
                You don't need to provide your personal information, but they can help us to provide better diagnostic and help you understand your images!
            </div>
            <div style="text-align: left; font-style: italic;">
            <p>Note that the information provided will remain confidential and will be deleted at the end of the analysis.
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.form(key='user_details_form'):
            st.write('Please enter your details:')
            sex = st.selectbox('Select your sex:', options=['Male', 'Female', 'Other'])
            age = st.number_input('Age:', min_value=0, max_value=120, step=1, format='%d')
            weight = st.number_input('Weight (in kg):', min_value=0.0, max_value=300.0, step=0.5, format='%f')
            size = st.number_input('Height (in cm):', min_value=0.0, max_value=300.0, step=0.5, format='%f')
            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                st.write('Thanks for submitting your details!')
        
        
    with tab3:
            st.markdown("## Upload your X-ray!")
            st.markdown("Please upload an X-ray image, and we will display it below.")
            # File uploader allows user to add their own image
            uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
            if uploaded_file is not None:
                disease_groups = {}
                all_predicted_diseases = []
                # Using columns to layout image and selection
                col1, col2 = st.columns([2, 2])
                with col1:
                    image = Image.open(uploaded_file)
                    st.image(image, caption='Uploaded X-ray.', use_container_width=True)
                with col2:
                    st.write("Image is ready for processing!")
                    st.write("It looks like you uploaded a Chest X-Ray!")
                    disease_list = ["No Finding", "Enlarged Cardiomediastinum", "Cardiomegaly", "Lung Opacity",
                                    "Lung Lesion", "Edema", "Consolidation", "Pneumonia", "Atelectasis",
                                    "Pneumothorax", "Pleural Effusion", "Fracture"]
                    all_options = ["Select All"] + disease_list
                    if 'selected_diseases' not in st.session_state:
                        st.session_state.selected_diseases = []
                    selected_diseases = st.multiselect(
                        "Please select the diseases you want to test:",
                        all_options,
                        default=st.session_state.selected_diseases
                    )
                    if "Select All" in selected_diseases:
                        selected_diseases = disease_list
                        st.session_state.selected_diseases = selected_diseases
                    if st.button('Analyze Image'):
                        st.write("We are processing your image...")
                        st.write("It can take a few seconds...")
                        pred1 = torch_x_ray_prediction(uploaded_file)
                        try:
                            d1 = [d for d in selected_diseases if pred1[d] == 1]
                        except:
                            st.write("No valid X-ray image uploaded.")
                        # pred2 = perform_disease_prediction_mi2(uploaded_file)
                        pred3 = perform_disease_prediction_chexagent(uploaded_file)
                        pred2 = pred3
                        predictions = {
                            'Dr1': d1,
                            'Dr2': [d for d in selected_diseases if pred2[d] == 1],
                            'Dr3': [d for d in selected_diseases if pred3[d] == 1]
                        }
                        all_predicted_diseases = set(predictions['Dr1'] + predictions['Dr2'] + predictions['Dr3'])
                        # Calculate probabilities and group diseases
                        disease_groups = {3: [], 2: [], 1: []}
                        for disease in all_predicted_diseases:
                            count = sum(disease in predictions[doc] for doc in ['Dr1', 'Dr2', 'Dr3'])
                            if count == 3:
                                disease_groups[3].append(disease)
                            elif count == 2:
                                disease_groups[2].append(disease)
                            elif count == 1:
                                disease_groups[1].append(disease)
                diseases_info = {
                    "No Finding": "No significant abnormality detected in the X-ray image.",
                    "Enlarged Cardiomediastinum": "Increase in the size of the mediastinum, which may suggest the presence of various conditions including lymphadenopathy or mass lesions.",
                    "Cardiomegaly": "Enlargement of the heart's size, often indicative of heart disease or high blood pressure.",
                    "Lung Opacity": "Any area of increased opacity in the lung can indicate a range of issues, from infection to chronic disease.",
                    "Lung Lesion": "A localized abnormality in the lung which can be benign or malignant. Further testing is usually required.",
                    "Edema": "Swelling caused by excess fluid trapped in the body's tissues, which can be seen in pulmonary edema as fluffy opacities in the lungs.",
                    "Consolidation": "Region of normally compressible lung tissue that has filled with liquid instead of air. It is typically a result of pneumonia.",
                    "Pneumonia": "Infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus.",
                    "Atelectasis": "Partial or complete collapse of the lung or a section (lobe) of a lung.",
                    "Pneumothorax": "An abnormal collection of air in the pleural space between the lung and the chest wall, causing the lung to collapse.",
                    "Pleural Effusion": "Accumulation of excess fluid between the layers of the pleura outside the lungs.",
                    "Fracture": "Any break in the bones, which can involve ribs or other bones visible in an X-ray of the chest."
                }
                st.markdown("""
                    <style>
                    .tooltip {
                        position: relative;
                        display: inline-block;
                        border-bottom: 1px dotted black;
                    }
                    .tooltip .tooltiptext {
                        visibility: hidden;
                        width: 400px;
                        background-color: blue;
                        color: #fff;
                        text-align: center;
                        border-radius: 6px;
                        padding: 5px;
                        position: absolute;
                        z-index: 1;
                        bottom: 0%;
                        left: 50%;
                        margin-left: 60px;
                        font-size: 12px;
                    }
                    .tooltip:hover .tooltiptext {
                        visibility: visible;
                        font-size: 16px;  /* Larger font size on hover */
                    }
                    </style>
                    """, unsafe_allow_html=True)
                st.write("### According to the 3 ModDocs:")
                if len(all_predicted_diseases) == 0:
                            st.write("Your X-ray is healthy!")
                for prob, diseases in disease_groups.items():
                    if diseases:
                        for disease in diseases:
                            # Display each disease in a blue box followed by an arrow and the probability
                            # tooltip_html = f'<div style="display: inline-block; padding: 10px; background-color: blue; color: white; border-radius: 5px;">{disease}</div> --> {prob}/3'
                            tooltip_html = f'<div class="tooltip">{disease}<span class="tooltiptext">{diseases_info[disease]}</span></div> --> {prob}/3'
                            st.markdown(tooltip_html, unsafe_allow_html=True)
                        st.markdown("<div style='padding: 20px;'></div>", unsafe_allow_html=True)
        with tab4:
            # TODO: Change to predicted diseases
            diseases = [
            "Enlarged Cardiomediastinum",
            "Cardiomegaly",
            "Lung Opacity", "Lung Lesion",
            "Edema", "Consolidation", "Pneumonia", "Atelectasis",
            "Pneumothorax", "Pleural Effusion", "Fracture", "Support Devices"]
            st.markdown("## Localize Disease")
            st.markdown("Please upload an X-ray image, and we will display it below.")
            uploaded_file_loc = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], key="unique_key_1")
            if uploaded_file_loc is not None:
                selected_disease = st.session_state.get("selected_disease", None)
                cols = st.columns(len(diseases) // 2)  # Arrange buttons in two rows
                for i, disease in enumerate(diseases):
                    if cols[i % len(cols)].button(disease):
                        st.session_state["selected_disease"] = disease  # Store the selected disease
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
                        st.image(path_to_localized_disease, caption='Localized Disease.', use_container_width=True)
        with tab5:
            st.markdown("## Radiology Report Simplification")
            report_option = st.radio("Choose input method:", ["Upload Existing Report", "Generate Report from Image"])
            report_text = None
            if report_option == "Upload Existing Report":
                uploaded_image = st.file_uploader("Upload a radiology report", type=["txt"])
                if uploaded_image is not None:
                    report_text = uploaded_image.read().decode("utf-8")
                    st.text_area("Uploaded Report:", report_text, height=150)
            else:
                # report_text = """
                # There is evidence of right lower lobe consolidation with air bronchograms, suggestive of pneumonia.
                # No pleural effusion is seen. The cardiac silhouette is normal in size.
                # """
                uploaded_file = st.file_uploader("Upload an X-ray", type=['jpg', 'jpeg', 'png'], key="unique_key_2")
                report_text = perform_report_generation_chexagent(uploaded_file)
                st.text_area("Generated Report:", report_text, height=150)
            if st.button("Explain Report", key="explain_report_btn") and report_text:
                with st.spinner("Generating explanation..."):
                    explanation = explain_radiology_report(report_text)
                st.markdown("### Simplified Explanation:")
                st.write(explanation)
    if __name__ == "__main__":
        main()