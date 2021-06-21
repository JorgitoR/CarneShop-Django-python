from django.contrib import admin
from .models import notificacion
from notificacion.base.admin import AbstractNotificacionAdmin


class NotificacionAdmin(AbstractNotificacionAdmin):
	raw_id_fields = ('destinario',)
	list_display = ('destinario', 'actor', 'verbo', 'nivel', 'no_leido', 'publico')
	list_filter = ('nivel', 'no_leido', 'publico', 'timestamp')

	def get_queryset(self, request):
		qs = super(NotificacionAdmin, self).get_queryset(request)
		return qs.prefetch_related('actor')


admin.site.register(notificacion, NotificacionAdmin)