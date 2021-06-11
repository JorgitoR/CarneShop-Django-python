from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe, escape

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericRelation

from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save


class Usuario(AbstractUser):
	admin = models.BooleanField(default=False)
	cliente = models.BooleanField(default=False)



class categoria(models.Model):
	nombre = models.CharField(max_length=100)
	color = models.CharField(max_length=7, default="#333")


	def get_categoria(self):
		nombre = escape(self.nombre)
		color = escape(self.color)
		html = '<span style="background:%s">%s</span>' % (self.color, self.nombre)
		return mark_safe(html)



class OrdenarProducto(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, verbose_name="selecionar producto", on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField(verbose_name="Id del producto")
	content_object = GenericForeignKey('content_type', 'object_id')

	ordenado = models.BooleanField(default=False)
	cantidad = models.IntegerField(default=1)

	def __str__(self):
		return self.usuario.username



class Orden(models.Model):
	class Estados(models.TextChoices):
		PROCESO = "EN PROCESO DE ENTREGA", "En proceso de entrega",
		ENTREGADO = "ENTREGADO", "Entregado",
		DEVOLUCION = "DEVOLUCION", "Devolucion"

	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ordenar')
	productos = models.ManyToManyField(OrdenarProducto, through='pedidos')
	date = models.DateTimeField(auto_now_add=True)
	ordenado = models.BooleanField(default=False)

	cupon = models.ForeignKey('Cupon', on_delete=models.SET_NULL, blank=True, null=True)
	estado = models.CharField(max_length=100, choices=Estados.choices)


class pedidos(models.Model):
	pedidos = models.ForeignKey(OrdenarProducto, on_delete=models.CASCADE)
	orden = models.ForeignKey(Orden, on_delete=models.CASCADE)

	def __str__(self):
		return self.pedidos.content_object.titulo

class Cupon(models.Model):
	codigo = models.CharField(max_length=15)
	valor = models.FloatField()

	def __str__(self):
		return self.codigo

class producto(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="producto")
	categoria = models.ForeignKey(categoria, on_delete=models.CASCADE, related_name="producto")
	titulo = models.CharField(max_length=100)
	texto = models.TextField()
	img = models.ImageField(upload_to='producto/%Y/%M/%d', null=True, blank=True, verbose_name='Imagen')

	pedido = GenericRelation(OrdenarProducto, related_query_name='pedido')

	stock = models.IntegerField(default=0, verbose_name='Stock')
	precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

	slug = models.SlugField(blank=True, null=True, unique=True)

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(producto)
		return content_type


def crear_url(instance, nueva_url=None):
	slug =  slugify(instance.titulo)
	if nueva_url is not None:
		slug =  nueva_url

	return slug


def slug_save(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = crear_url(instance)

pre_save.connect(slug_save, sender=producto)