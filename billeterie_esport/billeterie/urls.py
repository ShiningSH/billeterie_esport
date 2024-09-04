from django.urls import path
from . import views

urlpatterns = [
    # Affichage par défaut de la liste des événements
    path('', views.event_list, name='event_list'),
    # Route pour l'achat de billets
    path('event/<int:event_id>/buy/', views.buy_ticket, name='buy_ticket'),
    # Route pour la confirmation de l'achat
    path('ticket/<int:ticket_id>/confirmation/', views.ticket_confirmation, name='ticket_confirmation'),
]
