""""
# Test Unitaires pour la méthode get_prix :
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

"""[KO]
# Tests Unitaires pour la méthode save dans Ticket :
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
"""
""""
# Test Fonctionnels de la vue de liste des événements :
from django.test import TestCase
from django.urls import reverse
from .models import Event

class EventListViewTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            nom="Festival",
            date_debut="2024-12-01",
            date_fin="2024-12-10",
            prix_premier_jour=50.00,
            prix_finale=30.00
        )

    def test_event_list_view(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.nom)
"""

""""
# Test d'intégration d'une commande incluant des détails de commande :
from django.test import TestCase
from .models import User, Event, Ticket, Order, OrderDetail
from decimal import Decimal

class OrderIntegrationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(nom='Doe', prenom='John', email='john.doe@example.com')
        self.event = Event.objects.create(
            nom='Concert',
            date_debut='2024-12-01',
            date_fin='2024-12-01',
            prix_premier_jour=100.00,  # Prix correct pour le test
            prix_finale=120.00  # Prix correct pour le test
        )
        self.ticket1 = Ticket.objects.create(
            type='individuel',
            date='2024-12-01',
            user=self.user,
            event=self.event
        )
        self.ticket2 = Ticket.objects.create(
            type='individuel',
            date='2024-12-01',
            user=self.user,
            event=self.event
        )

        self.order = Order.objects.create(user=self.user, email=self.user.email)
        OrderDetail.objects.create(order=self.order, ticket=self.ticket1, quantity=1)
        OrderDetail.objects.create(order=self.order, ticket=self.ticket2, quantity=1)
        self.order.calculate_total()

    def test_order_total(self):
        print(f'Prix ticket 1: {self.ticket1.prix}')
        print(f'Prix ticket 2: {self.ticket2.prix}')
        print(f'Total de la commande: {self.order.total}')
        self.assertEqual(self.order.total, Decimal('240.00'))  # Ajustez en fonction du calcul correct
"""
"""
# Tests de Bout en Bout (End-to-End)
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from billeterie.models import Event, User, Ticket

