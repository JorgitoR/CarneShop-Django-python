from django.db import models

from django.contrib.auth.models import Group
from Dashboard.models import Usuario
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils import timezone
from jsonfield.fields import JSONField
#pip install jsonfield

from notificacion.signals import notificar

from swapper import load_model

from django.db.models.query import QuerySet

from notificacion import settings as ajustes_notificacion

DATOS_EXTRAS = ajustes_notificacion.get_config()['USE_JSONFIELD']

def is_soft_delete():
	return notificacion.settings.get_config()['SOFT_DELETE']


def assert_soft_delete():
	if not is_soft_delete():

		#msg = Para usar el campo "deleted" configurar SOFT_DELETE=True en ajustes
		#delo contrario NotificacionQuerySet.no_leidon y NotificacionQueryset.leido no
		#filtraran por el campo "deleted"

		msg = 'REVERTME'
		raise ImproperlyConfigured(msg)

class NotificacionQuerySet(models.QuerySet):
	def no_enviado(self):
		return self.filter(emailed=False)

	def enviado(self):
		return self.filter(emailed=True)

	def no_leido(self, include_deleted=False):
		"""Retornamos solos los item que no han sido leidos en el actual Queryset"""

		if is_soft_delete() and not include_deleted:
			return self.filter(no_leido=True, eliminado=False)

		#cuando SOFT_DELETE=False, se supone que los desarrolladores No deben tocar el
		#campo eliminado
		return self.filter(no_leido=True)


	def leido(self, include_deleted=False):

		if is_soft_delete() and not include_deleted:
			return self.filter(no_leido=False, eliminado=False)

		return self.filter(no_leido=False)


	def marcar_todo_as_leido(self, destinario=None):
		"""
			Marcar todos los mensages como leidos en el actual Queryset
	
		"""
		#Filtramos los mensajes que no han sido leidos
		#Para luego marcarlos como leidos
		qs = self.no_leido(True)
		if destinario:
			qs = qs.filter(destinario=destinario)

		return qs.update(no_leido=False)


	def marcar_todos_como_no_leidos(self, destinario=None):
		"""
			Marcar todo los mensages como no leidos en actual queryset
		"""
		#filtramos todo los mensajes 
		qs = self.no_leido(True)
		
		if destinario:
			qs = qs.filter(destinario=destinario)

		return qs.update(no_leido=True)

	def eliminar(self):
		"""Retornamos solo los items eliminado en actual queryset"""
		assert_soft_delete()
		return self.filter(eliminado=True)


	def activo(self):
		"""
			Retornamos solo activo(no-eliminado) item en el actual Queryset
		"""
		assert_soft_delete()
		return self.filter(eliminado=False)

	def marcar_todo_como_eliminado(self, destinario=None):

		assert_soft_delete()
		qs = self.activo()
		if destinario:
			qs = qs.filter(destinario=destinario)
		return qs.update(eliminado=True)


	def marcar_todo_como_activo(self, destinario=None):
		assert_soft_delete()
		qs = self.eliminar()
		if destinario:
			qs = qs.filter(destinario=destinario)
		return qs.update(eliminado=False)


	def marcar_todo_como_no_enviado(self, destinario=None):
		qs = self.enviado()
		if destinario:
			qs=qs.filter(destinario=destinario)

		return qs.update(emailed=False)

	def marcar_todo_como_enviado(self, destinario=None):
		qs = self.no_enviado()
		if destinario:
			qs = qs.filter(destinario=destinario)
		return qs.update(emailed=True)


class AbstractNotificacionManager(models.Manager):
	def get_queryset(self):
		return self.NotificacionQuerySet(self.model,  using=self._db)


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

	objects = NotificacionQuerySet.as_manager()

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



def notificar_handler(verbo, **kwargs):
	"""
		Funcion de controlador para crear una instancia de
		notificacion tras una llamada de signal de accion
	"""

	destinario = kwargs.pop('destinario')
	actor = kwargs.pop('sender')
	#obj = [(kwargs.pop(opt, None)) for opt in ('objetivo', 'action_object')]

	publico = bool(kwargs.pop('publico', True))
	descripcion = kwargs.pop('descripcion', None)
	timestamp = kwargs.pop('timestamp', timezone.now())

	Notificacion = load_model('notificacion', 'notificacion')
	nivel = kwargs.pop('nivel', Notificacion.NIVELES.info)


	#Compruebe si es usuario o grupo

	if isinstance(destinario, Group):
		destinarios = destinario.user_set.all()
	elif isinstance(destinario, (QuerySet, list)):
		destinarios = destinario
	else:
		destinarios = [destinario]

	print(destinarios)


	nueva_notificacion = []
	for destinario in destinarios:
		newnotify = Notificacion(
				destinario = destinario,
				actor_content_type=ContentType.objects.get_for_model(actor),
				object_id_actor = actor.pk,
				verbo =str(verbo),
				publico=publico,
				descripcion = descripcion,
				timestamp=timestamp,
				nivel=nivel
		)


		newnotify.save()
		nueva_notificacion.append(newnotify)

	return nueva_notificacion


notificar.connect(notificar_handler, dispatch_uid='notificacion.models.notificacion')