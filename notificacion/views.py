from django.shortcuts import render, get_object_or_404, redirect


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.views.generic import ListView


from notificacion import settings
from notificacion.settings import get_config

from django.forms import model_to_dict
from swapper import load_model

from django.http import JsonResponse

Notificacion = load_model('notificacion', 'notificacion')


class NotificacionLista(ListView):
	model = Notificacion
	template_name = 'notificacion/lista.html'
	context_object_name = 'notificacion'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(NotificacionLista, self).dispatch(request, *args, **kwargs)


class Notificaciones(NotificacionLista):
	"""
		Pagina index para usuario autenticado
	"""

	def get_queryset(self):
		if settings.get_config()['SOFT_DELETE']:
			qs = self.request.user.notificaciones.activo()
			print('ACTIVO', qs)
		else:
			qs = self.request.user.notificaciones.all()
			print('ALL', qs)

		return qs
