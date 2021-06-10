from django.urls import path

from .views import (
		RegistroView,
		home
	)

urlpatterns = [
	
	path('registro2/', RegistroView.as_view(), name='registro'),

	path('home/', home, name="home")

]