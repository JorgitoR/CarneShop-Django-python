from django.db import models


from Dashboard.models import Usuario
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notificacion(models.Model):
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
	content_object = GenericForeignKey("actor_content_type", "object_id_actor")


	verbo = models.CharField(max_length=255)
	descripcion = models.TextField(blank=True, null=True)


