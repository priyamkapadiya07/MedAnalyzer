import pytesseract
from PIL import Image
import re
import joblib
from difflib import SequenceMatcher
import numpy as np
import os
import fitz
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

diabetes_model = joblib.load("analyzer_app/ml_model/diabetes_model.pkl")
anemia_model = joblib.load("analyzer_app/ml_model/anemia_model.pkl")
heart_model = joblib.load("analyzer_app/ml_model/heart_model.pkl")

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        print(f"❌ Image OCR failed: {e}")
        return ""

# Extract text from PDF (with OCR fallback)
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text().strip()
            if not text:
                images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
                text = pytesseract.image_to_string(images[0])
            full_text += text + "\n"
        doc.close()
        return full_text
    except Exception as e:
        print(f"❌ PDF text extraction failed: {e}")
        return ""

def parse_to_dict(text):
    result = {}
    lines = text.splitlines()

    for line in lines:
        match = re.match(r'^(.*?):\s*([\d.]+)', line)
        if match:
            test_name = match.group(1).strip()
            value = match.group(2).strip()
            try:
                result[test_name] = float(value)
            except ValueError:
                result[test_name] = value
    return result

def extract_report_data(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".pdf"]:
        raw_text = extract_text_from_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        raw_text = extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file type!")

    return parse_to_dict(raw_text)

def predict_diseases(data):
    results = {}
    
    # # Glucose: 13.5 – 17.5 g/dL (males) , 12.0 – 15.5 g/dL (females)
    # if data.get("Glucose"):
    #     results["Diabetes"] = "Yes" if diabetes_model.predict([[data["Glucose"]]])[0] == 1 else "No"
        
    # # Hemoglobin: 70 – 99 mg/dL (fasting)
    # if data.get("Hemoglobin"):
    #     results["Anemia"] = "Yes" if anemia_model.predict([[data["Hemoglobin"]]])[0] == 1 else "No"
        
    # # Cholesterol: < 200 mg/dL (desirable)
    # if data.get("Cholesterol"):
    #     results["Heart Disease"] = "Yes" if heart_model.predict([[data["Cholesterol"]]])[0] == 1 else "No"

    # Hemoglobin: 12 – 16 g/dL (Normal)
    if data.get("Hemoglobin"):
        hb = float(data["Hemoglobin"])
        if hb < 12:
            results["Anemia"] = "Yes"
        elif hb > 16:
            results["Polycythemia"] = "Yes"
        else:
            results["Hemoglobin Status"] = "Normal"

    # Glucose: 70 – 110 mg/dL (Fasting Normal)
    if data.get("Glucose"):
        glucose = float(data["Glucose"])
        if glucose < 70:
            results["Hypoglycemia"] = "Yes"
        elif glucose > 110:
            results["Diabetes"] = "Yes"
        else:
            results["Glucose Status"] = "Normal"

    # Cholesterol: 125 – 200 mg/dL (Normal)
    if data.get("Cholesterol"):
        chol = float(data["Cholesterol"])
        if chol < 125:
            results["Low Cholesterol"] = "Yes"
        elif chol > 200:
            results["Heart Disease Risk"] = "Yes"
        else:
            results["Cholesterol Status"] = "Normal"

    
    # WBC: 4,000 – 11,000 /µL
    if data.get("WBC"):
        wbc = float(data["WBC"])
        if wbc > 11000:
            results["Infection"] = "Yes"
        elif wbc < 4000:
            results["Leukopenia"] = "Yes"
        else:
            results["WBC Status"] = "Normal"

    # PLT: 150,000 – 450,000 /µL
    if data.get("PLT"):
        plt = float(data["PLT"])
        if plt < 150000:
            results["Thrombocytopenia"] = "Yes"
        elif plt > 450000:
            results["Thrombocytosis"] = "Yes"
        else:
            results["Platelet Status"] = "Normal"

    # MCV: 80 – 100 fL
    if data.get("MCV"):
        mcv = float(data["MCV"])
        if mcv < 80:
            results["Microcytic Anemia"] = "Yes"
        elif mcv > 100:
            results["Macrocytic Anemia"] = "Yes"
        else:
            results["MCV Status"] = "Normal"

    # ESR: 0 – 20 mm/hr
    if data.get("ESR"):
        esr = float(data["ESR"])
        if esr > 20:
            results["Inflammation"] = "Yes"
        else:
            results["ESR Status"] = "Normal"


    return results

def suggest_medicines(diseases):
    med_dict = {
        "Diabetes": [
            "Metformin", "Insulin", "Glipizide", "Dapagliflozin", "Sitagliptin"
        ],
        "Hypoglycemia": [
            "Glucose tablets", "Dextrose IV", "Glucagon injection", "Fruit juice", "Candy"
        ],
        "Anemia": [
            "Iron supplements", "Folic acid", "Vitamin B12", "Erythropoietin"
        ],
        "Polycythemia": [
            "Hydroxyurea", "Aspirin (low-dose)", "Phlebotomy", "Interferon-alpha"
        ],
        "Heart Disease": [
            "Statins", "Beta blockers", "ACE inhibitors", "Aspirin", "Nitroglycerin"
        ],
        "Heart Disease Risk": [
            "Lifestyle changes (diet, exercise)", "Statins", "Ezetimibe", "Fibrates"
        ],
        "Low Cholesterol": [
            "Balanced diet with healthy fats", "Niacin", "Omega-3 supplements"
        ],
        "Infection": [
            "Amoxicillin", "Azithromycin", "Ceftriaxone", "Ibuprofen", "Paracetamol"
        ],
        "Leukopenia": [
            "Filgrastim (G-CSF)", "Antibiotic prophylaxis", "Immune boosters", "B12 and folate"
        ],
        "Thrombocytopenia": [
            "Platelet transfusion", "Eltrombopag", "Steroids", "IVIG", "Romiplostim"
        ],
        "Thrombocytosis": [
            "Aspirin (low-dose)", "Hydroxyurea", "Anagrelide", "Plateletpheresis (in extreme cases)"
        ],
        "Microcytic Anemia": [
            "Ferrous sulfate", "Vitamin C", "Folic acid", "Iron-rich diet"
        ],
        "Macrocytic Anemia": [
            "Vitamin B12", "Folic acid", "Hydroxycobalamin", "Dietary changes"
        ],
        "Inflammation": [
            "NSAIDs", "Prednisone", "Colchicine", "Corticosteroids"
        ]
    }

    meds = {}
    has_disease = False
    for disease, status in diseases.items():
        if status == "Yes":
            meds[disease] = med_dict.get(disease, [])
            has_disease = True

    if not has_disease:
        meds["Status"] = ["🎉 You are healthy. No medication needed!"]
    return meds
