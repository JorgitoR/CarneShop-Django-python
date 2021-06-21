from django.db import models

from .base.models import AbstractNotificacion


class notificacion(AbstractNotificacion):

	class Meta(AbstractNotificacion.Meta):
		abstract = False
		