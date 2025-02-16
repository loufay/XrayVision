import io
import requests
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from models.CheXagent.chexagent import CheXagent

# huggingface-cli login
# if other gpu set torch.float16 back to torch.bfloat16

def perform_report_generation_chexagent(path_to_image):
    ##TODO: Remove path
    # path_to_image = "../data/mimic.jpg"
    print(path_to_image)
    file_path = path_to_image
    

    if path_to_image is not None:
        # Save it to a temp file
        with open(path_to_image.name, "wb") as f:
            f.write(path_to_image.getbuffer())

        file_path = path_to_image.name
        print(file_path)



    chexagent = CheXagent()
    
    responses = chexagent.findings_generation_section_by_section([file_path])
    
    result_string = ""
    for response in responses:
        result_string += f'{response[0]}: {response[1]}\n'
    
    return result_string

if __name__ == "__main__":
    perform_report_generation_chexagent(path_to_image="")