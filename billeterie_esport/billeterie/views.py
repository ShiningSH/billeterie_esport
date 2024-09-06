from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Ticket, Order, OrderDetail, User
from django.urls import reverse
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count

# Afficher la liste des événements
def event_list(request):
    """Affiche la liste de tous les événements disponibles."""
    events = Event.objects.all()
    return render(request, 'billeterie/event_list.html', {'events': events})

# Acheter un billet pour un événement donné
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        ticket_type = request.POST['type']
        jour = request.POST.get('jour')  # Date choisie si c'est un billet individuel

        # Afficher la date pour débogage
        print(f"Date reçue: {jour}")

        # Convertir la date si elle est fournie
        if jour:
            try:
                jour = date.fromisoformat(jour)  # Convertir en objet date
            except ValueError:
                raise ValidationError("La date fournie est invalide. Assurez-vous qu'elle est au format YYYY-MM-DD.")
        else:
            jour = None  # Assurez-vous que la date est None si non fournie

        user, created = User.objects.get_or_create(email=email, defaults={'nom': nom, 'prenom': prenom})

        # Créer le billet
        if ticket_type == 'multipass':
            ticket = Ticket.objects.create(type='multipass', user=user, event=event)
        else:
            ticket = Ticket.objects.create(type='individuel', user=user, event=event, date=jour)

        return redirect(reverse('ticket_confirmation', args=[ticket.id]))

    return render(request, 'billeterie/buy_ticket.html', {'event': event})

# Confirmer l'achat du billet
def ticket_confirmation(request, ticket_id):
    """Affiche la confirmation d'achat du billet."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'billeterie/ticket_confirmation.html', {'ticket': ticket})

# Afficher les détails d'une commande
def order_details(request, order_id):
    """Affiche les détails d'une commande spécifique."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'billeterie/order_details.html', {'order': order})

 # Tableau de bord
def dashboard(request):
    events = Event.objects.all()
    data = []
    total_entries_individual = 0
    total_entries_multipass = 0
    total_amount = 0

    for event in events:
        tickets = Ticket.objects.filter(event=event)
        entries_individual = tickets.filter(type='individuel').count()
        entries_multipass = tickets.filter(type='multipass').count()
        amount = tickets.aggregate(total=Sum('prix'))['total'] or 0

        data.append({
            'event': event.nom,
            'entries_individual': entries_individual,
            'entries_multipass': entries_multipass,
            'amount': amount,
        })

        total_entries_individual += entries_individual
        total_entries_multipass += entries_multipass
        total_amount += amount

    data.append({
        'event': 'TOTAL',
        'entries_individual': total_entries_individual,
        'entries_multipass': total_entries_multipass,
        'amount': total_amount,
    })

    return render(request, 'billeterie/dashboard.html', {'data': data})