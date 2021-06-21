from django.contrib import admin
from .models import notificacion
from notificacion.base.admin import AbstractNotificacionAdmin


class NotificacionAdmin(AbstractNotificacionAdmin):
	raw_id_fields = ('destinario',)
	list_display = ('destinario', 'actor', 'verbo', 'nivel', 'no_leido', 'publico')
	list_filter = ('nivel', 'no_leido', 'publico', 'timestamp')



admin.site.register(notificacion, NotificacionAdmin)