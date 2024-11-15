from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoppingListItemViewSet, homepage

router = DefaultRouter()
router.register(r'items', ShoppingListItemViewSet)

urlpatterns = [
    path('', homepage),  # Add the homepage route
    path('api/', include(router.urls)),  # Include the router with API routes under 'api/'
]
