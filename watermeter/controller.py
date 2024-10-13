import base64
import io
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from ninja_extra import api_controller, route,status
from ninja import File, UploadedFile
import google.generativeai as genai
from pathlib import Path
import os
import tempfile

from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from account.permission import UserWithPermission
from watermeter.models import WaterConsumption
from watermeter.schema import CreateWaterMeterSchema, waterMeterProcessResponseSchema
from watermeter.utility import cleanup_temp_image, extract_kilolitres_and_serial, find_flat_and_user_by_serial, process_image, save_temp_image

# Configure API key for Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@api_controller('/watermeter',tags=['watermeter'],permissions=[IsAuthenticated], auth=JWTAuth())
class MeterImageProcessController:
    """
    API Controller to handle image upload and processing with Google Gemini
    """

    @route.post("image/scan/",response={200: waterMeterProcessResponseSchema, 400: dict}, url_name="Scan meter image",permissions=[UserWithPermission('watermeter.scan_meter')])
    def upload_MeterImg(self, image: UploadedFile = File(...)):
        """
        Uploads an image, processes it using Gemini API, and returns extracted information.
        """
        try:
            # Save the uploaded image temporarily
            media_path = save_temp_image(self,image)

            # Process the image using the AI model
            extracted_data =process_image(self,media_path)    
            
            # Clean up the temporary image file
            cleanup_temp_image(self,media_path) 

            # Extract kilolitres and serial_number from JSON
            kilolitres, serial_number = extract_kilolitres_and_serial(self,extracted_data)

            # Find the flat and user by serial number
            flat, user =find_flat_and_user_by_serial(self,serial_number)


            return {
                "kilolitres": kilolitres,
                "serial_number": serial_number,
                "flat": flat,
                "user": user,
            }
        except json.JSONDecodeError as json_err:
            return {'error': f'JSON Decode Error: {str(json_err)}'}
        except Exception as e:
            return {'error': str(e)}
        
    @route.post('/', response={status.HTTP_201_CREATED: CreateWaterMeterSchema},permissions=[UserWithPermission('watermeter.add_waterconsumption')])
    def create_WaterConsumption(self, payload: CreateWaterMeterSchema):
        """Enter new  a WaterConsumption reading"""
        waterconsumption = WaterConsumption.objects.create(**payload.dict())
        return waterconsumption
