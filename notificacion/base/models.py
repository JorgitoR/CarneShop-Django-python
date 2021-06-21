from django.db import models


from Dashboard.models import Usuario
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils import timezone
from jsonfield.fields import JSONField
#pip install jsonfield

from notificacion.signals import notificar


class NotificacionQuerySet(models.Queryset):
	def no_enviado(self):
		return self.filter(emailed=False)

	def enviado(self):
		return self.filter(emailed=True)

	def no_leido(self, include_deleted=False):
		"""Retornamos solos los item que no han sido leidos en el actual Queryset"""

		return self.filter(no_leido=False)

	


class AbstractNotificacion(models.Model):

	"""
		Formato General:
			<actor> <verbo> <tiempo>
			<actor> <verbo> <objetivo> <tiempo>
			<actor> <verbo> <action_object> <tiempo>
		
		Ejemplo:
			<jorgito> <Tu pedido esta en camino> <Hace 2 minutos>

		Representacion Unicode:
			Jorgito tu pedido esta en camino Hace 2 minutos

		

	"""

	class NIVELES(models.TextChoices):
		exito = 'Exito', 'exito',
		info = 'Informacion', 'informacion',
		advertencia = 'Advertencia', 'advertencia',
		error = 'Error', 'error'

	nivel = models.CharField(choices=NIVELES.choices, default=NIVELES.info, max_length=20)

	destinario = models.ForeignKey(Usuario, on_delete=models.CASCADE, 
					related_name='notificar_destino', blank=True, null=True)

	no_leido = models.BooleanField(default=True, blank=False, db_index=True)
	actor_content_type = models.ForeignKey(ContentType, 
							related_name='notificar_actor', on_delete=models.CASCADE)

	object_id_actor = models.PositiveIntegerField()
	actor = GenericForeignKey("actor_content_type", "object_id_actor")


	verbo = models.CharField(max_length=255)
	descripcion = models.TextField(blank=True, null=True)


	timestamp = models.DateTimeField(default=timezone.now, db_index=True)
	#marca de tiempo

	publico = models.BooleanField(default=True, db_index=True)
	eliminado = models.BooleanField(default=False, db_index=True)
	emailed = models.BooleanField(default=False, db_index=True)
	#emailed = enviado por correo electronico

	data = JSONField(blank=True, null=True)


	class Meta:
		abstract = True
		ordering = ("-timestamp",)
		index_together = ('destinario', 'no_leido')

		#abstract = True 
		#model class that inherits from a django abstract class, 
		#Django will only generate tables for subclasses of models.Model, so the former

	def __str__(self):
		diccionario = {
			'actor':self.actor,
			'verbo': self.verbo,
			
		}

		return u'%(actor)s %(verbo)s' % diccionario

