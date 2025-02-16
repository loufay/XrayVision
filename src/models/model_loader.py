import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 🔹 Cache model loading to avoid reloading on each interaction
@st.cache_resource
def load_mistral_model():
    model_name = "mistralai/Mistral-7B-Instruct-v0.3"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
    return tokenizer, model
