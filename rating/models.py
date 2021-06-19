from django.db import models

from Dashboard.models import Usuario
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Avg
from django.db.models.signals import pre_save, post_save 

class ClasificacionChoice(models.IntegerChoices):
	UNO = 1
	DOS = 2
	TRES = 3
	CUATRO = 4
	CINCO = 5

	__empty__ = 'Clasifica el servicio'


class RatingQueryset(models.QuerySet):
	def rating(self):
		return self.aggregate(promedio=Avg("puntaje"))["puntaje"]

class RatingManager(models.Manager):
	def get_queryset(self):
		return RatingQueryset(self.model, using=self._db)


class rating(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	puntaje = models.IntegerField(null=True, blank=True, choiices=ClasificacionChoice.choices)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey("content_type", "object_id")

