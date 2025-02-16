import streamlit as st
import csv

def tab2_add_personal_data():
    st.markdown(
    """
    <div style="text-align: left;">
        <p>
        You don't need to provide your personal information, but they can help us provide better diagnostics and help you understand your images!
    </div>
    <div style="text-align: left; font-style: italic;">
    <p>Note that the information provided will remain confidential and will be deleted at the end of the analysis.
    </div>
    """,
    unsafe_allow_html=True
    )

    info = {"sex": None, "age": None, "BMI": None, "smoke": None, "alcool": None}
    

    with st.form(key='user_details_form'):
        st.write('Please enter your details:')
        sex = st.selectbox('Select your sex:', options=['Male', 'Female', 'Other'])
        age = st.number_input('Age:', min_value=0, max_value=120, step=1, format='%d')
        weight = st.number_input('Weight (in kg):', min_value=0.0, max_value=300.0, step=0.5, format='%f')
        size = st.number_input('Height (in cm):', min_value=0.0, max_value=300.0, step=0.5, format='%f')

        # Select tobacco consumption
        tobacco = st.radio('Do you smoke?', ['Yes', 'No', 'Used to Smoke'])

        # Select alcohol consumption
        alcohol = st.radio('Do you drink alcohol?', ['Yes - Daily', 'Yes - Weekly', 'Yes - Occasionally', 'No'])

        st.write('Something we should be aware of?')
        text = st.text_area("Please provide any relevant information:", height=150)



        info["sex"] = sex
        info["age"] = age
        if weight is not None and size is not None:
            if size != 0:
                info["BMI"] = weight/(size/100)**2
        else:
            info["BMI"] = None
        info['smoke'] = tobacco
        info["alcool"] = alcohol
        info["text"] = text

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            st.write('Thanks for submitting your details!')
            # print(info)
            save_dict_to_csv('patient_info.csv', info)
            
        else:
            sex, age, weight, size, smoke, alcool, text = None, None, None, None, None, None, None
            info["sex"] = sex
            info["age"] = age
            info["BMI"] = None
            info['smoke'] = smoke
            info["alcool"] = alcool
            info["text"] = text



def save_dict_to_csv(filename, data_dict):
    # Open the file in write mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers (dictionary keys)
        writer.writerow(data_dict.keys())
        # Write the values (dictionary values)
        writer.writerow(data_dict.values())