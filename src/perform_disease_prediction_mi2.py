
from models.medimageinsightmodel import MedImageInsight
import os
import sys
current_dir = os.getcwd()
current_dir = current_dir + "/aiXperts/src/models"
sys.path.append(current_dir)
from PIL import Image
import base64
import io

def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()

def load_model():
    classifier = MedImageInsight(
        model_dir=os.path.join(current_dir, "MedImageInsight/2024.09.27"),
        vision_model_name="medimageinsigt-v1.0.0.pt",
        language_model_name="language_model.pth"
    )

    classifier.load_model()
    classifier.model.to(classifier.device)
    classifier.model.eval()

    return classifier

def perform_disease_prediction_mi2(path_to_image):  

    ##TODO: Remove path to image
    # path_to_image = "42142.jpg"

    # Load model
    classifier = load_model()

    # Read image
    print(path_to_image)
    image = Image.open(path_to_image)

    # Convert the image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()

    # Encode to base64
    img_base64 = base64.encodebytes(img_byte)

    # If you need it as a string
    img_base64_str = img_base64.decode("utf-8")

    disease = [ 
    "Enlarged Cardiomediastinum",
    "Cardiomegaly",
    "Lung Opacity","Lung Lesion",
    "Edema","Consolidation","Pneumonia","Atelectasis","Pneumothorax","Pleural Effusion","Fracture","Support Devices"]

    results = {}
    for disease in disease:
        labels = ["normal", disease, "unclear"]
        result = classifier.predict([img_base64_str], labels)
        disease_present = 1 if max(result[0], key=result[0].get)==disease else 0    
        results[disease] = disease_present
    
    if all(value == 0 for value in results.values()):
        results['No Finding'] = 1
    else:
        results['No Finding'] = 0
    
    ##TODO: Remove print statements
    #print result keys with value 1
    # print([key for key, value in results.items() if value == 1])

    return results

# if __name__ == "__main__":
#     perform_disease_prediction_mi2(path_to_image="../data/42142.jpg")