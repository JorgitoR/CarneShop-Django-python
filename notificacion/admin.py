from django.contrib import admin

class NotificacionAdmin(admin.ModelAdmin):
	raw_id_fields = ('destinario',)
	list_display = ('destinario', 'actor', 'verbo', 'nivel', 'no_leido', 'publico')
	list_filter = ('nivel', 'no_leido', 'publico', 'timestamp')

	def get_queryset(self, request):
		qs = super(NotificacionAdmin, self).get_queryset(request)
		return qs.select_related('actor')