import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
from perform_disease_prediction_torchxrayvision import torch_x_ray_prediction


def main():
    st.set_page_config(page_title="Main", page_icon=":computer:", layout="wide")
    st.markdown("<h1 style='text-align: center; color: black;'>DiagnoseMe</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Read Your Rays, Right Away</h3>", unsafe_allow_html=True)

    # Tabs
    tabs = st.tabs(["Home", "Personal Information", "Read Your Rays"])
    tab1, tab2, tab3 = tabs

    

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
            st.write("Filename:", uploaded_file.name)

            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded X-ray.', width=300)

            st.write("Image is ready for processing...")

            disease_list = ["No Finding", "Enlarged Cardiomediastinum", "Cardiomegaly", "Lung Opacity",
                            "Lung Lesion", "Edema", "Consolidation", "Pneumonia", "Atelectasis", 
                            "Pneumothorax", "Pleural Effusion", "Fracture"]

            if 'selected_diseases' not in st.session_state:
                st.session_state.selected_diseases = []

            st.markdown("""
                <style>
                .big-font {
                    font-size:20px !important;
                }
                </style>
                """, unsafe_allow_html=True)

            st.markdown('<p class="big-font">Select diseases you want to test:</p>', unsafe_allow_html=True)


            if 'selected_diseases' not in st.session_state:
                st.session_state.selected_diseases = []

            selected_diseases = st.multiselect("", disease_list, default=st.session_state.selected_diseases)

            if st.button('Select All'):
                st.session_state.selected_diseases = disease_list
                selected_diseases = disease_list

            # selected_diseases = st.multiselect("", disease_list, default=selected_diseases)

            # Add a button Analyze Now!

            # if selected_diseases:
            #     st.write("You selected:", selected_diseases)

            if st.button('Analyze Image'):
            # Call the function from the imported file
                predictions = torch_x_ray_prediction(uploaded_file)
                diseases_in_x_ray = []
                for d in selected_diseases:
                    if predictions[d] == 1:
                        diseases_in_x_ray.append(d)
                    s = ', '.join(diseases_in_x_ray)
                st.write("Predicted diseases:", s)

            





if __name__ == "__main__":
    main()


