from django.db import models

class User(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.prenom} {self.nom}'


class Event(models.Model):
    nom = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField()
    
    # Prix variable par jour
    prix_premier_jour = models.DecimalField(max_digits=10, decimal_places=2)
    prix_finale = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom

    def get_prix(self, date):
        """Renvoie le prix en fonction de la date de l'événement"""
        if date == self.date_fin:
            return self.prix_finale
        return self.prix_premier_jour


class Ticket(models.Model):
    TYPE_CHOICES = [
        ('individuel', 'Individuel'),
        ('multipass', 'Multipass')
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} - {self.event.nom}'

    def save(self, *args, **kwargs):
        if self.type == 'multipass':
            # Si c'est un Multipass, on fixe un prix unique
            self.prix = 30  # Par exemple
        else:
            # Prix variable selon la date de l'événement
            self.prix = self.event.get_prix(self.date)
        super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commande {self.id} - {self.user.email}'

    def calculate_total(self):
        """Calcule le total de la commande en fonction des tickets"""
        self.total = sum(detail.total_price for detail in self.orderdetail_set.all())
        self.save()


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.price = self.ticket.prix
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Détail Commande {self.order.id} - Billet {self.ticket.id}'
