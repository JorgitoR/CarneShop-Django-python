from django.urls import path

from .views import RegistrarceView, Login

urlpatterns = [

	path('registro/', RegistrarceView.as_view(), name=''),
	path('login/', Login.as_view(), name='login'),
]