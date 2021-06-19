from django import forms
from .models import ClasificacionChoice

class RatingForm(forms.Form):
	rating = forms.ChoiceField(choices=ClasificacionChoice.choice)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	content_type_id = forms.IntegerField(widget=forms.HiddenInput)
	siguiente = forms.CharField(widget=forms.HiddenInput)