class CheckoutE2ETests(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(10)
        super().setUp()

        self.user = User.objects.create(nom="Doe", prenom="John", email="john.doe@example.com")
        self.event = Event.objects.create(
            nom="Concert",
            date_debut="2024-12-01",
            date_fin="2024-12-01",
            prix_premier_jour=100.00,
            prix_finale=80.00
        )
        self.ticket = Ticket.objects.create(
            type="individuel",
            date=self.event.date_debut,
            user=self.user,
            event=self.event
        )

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_checkout_process(self):
        self.selenium.get(f'{self.live_server_url}/billeterie/')
        self.selenium.find_element(By.XPATH, '//button[text()="Acheter"]').click()

        confirmation_message = self.selenium.find_element(By.ID, 'confirmation').text
        self.assertIn("Merci pour votre achat", confirmation_message)
"""

#Test d'achat groupé :
from django.test import TestCase
from .models import User, Event, Ticket, Order, OrderDetail

class TicketPurchaseTest(TestCase):

    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create(nom="brossat", prenom="damien", email="bd@example.fr")
        
        # Créer un événement de test
        self.event = Event.objects.create(
            nom="Tournoi Esport",
            date_debut="2025-04-15",
            date_fin="2025-04-16",
            prix_premier_jour=20.00,
            prix_finale=40.00
        )

    def test_group_ticket_purchase(self):
        # Créer une commande groupée avec plusieurs billets
        order = Order.objects.create(user=self.user, email=self.user.email)

        # Créer trois billets pour des utilisateurs différents sous la même commande
        owners = ["jean", "Bob", "damien"]
        for owner in owners:
            ticket_user = User.objects.create(nom=owner, prenom="Test", email=f"{owner.lower()}@example.com")
            ticket = Ticket.objects.create(
                type='individuel',
                date=self.event.date_debut,
                user=ticket_user,
                event=self.event
            )
            OrderDetail.objects.create(order=order, ticket=ticket, quantity=1)

        # Vérifier que 3 billets ont été associés à la commande
        self.assertEqual(order.orderdetail_set.count(), 3)

        # Vérifier que le total de la commande est correct
        order.calculate_total()
        expected_total = 3 * self.event.get_prix(self.event.date_debut)
        self.assertEqual(order.total, expected_total)

#Billeterie nominative
from django.test import TestCase
from .models import User, Event, Ticket
from datetime import date

class NominativeTicketTest(TestCase):

    def setUp(self):
        # Créer un événement de test
        self.event = Event.objects.create(
            nom="Tournoi Esport",
            date_debut="2024-04-15",
            date_fin="2024-04-16",
            prix_premier_jour=20.00,
            prix_finale=40.00
        )

    def test_nominative_ticket_purchase(self):
        # Créer un utilisateur de test
        user = User.objects.create(nom="Doe", prenom="John", email="john.doe@example.com")
        
        # Acheter un billet pour le premier jour de l'événement
        ticket = Ticket.objects.create(
            type='individuel',
            date=self.event.date_debut,
            user=user,
            event=self.event
        )

        # Vérifier que le billet est associé au bon utilisateur et à la bonne date
        self.assertEqual(ticket.user.nom, "Doe")
        self.assertEqual(ticket.user.prenom, "John")
        self.assertEqual(ticket.user.email, "john.doe@example.com")
        self.assertEqual(ticket.date, self.event.date_debut)


#Prix variable selon le jour
class VariablePriceTest(TestCase):

    def setUp(self):
        # Créer un événement avec deux prix différents pour le premier jour et le jour de la finale
        self.event = Event.objects.create(
            nom="Tournoi Esport",
            date_debut="2024-04-15",
            date_fin="2024-04-16",
            prix_premier_jour=20.00,
            prix_finale=40.00
        )
        # Créer un utilisateur de test
        self.user = User.objects.create(nom="Doe", prenom="John", email="john.doe@example.com")

    def test_price_for_first_day(self):
        # Acheter un billet pour le premier jour
        ticket = Ticket.objects.create(
            type='individuel',
            date=self.event.date_debut,
            user=self.user,
            event=self.event
        )
        # Vérifier que le prix est celui du premier jour
        self.assertEqual(ticket.prix, 20.00)

    def test_price_for_final_day(self):
        # Acheter un billet pour le jour de la finale
        ticket = Ticket.objects.create(
            type='individuel',
            date=self.event.date_fin,
            user=self.user,
            event=self.event
        )
        # Vérifier que le prix est celui du jour de la finale
        self.assertEqual(ticket.prix, 40.00)


#Multipass
class MultipassTicketTest(TestCase):

    def setUp(self):
        # Créer un événement de test
        self.event = Event.objects.create(
            nom="Lyon Esport",
            date_debut="2024-04-15",
            date_fin="2024-04-17",
            prix_premier_jour=20.00,
            prix_finale=40.00
        )
        # Créer un utilisateur pour passer la commande
        self.buyer = User.objects.create(nom="Buyer", prenom="John", email="buyer@example.com")

    def test_multipass_purchase(self):
        # Créer plusieurs multipass pour différentes personnes
        identities = [
            {"nom": "Smith", "prenom": "Alice"},
            {"nom": "Johnson", "prenom": "Bob"},
            {"nom": "Brown", "prenom": "Charlie"}
        ]
        for identity in identities:
            user = User.objects.create(nom=identity["nom"], prenom=identity["prenom"], email=self.buyer.email)
            ticket = Ticket.objects.create(type='multipass', user=user, event=self.event)

            # Vérifier que le prix du multipass est bien fixe
            self.assertEqual(ticket.prix, 30.00)

        # Vérifier que le nombre de Multipass est correct
        tickets = Ticket.objects.filter(type='multipass', event=self.event)
        self.assertEqual(tickets.count(), len(identities))

        for ticket, identity in zip(tickets, identities):
            self.assertEqual(ticket.user.nom, identity["nom"])
            self.assertEqual(ticket.user.prenom, identity["prenom"])
            self.assertEqual(ticket.user.email, self.buyer.email)  # Même email pour tous

