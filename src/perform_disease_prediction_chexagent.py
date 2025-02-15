import io
import requests
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from models.CheXagent.chexagent import CheXagent

# huggingface-cli login
# if other gpu set torch.float16 back to torch.bfloat16

def perform_disease_prediction_mi2(path_to_image):
    ##TODO: Remove path
    path_to_image = "/mnt/data2/datasets_lfay/MedImageInsights/data/CheXpert-v1.0-512/images/train/patient04905/study4/view1_frontal.jpg"

    chexagent = CheXagent()

    diseases = [ 
        "Enlarged Cardiomediastinum",
        "Cardiomegaly",
        "Lung Opacity","Lung Lesion",
        "Edema","Consolidation","Pneumonia","Atelectasis","Pneumothorax","Pleural Effusion","Fracture","Support Devices"]

        #response = model.binary_disease_classification([path_to_image], "Pneumothorax")
    prompt = f'Does this chest X-ray contain a Pneumothorax?'

    response = chexagent.disease_identification([path_to_image], diseases)

    # create dict with all diseases set to 1 if present in response else 0
    results = {}
    for disease in diseases:
        results[disease] = 1 if disease in response else 0
    
    
    responses = chexagent.findings_generation_section_by_section([path_to_image])

    return results

if __name__ == "__main__":
    perform_disease_prediction_mi2(path_to_image="")