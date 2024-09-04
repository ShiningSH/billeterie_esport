from django.test import TestCase
from .models import User, Event, Ticket, Order, OrderDetail
from datetime import date

class billeterieTestCase(TestCase):

    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create(nom="Dupont", prenom="Jean", email="jean.dupont@example.com")

        # Créer un événement de test
        self.event = Event.objects.create(
            nom="Lyon ESPORT",
            date_debut=date(2024, 9, 10),
            date_fin=date(2024, 9, 12),
            prix_premier_jour=20.00,
            prix_finale=30.00
        )

    def test_prix_variable_pour_les_billets(self):
        """Test pour vérifier que le prix du billet change selon le jour de l'événement"""

        # Créer un billet pour le premier jour
        ticket_premier_jour = Ticket.objects.create(
            type='individuel',
            user=self.user,
            event=self.event,
            date=self.event.date_debut
        )
        self.assertEqual(ticket_premier_jour.prix, 20.00)

        # Créer un billet pour le dernier jour
        ticket_finale = Ticket.objects.create(
            type='individuel',
            user=self.user,
            event=self.event,
            date=self.event.date_fin
        )
        self.assertEqual(ticket_finale.prix, 30.00)

    def test_multipass(self):
        """Test pour vérifier que le Multipass est bien facturé à un prix fixe"""

        # Créer un Multipass
        multipass = Ticket.objects.create(
            type='multipass',
            user=self.user,
            event=self.event
        )
        self.assertEqual(multipass.prix, 30.00)

    def test_achats_groupes(self):
        """Test pour vérifier que plusieurs billets peuvent être achetés pour le même événement"""

        # Créer une commande
        order = Order.objects.create(user=self.user, email=self.user.email)

        # Créer plusieurs billets pour différents utilisateurs
        ticket1 = Ticket.objects.create(
            type='individuel',
            user=self.user,
            event=self.event,
            date=self.event.date_debut
        )
        ticket2 = Ticket.objects.create(
            type='individuel',
            user=self.user,
            event=self.event,
            date=self.event.date_debut
        )

        # Ajouter les billets à la commande
        OrderDetail.objects.create(order=order, ticket=ticket1, quantity=1, price=ticket1.prix)
        OrderDetail.objects.create(order=order, ticket=ticket2, quantity=1, price=ticket2.prix)

        # Calculer le total
        order.calculate_total()
        self.assertEqual(order.total, 40.00)
