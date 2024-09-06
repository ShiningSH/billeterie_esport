from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Event, Ticket

class EventAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_debut', 'date_fin', 'prix_premier_jour', 'prix_finale')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'type', 'date', 'prix')

admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)

# Personnaliser le site admin pour ajouter un lien vers le tableau de bord
class CustomAdminSite(admin.AdminSite):
    site_header = 'Administration de la Billetterie'

    def each_context(self, request):
        context = super().each_context(request)
        context['dashboard_url'] = reverse('dashboard')
        return context

admin_site = CustomAdminSite(name='custom_admin')

# Enregistrer vos modèles avec le site personnalisé
admin_site.register(Event, EventAdmin)
admin_site.register(Ticket, TicketAdmin)
