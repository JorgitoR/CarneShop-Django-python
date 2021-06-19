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
			c_type = ContentType.objects.get_for_id(content_type)	
			obj = rating.objects.create(
					usuario = request.user,
					puntaje = puntaje,
					content_type = c_type,
					object_id = object_id
			)		

			next_path = form.cleaned_data.get('siguiente')

	return  HttpResponseRedirect('/')
