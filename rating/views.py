from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType 
from django.http import HttpResponseRedirect


from .forms import RatingForm
from .models import rating


def RatingView(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = RatingForm(request.POST or None)
		if form.is_valid():
			puntaje = form.cleaned_data.get('rating')
			content_type = form.cleaned_data.get('content_type_id')
			object_id = form.cleaned_data.get('object_id')
