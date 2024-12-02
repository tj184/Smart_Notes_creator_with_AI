import pyautogui
import time
import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import ollama

import requests


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def screen_record(duration=10, interval=1, output_folder="screenshots"):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    start_time = time.time()
    counter = 0
    
    while time.time() - start_time < duration:
      
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(output_folder, f"screenshot_{counter}.png"))
        counter += 1
        time.sleep(interval)

    print("Screen recording completed.")


API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

def query(folder="screenshots"):
    text=""
    text2=""

    image_files = [f for f in os.listdir(folder) if f.endswith('.png')]
    
    for image_file in image_files:
        image_path = os.path.join(folder, image_file)
        text2+=extract_text_from_image(image_path)
        with open(image_path, "rb") as f:
            data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            text+=str(response.json())
    return text,text2

def extract_text_from_image(image_path):
    
    image = Image.open(image_path)

    
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    extracted_text = pytesseract.image_to_string(image_cv)

    return extracted_text



            

screen_record(duration=10, interval=2)
a=query()
desiredmodel='llama3.2:3b'
ask="Format the following data and provide summary for and keypoints as well as define the key points of the following :"+ str(a)
response=ollama.chat(model=desiredmodel,messages=[{
    'role':'user',
    'content':ask,
},
])

final=response['message']['content']
with open('text.txt','w',encoding='utf-8') as text_file:
    text_file.write(final)