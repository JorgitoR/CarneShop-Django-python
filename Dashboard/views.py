from django.shortcuts import render, redirect

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import RegistroForm
from .models import Usuario

from django.contrib.auth import authenticate, login

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


def home(request):


	return render(request, 'dashboard/home.html')