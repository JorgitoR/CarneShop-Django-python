from django.db import models

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
	admin = models.BooleanField(default=False)
	cliente = models.BooleanField(default=False)



