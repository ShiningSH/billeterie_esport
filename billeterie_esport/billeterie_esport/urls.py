from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billeterie/', include('billeterie.urls')),  # Le nom du dossier doit correspondre
]
