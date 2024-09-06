from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('billeterie.urls')),  # Redirige vers les URL de l'application billeterie
]
