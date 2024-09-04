from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Ticket, Order, OrderDetail, User
from django.http import HttpResponse
from django.urls import reverse
from datetime import date

# Afficher la liste des événements
def event_list(request):
    events = Event.objects.all()
    return render(request, 'billeterie/event_list.html', {'events': events})

# Acheter un billet pour un événement donné
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Récupérer les informations du formulaire
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        ticket_type = request.POST['type']
        jour = request.POST.get('jour')  # Date choisie si c'est un billet individuel
        
        # Créer ou récupérer l'utilisateur
        user, created = User.objects.get_or_create(nom=nom, prenom=prenom, email=email)

        # Créer le billet
        if ticket_type == 'multipass':
            ticket = Ticket.objects.create(type='multipass', user=user, event=event)
        else:
            ticket = Ticket.objects.create(type='individuel', user=user, event=event, date=jour)
        
        # Rediriger vers la page de confirmation
        return redirect('ticket_confirmation', ticket_id=ticket.id)

    return render(request, 'billeterie/buy_ticket.html', {'event': event})

# Confirmer l'achat du billet
def ticket_confirmation(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'billeterie/ticket_confirmation.html', {'ticket': ticket})

# Afficher les détails d'une commande
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'billeterie/order_details.html', {'order': order})
