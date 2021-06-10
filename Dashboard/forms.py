from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario

class RegistroForm(UserCreationForm):

	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta(UserCreationForm.Meta):
		model = Usuario
		fields = [
			"username",
			"password1",
			"password2",
			"email",
			"first_name", 
			"last_name"
		]
		

	def save(self, commit=True):

		usuario = super().save(commit=False)
		usuario.cliente = True

		if commit:
			usuario.save()

		return usuario

