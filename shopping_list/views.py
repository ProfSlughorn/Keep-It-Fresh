from rest_framework import viewsets
from .models import ShoppingListItem
from .serializers import ShoppingListItemSerializer

class ShoppingListItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemSerializer
from django.shortcuts import render

from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Welcome to the Keep It Fresh API. Go to /api/shopping-list/ to see the shopping list.")
