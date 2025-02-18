

# install pip install openai streamlit
import os
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)
def structure_radiology_report(report_text):
    prompt = f"""
    You are an expert radiologist assistant. Structure the following radiology report into clear sections:
    
    1. **Findings** - Describe detailed observations from the X-ray.
    2. **Impression** - Summarize the key takeaways in a clinical manner.
    3. **Recommendations** (if applicable) - Suggest any next steps.
    
    Report:
    {report_text}

    Return only the structured text.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a radiology AI assistant."},
                  {"role": "user", "content": prompt}],
        api_key=api_key
    )

    return response["choices"][0]["message"]["content"]

# Example usage
report_text = """There is evidence of right lower lobe consolidation with air bronchograms, suggestive of pneumonia.
No pleural effusion is seen. The cardiac silhouette is normal in size."""

structured_report = structure_radiology_report(report_text)
print(structured_report)
