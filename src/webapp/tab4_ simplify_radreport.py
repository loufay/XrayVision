

def tab4_simplify_radreport():
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