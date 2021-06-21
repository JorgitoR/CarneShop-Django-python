from django.dispatch import Signal

notificar = Signal(providing_args=[
								'destinario', 
								'actor', 
								'verbo', 
								'descripcion',
								'timestamp',
								'nivel'])