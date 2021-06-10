from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from rest_framework.response import Response 
from django.http import HttpResponseRedirect

from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from .serializers import(
		RegistroSerializer,	
	)


class RegistrarceView(generics.CreateAPIView):

	permission_classes=[permissions.AllowAny]
	serializer_class = RegistroSerializer

	def create(self, request, *args, **kwargs):
		usuario = super().create(request, *args, **kwargs)
		print(usuario.data)
		return Response({
			'status':200,
			'data': usuario.data
		})

class Login(FormView):
	template_name = 'Usuario/login.html'
	form_class = AuthenticationForm
	success_url = reverse_lazy('home')

	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(Login, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		usuario = authenticate(username=username, password=password)
		token, created = Token.objects.get_or_create(user=usuario)
		if token:
			login(self.request, form.get_user())
			return super(Login, self).form_valid(form)