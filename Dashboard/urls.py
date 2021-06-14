from django.urls import path

from .views import (
		add_carrito,
		CheckView,
		minus_cart,
		home,
	)

from .views_user import(
	RegistroView,
	LogOutView,
	perfil,
	DirecionCrear
)

urlpatterns = [
	
	path('registro2/', RegistroView.as_view(), name='registro'),
	path('logout/', LogOutView.as_view(), name='logout'),
	path('perfil/@<username>', perfil, name='perfil'),
	path('crear_direccion/', DirecionCrear.as_view(), name='crear_direccion'),

	path('home/', home, name="home"),
	path('add_carrito/<slug>/', add_carrito, name='add_carrito'),
	path('check_out/', CheckView.as_view(), name='check_out'),
	path('minus_cart/<slug>/', minus_cart, name='minus_cart'),

]