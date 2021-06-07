from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario

class RegistroForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = Usuario

	def save(self, commit=True):

		usuario = super().save(commit=False)
		usuario.cliente = True

		if commit:
			usuario.save()

		return usuario

