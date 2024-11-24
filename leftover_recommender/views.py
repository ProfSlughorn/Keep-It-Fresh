import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_preferences.utils import get_global_household_staples


def get_access_token(client_id, client_secret):
    """
    Fetches an access token from FatSecret API.
    """
    print("Fetching access token...")
    url = "https://oauth.fatsecret.com/connect/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "basic",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, headers=headers, data=data)

    # Log the response for debugging
    print("Access token response status:", response.status_code)
    print("Access token response text:", response.text)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Access token fetched successfully:", access_token)
        return access_token
    else:
        print("Error fetching access token:", response.status_code, response.text)
        raise Exception(f"Failed to get access token: {response.text}")


def get_recipes(access_token, search_expression, max_results=10, page_number=0):
    """
    Fetches recipes matching the search expression from FatSecret API.
    """
    url = "https://platform.fatsecret.com/rest/recipes/search/v3"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "search_expression": search_expression,
        "max_results": max_results,
        "page_number": page_number,
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")


def get_recipe_details(access_token, recipe_id):
    """
    Fetches detailed information about a recipe by its ID from FatSecret API.
    """
    url = "https://platform.fatsecret.com/rest/recipe/v2"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "recipe_id": recipe_id,
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")


def match_recipes(access_token, user_ingredients, household_staples, max_results=10):
    """
    Matches recipes based on user ingredients and household staples.
    """
    all_matched_recipes = []
    for ingredient in user_ingredients:  # Search for each user ingredient
        recipes = get_recipes(access_token, ingredient, max_results=max_results)
        if "recipes" in recipes and "recipe" in recipes["recipes"]:
            for recipe in recipes["recipes"]["recipe"]:
                recipe_id = recipe["recipe_id"]

                # Fetch detailed recipe information
                recipe_details = get_recipe_details(access_token, recipe_id)
                if "recipe" not in recipe_details:
                    continue  # Skip this recipe if details are missing

                # Extract ingredients from recipe
                ingredients_data = recipe_details["recipe"].get("ingredients", {}).get("ingredient", [])
                recipe_ingredients = [
                    ingredient["food_name"].lower() for ingredient in ingredients_data
                ] if isinstance(ingredients_data, list) else []

                # Matching logic
                matched = [
                    ingredient
                    for ingredient in recipe_ingredients
                    if any(user_ing in ingredient for user_ing in (user_ingredients + household_staples))
                ]
                total_ingredients = len(recipe_ingredients)
                match_percentage = (len(matched) / total_ingredients) * 100 if total_ingredients > 0 else 0

                if match_percentage < 50:  # Skip recipes with less than 50% match
                    continue

                # Get preparation and cooking times
                preparation_time = recipe_details["recipe"].get("preparation_time_min", "N/A")
                cooking_time = recipe_details["recipe"].get("cooking_time_min", "N/A")

                # Get recipe image URL
                recipe_images = recipe_details["recipe"].get("recipe_images", {}).get("recipe_image", [])
                recipe_image = (
                    recipe_images if isinstance(recipe_images, str) else recipe_images[0] if recipe_images else "N/A"
                )

                # Append recipe with match percentage
                all_matched_recipes.append(
                    {
                        "recipe_name": recipe_details["recipe"]["recipe_name"],
                        "matched_ingredients": matched,
                        "missing_ingredients": [
                            ingredient
                            for ingredient in recipe_ingredients
                            if ingredient not in matched
                        ],
                        "match_percentage": match_percentage,
                        "preparation_time": preparation_time,
                        "cooking_time": cooking_time,
                        "recipe_image": recipe_image,
                    }
                )

    # Sort recipes by match_percentage, descending
    return sorted(all_matched_recipes, key=lambda x: x["match_percentage"], reverse=True)



@csrf_exempt
def recommend_recipes(request):
    """
    API endpoint to recommend recipes based on leftover ingredients.
    """
    print("Received recommend_recipes POST request.")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Parsed request body:", data)
            user_ingredients = data.get('ingredients', [])

            if not isinstance(user_ingredients, list):
                print("Error: Ingredients must be a list")
                return JsonResponse({'error': 'Ingredients must be a list'}, status=400)

            if not user_ingredients:
                print("Error: No ingredients provided")
                return JsonResponse({'error': 'No ingredients provided'}, status=400)

            household_staples = get_global_household_staples()
            print("Fetched household staples from database:", household_staples)

            CLIENT_ID = "4e3672bde10043e4b3f0b89b33f408a6"
            CLIENT_SECRET = "44b56dd7199e4d2286807ca4aa787774"
            access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
            print("Fetched access token:", access_token)

            recipes = match_recipes(access_token, user_ingredients, household_staples, max_results=10)
            print("Matched recipes:", recipes)
            return JsonResponse({'recipes': recipes}, status=200)
        except Exception as e:
            print("Error occurred:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    print("Invalid request method")
    return JsonResponse({'error': 'Invalid request method'}, status=405)
