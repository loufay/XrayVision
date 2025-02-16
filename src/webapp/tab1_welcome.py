
import streamlit as st

def tab1_welcome():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                color: #2E3B55;
                margin-bottom: 10px;
            }
            .sub-title {
                text-align: center;
                font-size: 24px;
                color: #4A6076;
                margin-bottom: 20px;
            }
            .content-box {
                background-color: #F5F7FA;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                font-size: 18px;
                color: #333;
                line-height: 1.6;
                text-align: center;
            }
            .highlight {
                font-weight: bold;
                font-size: 22px;
                color: #007BFF;
            }
            .service-box {
                background: #ffffff;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
                margin-bottom: 20px;
            }
            .service-box:hover {
                transform: scale(1.05);
            }
            .service-icon {
                font-size: 40px;
                margin-bottom: 10px;
                color: #007BFF;
            }
            .service-title {
                font-size: 20px;
                font-weight: bold;
                color: #007BFF;
            }
            .service-text {
                font-size: 16px;
                color: #333;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main Title
    st.markdown('<h3 class="sub-title">Your AI-powered assistant for instant X-ray analysis</h3>', unsafe_allow_html=True)

    # Content Section
    st.markdown(
        """
        <div class="content-box">
            <p>Have you recently had an X-ray and are seeking feedback? 📷</p>
            <p>Already consulted a doctor but looking for a second opinion? 🏥</p>
            <p class="highlight">You're in the right place!</p>
            <p>At <strong>XRayVision</strong>, we provide instant, expert analysis of your X-ray images, 
            helping you understand your health better and faster. Get clarity, confidence, and control over your health decisions today.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Services Section
    st.markdown("<h2 style='text-align: center; color: #2E3B55;'>🩺 Our Services</h2>", unsafe_allow_html=True)

    # Services Data (Icon, Title, Description)
    services = [
        ("📊", "Disease Prediction", "Based on 3 AI models for a more accurate assessment."),
        ("📍", "Highlight Disease Location", "Visualizing the affected areas within your X-ray image.\n"),
        ("📝", "Medical Report Generation", "An AI-powered report based on your X-ray analysis."),
        ("📖", "Report Explanation", "A detailed breakdown of the results in simple terms."),
        ("🎯", "Personalized Recommendations", "Tailored advice based on your diagnosis, demographic, and lifestyle information.")
    ]

    # Display Services in Two Columns
    col1, col2 = st.columns(2)

    for i, (icon, title, description) in enumerate(services):
        with col1 if i % 2 == 0 else col2:
            st.markdown(
                f"""
                <div class="service-box">
                    <div class="service-icon">{icon}</div>
                    <div class="service-title">{title}</div>
                    <div class="service-text">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
