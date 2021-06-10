from rest_framework.response import Response 

from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from .serializers import(
		RegistroSerializer,	
	)


class RegistrarceView(generics.CreateAPIView):

	permission_classes=[permissions.AllowAny]
	serializer_class = RegistroSerializer

	def create(self, request, *args, **kwargs):
		usuario = super().create(request, *args, **kwargs)
		print(usuario)
		return Response({
			'status':200,
			'data': usuario.data
		})