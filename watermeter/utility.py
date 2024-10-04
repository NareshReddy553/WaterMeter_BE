import json
import os
from pathlib import Path
from django.shortcuts import get_object_or_404
from ninja import UploadedFile
import google.generativeai as genai

from account.models import Flat


def save_temp_image(self, image: UploadedFile) -> Path:
  """
  Saves the uploaded image to a temporary path and returns the file path.
  """
  media_path = Path("media") / image.name
  with open(media_path, 'wb') as f:
      f.write(image.read())
  return media_path
      
def cleanup_temp_image(self, media_path: Path):
  """
  Removes the temporary image file after processing.
  """
  os.remove(media_path)
  
def process_image(self, media_path: Path) -> dict:
  """
  Uploads the image to the AI model and processes the result.
  """
  genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
  
  myfile = genai.upload_file(media_path)

  model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))
  
  result = model.generate_content(
      [myfile, "\n\n",
        "Extract the 'kilolitres' and 'serial_number' from the water meter image. "
        "Ensure the 'serial_number' is unique, and 'kilolitres' represents the amount of water consumed in liters as a number. "
        "If the image is upside down or incorrectly oriented, correct the orientation and read the values properly. "
        "If you're unable to read any data, return an error stating that the image is unclear and needs to be reuploaded. "
        "Ensure that the 'kilolitres' value is a number without unnecessary leading zeros. "
        "Return the data in the following JSON format with the unique key and reading: "
        '{"kilolitres": "XXXXX", "serial_number": "XXXXX"}.']
  )
  extracted_data = json.loads(result.text)
  
  return extracted_data

def extract_kilolitres_and_serial(self, extracted_data: dict) -> tuple:
  """
  Extracts the kilolitres and serial_number from the processed JSON data.
  """
  kilolitres = str(extracted_data['kilolitres']).lstrip('0')  # Remove leading zeros
  kilolitres = int(kilolitres) if kilolitres else 0
  serial_number = extracted_data['serial_number']
  return kilolitres, serial_number

def find_flat_and_user_by_serial(self, serial_number: str) -> tuple:
  """
  Finds the flat and user associated with the given serial number.
  """
  # Assuming 'serial_number' is unique in the Flat model
  flat = get_object_or_404(Flat, meter_no=serial_number)
  user = flat.user  # Assuming Flat has a related field 'user'
  return flat, user