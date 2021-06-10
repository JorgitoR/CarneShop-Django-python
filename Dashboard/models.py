from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe, escape

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 

class Usuario(AbstractUser):
	admin = models.BooleanField(default=False)
	cliente = models.BooleanField(default=False)



class categoria(models.Model):
	nombre = models.CharField(max_length=100)
	color = models.CharField(max_length=7, default="#333")


	def get_categoria(self):
		nombre = escape(self.nombre)
		color = escape(self.color)
		html = '<span style="background:%s">%s</span>' (self.color, self.nombre)
		return mark_safe(html)



class OrdenarProducto(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, verbose_name="selecionar producto")
	object_id = models.PositiveIntegerField(verbose_name="Id del producto")
	content_object = GenericForeignKey('content_type', 'object_id')

	ordenado = models.BooleanField(default=False)
	cantidad = models.IntegerField(default=1)

	def __str__(self):
		return self.usuario.username


class producto(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="producto")
	categoria = models.ForeignKey(categoria, on_delete=models.CASCADE, related_name="producto")
	titulo = models.CharField(max_length=100)
	texto = models.TextField()
