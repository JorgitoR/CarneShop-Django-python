from django.urls import path 

from .views import RatingView

urlpatterns = [
	
	path('item-rating', RatingView, name='rating')

]