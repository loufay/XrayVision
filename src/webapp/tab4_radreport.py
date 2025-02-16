
import streamlit as st 
import os 
import sys 
from perform_report_explanation_mistral import explain_radiology_report
from perform_report_generation_chexagent import perform_report_generation_chexagent
import csv
from perform_disease_recommendation_perplexity import perform_disease_recommendation_perplexity

def tab4_radreport():
    info = read_csv_to_dict('patient_info.csv')

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


    st.markdown("## Would like some recommendations based on our diagnosis?")

    diseases = [
        "Enlarged Cardiomediastinum",
        "Cardiomegaly",
        "Lung Opacity", "Lung Lesion",
        "Edema", "Consolidation", "Pneumonia", "Atelectasis",
        "Pneumothorax", "Pleural Effusion", "Fracture", "Support Devices"]

    # Dropdown to select disease
    disease = st.selectbox("Select your disease:", diseases)
    if st.button("Get Recommendations", key="qanda"):
        print(info)
        print("###############")
        print(disease)
        # disease = "Pneumonia"
        message = create_message(info, disease)
        print(message)
        with st.spinner("Generating explanation..."):
            explanation = perform_disease_recommendation_perplexity(message)
        st.markdown("### What to do:")
        st.write(explanation)

    

    




def create_message(info, disease):
    sex = info.get('sex', 'N/A')
    age = info.get('age', 'N/A')
    bmi = info.get('BMI', 'N/A')
    smoke = info.get('smoke', 'N/A')
    alcohol = info.get('alcool', 'N/A') 
    current_symptoms = info.get('text', 'N/A')
    if smoke == "No":
        smoke = "don't"
    if smoke == "Yes":
        smoke = ""
    if smoke == "Used to Smoke":
        smoke = "used to"

    if alcohol == "No":
        alcohol = "don't"
    if alcohol == "Yes - Daily":
        alcohol = "daily"
    if alcohol == "Yes - Weekly":
        alcohol = "sometimes"
    if alcohol == "Yes - Occasionally":
        alcohol = "sometimes"

    prompt = (
        f"I am a {age} years old {sex.lower()} with a BMI of {bmi}, "
        f"I {smoke} smoke and {alcohol.lower()} drink alcohol. "
        f"{current_symptoms}. My chest x-ray shows possible {disease.lower()}, "
        "what would you recommend me to do?"
    )
    return prompt





def read_csv_to_dict(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        # Convert the reader to a list and return the first dictionary
        return next(reader, None)  # Returns None if the file is empty


        
