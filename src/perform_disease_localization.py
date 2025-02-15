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
    # path_to_image = "/mnt/data2/datasets_lfay/MedImageInsights/data/CheXpert-v1.0-512/images/train/patient04905/study4/view1_frontal.jpg"
    if path_to_image is not None:
        # Save it to a temp file
        with open(path_to_image.name, "wb") as f:
            f.write(path_to_image.getbuffer())

        file_path = path_to_image.name
        print(file_path)

    chexagent = CheXagent()

    phrase = f"There is a {disease}."
    response = chexagent.phrase_grounding(path_to_image, phrase)
    print(f'Result: {response}')
    print(f'=' * 42)


if __name__ == "__main__":
    perform_disease_localization(path_to_image="")