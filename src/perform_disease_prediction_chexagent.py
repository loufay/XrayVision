import io
import requests
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from models.CheXagent.chexagent import CheXagent

# huggingface-cli login
# if other gpu set torch.float16 back to torch.bfloat16

def perform_disease_prediction_chexagent(path_to_image):
    ##TODO: Remove path
  #  path_to_image = "/mnt/data2/datasets_lfay/MedImageInsights/data/CheXpert-v1.0-512/images/train/patient04905/study4/view1_frontal.jpg"
    print(path_to_image)
    

    if path_to_image is not None:
        # Save it to a temp file
        with open(path_to_image.name, "wb") as f:
            f.write(path_to_image.getbuffer())

        file_path = path_to_image.name
        print(file_path)



    chexagent = CheXagent()

    diseases = [ 
        "Enlarged Cardiomediastinum",
        "Cardiomegaly",
        "Lung Opacity","Lung Lesion",
        "Edema","Consolidation","Pneumonia","Atelectasis","Pneumothorax","Pleural Effusion","Fracture","Support Devices"]

        #response = model.binary_disease_classification([path_to_image], "Pneumothorax")
    prompt = f'Does this chest X-ray contain a Pneumothorax?'

    response = chexagent.disease_identification([file_path], diseases)

    # create dict with all diseases set to 1 if present in response else 0
    results = {}
    for disease in diseases:
        results[disease] = 1 if disease in response else 0
    
        
    if all(value == 0 for value in results.values()):
        results['No Finding'] = 1
    else:
        results['No Finding'] = 0
    
  #  responses = chexagent.findings_generation_section_by_section([path_to_image])
    print(results)
    print("XXXX"*20)
    return results

if __name__ == "__main__":
    perform_disease_prediction_chexagent(path_to_image="")