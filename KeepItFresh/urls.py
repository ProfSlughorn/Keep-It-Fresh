from django.contrib import admin
from django.urls import path, include
from shopping_list.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shopping-list/', include('shopping_list.urls')),
    path('', homepage),  # Root URL points to homepage view
]
