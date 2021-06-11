from django.urls import path

from .views import (
		RegistroView,
		add_carrito,
		CheckView,
		home,
	)

urlpatterns = [
	
	path('registro2/', RegistroView.as_view(), name='registro'),

	path('home/', home, name="home"),
	path('add_carrito/<slug>/', add_carrito, name='add_carrito'),
	path('check_out/', CheckView.as_view(), name='check_out'),

]