from .models import HouseholdStaple

def get_global_household_staples():
    """
    Retrieve the global list of household staples.

    Returns:
        list: A list of ingredient names that represent household staples.
    """
    staples = HouseholdStaple.objects.values_list('ingredient_name', flat=True)
    return list(staples)

def add_global_household_staple(ingredient_name):
    """
    Add a new ingredient to the global household staples list.

    Args:
        ingredient_name (str): The name of the ingredient to add.
    """
    if not HouseholdStaple.objects.filter(ingredient_name=ingredient_name).exists():
        HouseholdStaple.objects.create(ingredient_name=ingredient_name)

def remove_global_household_staple(ingredient_name):
    """
    Remove an ingredient from the global household staples list.

    Args:
        ingredient_name (str): The name of the ingredient to remove.
    """
    HouseholdStaple.objects.filter(ingredient_name=ingredient_name).delete()

def clear_global_household_staples():
    """
    Remove all entries from the global household staples list.
    """
    HouseholdStaple.objects.all().delete()
