import os

import requests
import torch
from PIL import Image, ImageDraw
from rich import print
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils.logging import set_verbosity_error

class CheXagent(object):
    def __init__(self):

        HF_TOKEN = os.getenv("HF_TOKEN")
        # step 1: Setup constant
        self.model_name = "StanfordAIMI/CheXagent-2-3b"
        self.dtype = torch.float16
        self.device = "cuda"

        # step 2: Load Processor and Model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True, token=HF_TOKEN)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map="auto", trust_remote_code=True, token=HF_TOKEN)
        #self.model = self.model.to(self.device, self.dtype)
        self.model.eval()

    def generate(self, paths, prompt):
        # step 3: Inference
        query = self.tokenizer.from_list_format([*[{'image': path} for path in paths], {'text': prompt}])
        conv = [{"from": "system", "value": "You are a helpful assistant."}, {"from": "human", "value": query}]
        input_ids = self.tokenizer.apply_chat_template(conv, add_generation_prompt=True, return_tensors="pt")
        output = self.model.generate(
            input_ids.to(self.device), do_sample=False, num_beams=1, temperature=1., top_p=1., use_cache=True,
            max_new_tokens=512
        )[0]
        response = self.tokenizer.decode(output[input_ids.size(1):-1])
        return response
    
    def binary_disease_classification(self, paths, disease_name):
        assert isinstance(paths, list)
        assert isinstance(disease_name, str)
        prompt = f'Does this chest X-ray contain a {disease_name}?'
        response = self.generate(paths, prompt)
        return response
    
        
    def disease_identification(self, paths, disease_names):
        assert isinstance(paths, list)
        assert isinstance(disease_names, list)
        prompt = f'Given the CXR, identify any diseases. Options:\n{", ".join(disease_names)}'
        response = self.generate(paths, prompt)
        return response

    def findings_generation(self, paths, indication):
        assert isinstance(paths, list)
        assert isinstance(indication, str)
        prompt = f'Given the indication: "{indication}", write a structured findings section for the CXR.'
        response = self.generate(paths, prompt)
        return response
    
    
    def findings_generation_section_by_section(self, paths):
        assert isinstance(paths, list)
        anatomies = [
            "Airway", "Breathing", "Cardiac",
            "Diaphragm",
            "Everything else (e.g., mediastinal contours, bones, soft tissues, tubes, valves, and pacemakers)"
        ]
        prompts = [f'Please provide a detailed description of "{anatomy}" in the chest X-ray' for anatomy in anatomies]
        responses = []
        for anatomy, prompt in zip(anatomies, prompts):
            response = self.generate(paths, prompt)
            responses.append((anatomy, response))
        return responses
