import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import base64
from io import BytesIO
import requests
import tempfile
from .access_token import get_access_token  # Assuming get_access_token function is in access_token.py


def resize_and_compress_image(image_path, max_width=800, max_height=800, quality=85):
    """
    Resize and compress the image to ensure it meets the API's size requirements.

    Args:
        image_path (str): Path to the image file.
        max_width (int): Maximum width of the resized image.
        max_height (int): Maximum height of the resized image.
        quality (int): Quality of the compressed image (1-100).

    Returns:
        str: Base64-encoded string of the resized and compressed image.
    """
    with Image.open(image_path) as img:
        # Resize image while maintaining aspect ratio
        img.thumbnail((max_width, max_height), Image.LANCZOS)

        # Compress image to reduce size
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)

        # Convert to Base64
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return img_base64


def recognize_food(image_path, access_token):
    """
    Sends an image to the FatSecret Image Recognition API and returns food names.

    Args:
        image_path (str): Path to the image file.
        access_token (str): Access token for FatSecret API.

    Returns:
        dict: API response containing recognized food items.
    """
    # Resize and compress image before sending
    image_base64 = resize_and_compress_image(image_path)

    url = "https://platform.fatsecret.com/rest/image-recognition/v1"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "image_b64": image_base64,
        "region": "US",
        "language": "en",
        "include_food_data": True
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def analyze_image(request):
    if request.method == 'POST':
        logger.info(f"Received POST request: {request.method}")

        if 'image' not in request.FILES:
            logger.error("No image found in request.")
            return JsonResponse({'error': 'No image found in request.'}, status=400)

        image_file = request.FILES['image']
        logger.info(f"Image received: {image_file.name}")

        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            # Get the access token for the FatSecret API
            CLIENT_ID = "4e3672bde10043e4b3f0b89b33f408a6"
            CLIENT_SECRET = "44b56dd7199e4d2286807ca4aa787774"
            ACCESS_TOKEN = get_access_token(CLIENT_ID, CLIENT_SECRET)
            logger.info(f"Access token retrieved: {ACCESS_TOKEN}")

            # Call the FatSecret Image Recognition API
            result = recognize_food(temp_file_path, ACCESS_TOKEN)
            logger.info(f"API response: {result}")

            # Extract the list of recognized food items
            recognized_foods = [food["food_entry_name"] for food in result.get("food_response", [])]

            # Return the recognized food items as a JSON response
            return JsonResponse({'ingredients': recognized_foods})

        except Exception as e:
            logger.error(f"Error in analyzing image: {e}")
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

    logger.error("Invalid request method or no image found.")
    return JsonResponse({'error': 'Invalid request'}, status=400)

