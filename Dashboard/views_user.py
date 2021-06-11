from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, RedirectView
from django.utils import timezone
from .forms import RegistroForm, DirecionForm
from .models import (Usuario,
					direccion)

from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import View

def perfil(request, username=None):
	
	perfil = Usuario.objects.get(username=username)

	context = {
		'perfil':perfil
	}

	return render(request, 'Usuario/perfil.html', context)


class RegistroView(CreateView):
	model = Usuario
	form_class = RegistroForm
	template_name ='Usuario/registro.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['titulo'] = 'Registrate'
		return context

	def form_valid(self, form):
		usuario = form.save()
		login(self.request, usuario)
		return redirect('')

class LogOutView(RedirectView):
	pattern_name = 'login'

	def dispatch(self, request, *args, **kwargs):
		logout(request)
		return super().dispatch(request, *args, **kwargs)

class DirecionCrear(CreateView):
	model = direccion 
	form_class = DirecionForm
	template_name= 'Usuario/address.html'
	success_url=reverse_lazy('')
