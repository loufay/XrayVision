from model_loader import load_mistral_model  
import torch

def get_mistral_model():
    return load_mistral_model()

def explain_radiology_report(report_text):
    """
    Takes a radiology report as input and generates a simplified explanation.
    """
    # Load model inside function
    mistral_tokenizer, mistral_model = get_mistral_model()
    
    prompt = f"<s>[INST] Explain the following radiology report in simple and short terms for a non-medical person:\n\n{report_text}\n\nExplanation: [/INST]"
    
    inputs = mistral_tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        output = mistral_model.generate(**inputs, max_new_tokens=300, temperature=0.7, top_p=0.9)
    
    explanation = mistral_tokenizer.decode(output[0], skip_special_tokens=True)
    return explanation
