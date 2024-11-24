from django.urls import path
from .views import list_staples, add_staple, remove_staple, clear_staples

urlpatterns = [
    path('staples/', list_staples, name='list_staples'),
    path('staples/add/', add_staple, name='add_staple'),
    path('staples/remove/', remove_staple, name='remove_staple'),
    path('staples/clear/', clear_staples, name='clear_staples'),
]
