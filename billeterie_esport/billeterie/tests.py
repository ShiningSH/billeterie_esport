""""
# Test pour la méthode get_prix :
from django.test import TestCase
from .models import Event
from datetime import date

class EventModelTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            nom="Festival",
            date_debut="2024-12-01",
            date_fin="2024-12-10",
            prix_premier_jour=50.00,
            prix_finale=30.00
        )

    def test_get_prix_first_day(self):
        self.assertEqual(self.event.get_prix(self.event.date_debut), 50.00)

    def test_get_prix_last_day(self):
        self.assertEqual(self.event.get_prix(self.event.date_fin), 30.00)

    def test_get_prix_other_day(self):
        self.assertEqual(self.event.get_prix(date(2024, 12, 5)), 50.00)
"""

# Tests pour la méthode save dans Ticket :
# billeterie/tests.py
from django.test import TestCase
from .models import Ticket, Event, User

class TicketModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(nom="Doe", prenom="John", email="john.doe@example.com")
        self.event = Event.objects.create(
            nom="Concert",
            date_debut="2024-12-01",
            date_fin="2024-12-01",
            prix_premier_jour=80.00,
            prix_finale=70.00
        )
        
    def test_ticket_save_individual(self):
        ticket = Ticket.objects.create(
            type="individuel",
            date=self.event.date_debut,
            user=self.user,
            event=self.event
        )
        self.assertEqual(ticket.prix, 80.00)

    def test_ticket_save_multipass(self):
        ticket = Ticket.objects.create(
            type="multipass",
            user=self.user,
            event=self.event
        )
        self.assertEqual(ticket.prix, 30.00)

    def test_get_prix(self):
        # Cas où la date est la date de début
        self.assertEqual(self.event.get_prix(self.event.date_debut), 80.00)
        
        # Cas où la date est la date de fin
        self.assertEqual(self.event.get_prix(self.event.date_fin), 70.00)
        
        # Cas où la date est une autre date
        self.assertEqual(self.event.get_prix(self.event.date_debut + timedelta(days=1)), 80.00)
