import time
import torch
import torchvision
import skimage.io
import numpy as np
import torchxrayvision as xrv
from sklearn.metrics import roc_auc_score, roc_curve
import streamlit as st

# Cache the model loading to avoid redundant initialization
@st.cache_resource
def load_xray_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = xrv.models.DenseNet(weights="densenet121-res224-all")  # Load DenseNet model
    model.to(device)
    model.eval()  # Set model to evaluation mode
    return model, device

def torch_x_ray_prediction(image_path):
    model, device = load_xray_model()  # Load cached model

    try:
        img = skimage.io.imread(image_path)
        img = xrv.datasets.normalize(img, 255)  # Convert 8-bit image to [-1024, 1024] range
        img = img[None, ...]


        transform = torchvision.transforms.Compose([
            xrv.datasets.XRayCenterCrop(),
            xrv.datasets.XRayResizer(224),
        ])
      
        if len(img.shape) == 4:
            image_tensor = torch.from_numpy(img)
            img = image_tensor.squeeze(0)
            img = img.numpy()
        print(img.shape)  

        img = transform(img)
        img = torch.from_numpy(img).to(device)  # Move tensor to GPU

        outputs = model(img[None, ...])  # Process image through the model
      
        d_pred = dict(zip(model.pathologies, outputs[0].detach().cpu().numpy()))

    except Exception as e:
        print(f"Error processing file {image_path}: {e}")
        return np.zeros(18)  # Return array of 18 zeros if any error occurs


    keys_to_remove = ['Infiltration', 'Emphysema', 'Fibrosis', 'Pleural_Thickening', 'Nodule', 'Mass', 'Hernia']

    d_thresholds = {'Atelectasis': 0.6547774076461792,
    'Consolidation': 0.6521353125572205,
    'Pneumothorax': 0.5432726144790649,
    'Edema': 0.6592536568641663,
    'Pleural Effusion': 0.7849969267845154,
    'Pneumonia': 0.6374650001525879,
    'Cardiomegaly': 0.7481567859649658,
    'Lung Lesion': 0.7703077793121338,
    'Fracture': 0.3942892551422119,
    'Lung Opacity': 0.7328922748565674,
    'Enlarged Cardiomediastinum': 0.6636409759521484}

    for key in keys_to_remove:
        d_pred.pop(key, None)
    
    if 'Effusion' in d_pred:
        d_pred['Pleural Effusion'] = d_pred.pop('Effusion')

    for v in d_pred.keys():
        d_pred[v] = 0 if d_pred[v] <= d_thresholds[v] else 1

    if all(value == 0 for value in d_pred.values()):
        d_pred['No Finding'] = 1
    else:
        d_pred['No Finding'] = 0
    
    # print(d_pred)

    return d_pred

    
