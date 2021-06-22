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



