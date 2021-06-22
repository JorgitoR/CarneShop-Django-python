from django.urls import path

from .views import (Notificaciones)

urlpatterns = [

	path('notificaciones/', Notificaciones.as_view(), name='notificaciones')

]