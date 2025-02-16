import streamlit as st 

def tab1_welcome():
    
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