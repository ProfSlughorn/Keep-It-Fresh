from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import HouseholdStaple  # Import the HouseholdStaple model
from .utils import (
    get_global_household_staples,
    add_global_household_staple,
    remove_global_household_staple,
    clear_global_household_staples
)

@csrf_exempt
def list_staples(request):
    """
    API endpoint to list all household staples.
    """
    if request.method == 'GET':
        staples = get_global_household_staples()
        return JsonResponse({'staples': staples}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def add_staple(request):
    """
    API endpoint to add a new household staple or multiple staples.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):  # Check if it's a list for bulk addition
                added_ingredients = []
                for ingredient_name in data:
                    if not HouseholdStaple.objects.filter(ingredient_name=ingredient_name).exists():
                        HouseholdStaple.objects.create(ingredient_name=ingredient_name)
                        added_ingredients.append(ingredient_name)
                return JsonResponse(
                    {'message': f'{len(added_ingredients)} ingredients added.', 'added': added_ingredients}, status=201)

            # Handle single ingredient addition
            ingredient_name = data.get('ingredient_name')
            if not ingredient_name:
                return JsonResponse({'error': 'Ingredient name is required'}, status=400)
            if not HouseholdStaple.objects.filter(ingredient_name=ingredient_name).exists():
                HouseholdStaple.objects.create(ingredient_name=ingredient_name)
                return JsonResponse({'message': f'{ingredient_name} added to staples.'}, status=201)
            return JsonResponse({'message': f'{ingredient_name} already exists.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def remove_staple(request):
    """
    API endpoint to remove a household staple.
    """
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            ingredient_name = data.get('ingredient_name')
            if not ingredient_name:
                return JsonResponse({'error': 'Ingredient name is required'}, status=400)
            remove_global_household_staple(ingredient_name)
            return JsonResponse({'message': f'{ingredient_name} removed from staples.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def clear_staples(request):
    """
    API endpoint to clear all household staples.
    """
    if request.method == 'DELETE':
        clear_global_household_staples()
        return JsonResponse({'message': 'All staples cleared.'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
