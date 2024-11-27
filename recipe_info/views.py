import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_access_token(client_id, client_secret):
    """
    Fetches an access token from FatSecret API.
    """
    url = "https://oauth.fatsecret.com/connect/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "premier",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def get_recipe_details(access_token, recipe_id):
    """
    Fetches detailed information about a recipe by its ID from FatSecret API.
    """
    url = f"https://platform.fatsecret.com/rest/recipe/v2?recipe_id={recipe_id}&format=json"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

@csrf_exempt
def recipe_detail(request, recipe_id):
    """
    API endpoint to fetch detailed information for a specific recipe.
    """
    if request.method == 'GET':
        try:
            CLIENT_ID = "4e3672bde10043e4b3f0b89b33f408a6"
            CLIENT_SECRET = "44b56dd7199e4d2286807ca4aa787774"
            access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

            # Fetch the recipe details from FatSecret API
            recipe_details = get_recipe_details(access_token, recipe_id)

            # Safely access fields that might not be present
            recipe_data = {
                "recipe_name": recipe_details["recipe"].get("recipe_name", "Unknown Recipe"),
                "recipe_description": recipe_details["recipe"].get("recipe_description", "No description available."),
                "preparation_time": recipe_details["recipe"].get("preparation_time_min", "Not specified"),
                "cooking_time": recipe_details["recipe"].get("cooking_time_min", "Not specified"),
                "serving_size": recipe_details["recipe"].get("serving_sizes", {}).get("serving", {}).get("serving_size", "Not specified"),
                "recipe_image": recipe_details["recipe"].get("recipe_images", {}).get("recipe_image", ["No image available"])[0],
                "nutritional_info": recipe_details["recipe"].get("serving_sizes", {}).get("serving", {}),
            }

            # Filter ingredients to remove unwanted fields
            ingredients = recipe_details["recipe"].get("ingredients", {}).get("ingredient", [])
            filtered_ingredients = []
            for ingredient in ingredients:
                filtered_ingredients.append({
                    "food_name": ingredient.get("food_name", "Unknown Ingredient"),
                    "ingredient_description": ingredient.get("ingredient_description", "No description available")
                })

            recipe_data["ingredients"] = filtered_ingredients

            # Filter directions
            directions = recipe_details["recipe"].get("directions", {}).get("direction", [])
            filtered_directions = []
            for direction in directions:
                filtered_directions.append({
                    "direction_number": direction.get("direction_number", "N/A"),
                    "direction_description": direction.get("direction_description", "No description available")
                })

            recipe_data["directions"] = filtered_directions

            return JsonResponse(recipe_data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

