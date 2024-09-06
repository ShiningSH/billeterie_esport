from django.urls import path
from . import views

urlpatterns = [
    # Liste des événements
    path('', views.event_list, name='event_list'),

    # Page d'achat de billets pour un événement spécifique
    path('event/<int:event_id>/buy/', views.buy_ticket, name='buy_ticket'),

    # Page de confirmation de l'achat du billet
    path('ticket/<int:ticket_id>/confirmation/', views.ticket_confirmation, name='ticket_confirmation'),

    path('dashboard/', views.admin_dashboard, name='dashboard'),
]
