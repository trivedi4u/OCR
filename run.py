import pytesseract
import pandas as pd
import cv2
from PIL import Image
import numpy as np
import os

# Function to preprocess the image for better OCR accuracy
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image

# Function to perform OCR and extract structured data
def extract_table_from_image(folder_path):
    table = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(folder_path, filename)

            preprocessed_image = preprocess_image(image_path)
            pil_image = Image.fromarray(preprocessed_image)
            text = pytesseract.image_to_string(pil_image, config='--psm 6')
            
            # Convert the text to a list of lists for the table structure
            rows = text.strip().split('\n')
            table= table+[row.split() for row in rows]
    return table

# Function to save table to CSV
def save_table_to_csv(table, output_file):
    df = pd.DataFrame(table)
    df.to_csv(output_file, index=False, header=False)

# Main script
folder_path = 'file' # Path to the uploaded image
output_file = 'output.csv'  # Desired output CSV file name

table = extract_table_from_image(folder_path)
save_table_to_csv(table, output_file)
