import sys
sys.path.append('home/cmottez/aiXperts/src/models')
from models.model_loader import load_mistral_model
import torch


# # Use a pipeline as a high-level helper
# from transformers import pipeline

# messages = [
#     {"role": "user", "content": "Who are you?"},
# ]
# pipe = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")
# pipe(messages)

# # Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
# model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")



def get_mistral_model():
    return load_mistral_model()

def explain_radiology_report(report_text):
    """
    Takes a radiology report as input and generates a simplified explanation.
    """
    # Load model inside function
    mistral_tokenizer, mistral_model = get_mistral_model()
    
    prompt = f"<s>[INST] Explain the following radiology report in simple and short terms for a non-medical person:\n\n{report_text}\n\nExplanation: [/INST]"
    # prompt = f"<s>[INST] Explain the following chest x-ray report in simple and short terms for a non-medical person:\n{report_text}[/INST]"
    
    inputs = mistral_tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        output = mistral_model.generate(**inputs, max_new_tokens=300, temperature=0.7, top_p=0.9)
    
    explanation = mistral_tokenizer.decode(output[0], skip_special_tokens=True)

    start = explanation.find('Explanation')   # Find the first newline after the prompt part and adjust if your output format is different
    explanation = explanation[start:].strip()  # Strip leading and trailing whitespace

    return explanation


