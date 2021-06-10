from django.urls import path

from .views import (
		RegistroView
	)

urlpatterns = [
	
	path('registro2/', RegistroView.as_view(), name='registro')

]