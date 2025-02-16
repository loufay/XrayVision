import streamlit as st
from webapp.utils import get_disease_list, get_disease_info
from perform_disease_prediction_torchxrayvision import torch_x_ray_prediction
from perform_disease_prediction_mi2 import perform_disease_prediction_mi2
from perform_disease_prediction_chexagent import perform_disease_prediction_chexagent
from perform_disease_localization import perform_disease_localization
from PIL import Image
import os

def tab3_xray_analysis():
    st.markdown("## Upload your X-ray!")
    st.markdown("Please upload an X-ray image, and we will display it below.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], key="unique_key_1")

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
            disease_list = get_disease_list()
            all_options = ["Select All"] + disease_list

            if 'selected_diseases' not in st.session_state:
                st.session_state.selected_diseases = []

            selected_diseases = st.multiselect(
                "Please select the diseases you want to test:",
                all_options,
                default=st.session_state.selected_diseases
            )

            if "Select All" in selected_diseases:
                st.session_state.selected_diseases = disease_list
                selected_diseases = disease_list

            if st.button('Analyze Image'):
                with st.spinner("Checking for diseases..."):
                    try:
                        # Perform predictions
                        pred1 = torch_x_ray_prediction(uploaded_file)
                        pred2 = perform_disease_prediction_chexagent(uploaded_file)
                        pred3 = pred2  # Assuming pred3 is the same as pred2
                    except Exception as e:
                        st.error(f"Prediction error: {e}")
                        return  # Stop execution if prediction fails

                try:
                    d1 = [d for d in selected_diseases if pred1.get(d, 0) == 1]
                    predictions = {
                        'Dr1': d1,
                        'Dr2': [d for d in selected_diseases if pred2.get(d, 0) == 1],
                        'Dr3': [d for d in selected_diseases if pred3.get(d, 0) == 1]
                    }
                    all_predicted_diseases = set(predictions['Dr1'] + predictions['Dr2'] + predictions['Dr3'])
                except Exception as e:
                    st.error(f"Error processing predictions: {e}")
                    return

                # Group diseases based on agreement
                disease_groups = {3: [], 2: [], 1: []}
                for disease in all_predicted_diseases:
                    count = sum(disease in predictions[doc] for doc in ['Dr1', 'Dr2', 'Dr3'])
                    disease_groups[count].append(disease)

                diseases_info = get_disease_info()

        st.markdown("<div style='padding: 5px;'></div>", unsafe_allow_html=True)

        st.write("### Detected Diseases based on 3 Assistant Models:")

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
            margin-left: 170px;
            font-size: 12px;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            font-size: 16px;  /* Larger font size on hover */
        }
        </style>
        """, unsafe_allow_html=True)

        if len(all_predicted_diseases) == 0:
            st.write("No diseases detected!")
        else:
            # for prob, diseases in disease_groups.items():
            #     if diseases:
            #         for disease in diseases:
            #             st.write(f"**{disease}** → Agreement: {prob}/3")
            #             st.info(diseases_info.get(disease, "No additional information available."))
            for prob, diseases in disease_groups.items():
                if diseases:
                    for disease in diseases:
                        # Display each disease in a blue box followed by an arrow and the probability
                        # tooltip_html = f'<div style="display: inline-block; padding: 10px; background-color: blue; color: white; border-radius: 5px;">{disease}</div> -->  {prob}/3'
                        tooltip_html = f'<div class="tooltip">{disease}<span class="tooltiptext">{diseases_info[disease]}</span></div> → Agreement{prob}/3'
                        st.markdown(tooltip_html, unsafe_allow_html=True)
                    st.markdown("<div style='padding: 20px;'></div>", unsafe_allow_html=True)


