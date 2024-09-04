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

    def __str__(self):
        return self.nom

class Ticket(models.Model):
    TYPE_CHOICES = [
        ('individuel', 'Individuel'),
        ('multipass', 'Multipass')
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} - {self.event.nom}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commande {self.id} - {self.user.email}'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Détail Commande {self.order.id} - Billet {self.ticket.id}'
