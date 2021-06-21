from django.conf import settings


CONFIGURACION_POR_DEFECTO = {
	
	'USE_JSONFIELD':False,
	'SOFT_DELETE':False,
	'NUM_TO_FETCH'10,

}

def get_config():
	user_config = getattr(settings, 'CONFIGURACION_NOTIFICACIONES', {})

	config = CONFIGURACION_POR_DEFECTO.copy()
	config.update(user_config)

	return config