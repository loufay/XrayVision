import io
import requests
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from models.CheXagent.chexagent import CheXagent

# huggingface-cli login
# if other gpu set torch.float16 back to torch.bfloat16

def perform_disease_localization(path_to_image, disease=""):
    ##TODO: Remove path
    path_to_image = "/mnt/data2/datasets_lfay/MedImageInsights/data/CheXpert-v1.0-512/images/train/patient04905/study4/view1_frontal.jpg"

    chexagent = CheXagent()

    phrase = f"There is a {disease}."
    response = chexagent.phrase_grounding(path_to_image, phrase)
    print(f'Result: {response}')
    print(f'=' * 42)

    return results

if __name__ == "__main__":
    perform_disease_localization(path_to_image="")