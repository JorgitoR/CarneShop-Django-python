from django.urls import path

from .views import RegistrarceView

urlpatterns = [

	path('registro/', RegistrarceView.as_view(), name='')
]