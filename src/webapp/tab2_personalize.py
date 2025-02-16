import streamlit as st

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

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            st.write('Thanks for submitting your details!')