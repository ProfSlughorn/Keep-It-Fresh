import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import tempfile
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)

# Load YOLO model once, when the Django server starts
MODEL_PATH = 'models/best.pt'  # Adjust the path to your model
yolo_model = YOLO(MODEL_PATH)

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
            # Load the image using PIL
            img = Image.open(temp_file_path)

            # Run YOLOv11 model inference
            results = yolo_model(img)

            # Extract detected class names
            recognized_foods = []
            for result in results:
                for box in result.boxes:
                    if box.cls is not None:  # Check if there's a class assigned to the box
                        recognized_foods.append(yolo_model.names[int(box.cls)])

            logger.info(f"Recognized foods: {recognized_foods}")

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
