from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario, direccion

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



class DirecionForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['ciudad'].widget.attrs['autofocus'] = True

	class Meta:
		model = direccion
		fields = [
			'ciudad',
			'barrio',
			'kind_address',
			'direccion',
			'hastag',
			'numero1',
			'numero2'
		]