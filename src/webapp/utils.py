

def get_disease_list():
    return ["No Finding", "Enlarged Cardiomediastinum", "Cardiomegaly", "Lung Opacity",
                            "Lung Lesion", "Edema", "Consolidation", "Pneumonia", "Atelectasis",
                            "Pneumothorax", "Pleural Effusion", "Fracture"]

def get_disease_info():
    return {
            "No Finding": "No significant abnormality detected in the X-ray image.",
            "Enlarged Cardiomediastinum": "Increase in the size of the mediastinum, which may suggest the presence of various conditions including lymphadenopathy or mass lesions.",
            "Cardiomegaly": "Enlargement of the heart's size, often indicative of heart disease or high blood pressure.",
            "Lung Opacity": "Any area of increased opacity in the lung can indicate a range of issues, from infection to chronic disease.",
            "Lung Lesion": "A localized abnormality in the lung which can be benign or malignant. Further testing is usually required.",
            "Edema": "Swelling caused by excess fluid trapped in the body's tissues, which can be seen in pulmonary edema as fluffy opacities in the lungs.",
            "Consolidation": "Region of normally compressible lung tissue that has filled with liquid instead of air. It is typically a result of pneumonia.",
            "Pneumonia": "Infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus.",
            "Atelectasis": "Partial or complete collapse of the lung or a section (lobe) of a lung.",
            "Pneumothorax": "An abnormal collection of air in the pleural space between the lung and the chest wall, causing the lung to collapse.",
            "Pleural Effusion": "Accumulation of excess fluid between the layers of the pleura outside the lungs.",
            "Fracture": "Any break in the bones, which can involve ribs or other bones visible in an X-ray of the chest."
        }