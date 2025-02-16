
import streamlit as st
from webapp.utils import get_disease_list, get_disease_info
from perform_disease_prediction_torchxrayvision import torch_x_ray_prediction
from perform_disease_prediction_mi2 import perform_disease_prediction_mi2
from perform_disease_prediction_chexagent import *
from perform_disease_localization import perform_disease_localization
from PIL import Image

def tab3_xray_analysis():
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
                selected_diseases = disease_list
                st.session_state.selected_diseases = selected_diseases
            if st.button('Analyze Image'):
               
                with st.spinner("Check for diseases..."):

                    try:
                        # Perform predictions
                        pred1 = torch_x_ray_prediction(uploaded_file)
                        pred2 = perform_disease_prediction_chexagent(uploaded_file)
                        pred3 = pred2
                    except:
                        st.write("Prediction error")
                try: 
                    d1 = [d for d in selected_diseases if pred1[d] == 1]
                    predictions = {
                        'Dr1': d1,
                        'Dr2': [d for d in selected_diseases if pred2[d] == 1],
                        'Dr3': [d for d in selected_diseases if pred3[d] == 1]
                    }
                    all_predicted_diseases = set(predictions['Dr1'] + predictions['Dr2'] + predictions['Dr3'])
                except:
                    st.write("No valid X-ray image uploaded.")                   
                
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

                diseases_info = get_disease_info()

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


                st.write("### Detected Diseases based on 3 Assistent Models:")

                if len(all_predicted_diseases) == 0:
                            st.write("No diseases detected!")
                for prob, diseases in disease_groups.items():
                    if diseases:
                        for disease in diseases:
                            tooltip_html = f'<div class="tooltip">{disease}<span class="tooltiptext">{diseases_info[disease]}</span></div> --> {prob}/3'
                            st.markdown(tooltip_html, unsafe_allow_html=True)
                        st.markdown("<div style='padding: 20px;'></div>", unsafe_allow_html=True)
                
                        st.markdown("## Localize Disease")

                # Localize disease
                if uploaded_file is not None:
                    selected_disease = st.session_state.get("selected_disease", None)
                    cols = st.columns(len(all_predicted_diseases) // 2)  # Arrange buttons in two rows
                    for i, disease in enumerate(all_predicted_diseases):
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

                            ##TODO: Change PATH 
                            path_to_localized_disease = "/mnt/data2/datasets_lfay/aiXperts/src/temp/disease_localization.png"
                            # Display localized image
                            st.image(path_to_localized_disease, caption='Localized Disease.', use_container_width=True)