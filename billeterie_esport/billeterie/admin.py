from django.contrib import admin
from .models import Event, Ticket

class EventAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_debut', 'date_fin', 'prix_premier_jour', 'prix_finale')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'type', 'date', 'prix')

admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
