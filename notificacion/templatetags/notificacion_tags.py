from django import template


register = template.Library()

@register.filter()
def notificacion_sin_leer(context):
	user = user_context(context)
	print(user)
	if not user:
		return ''
	return user.notificaciones.no_leido().count()

notificacion_sin_leer = register.simple_tag(takes_context=True)(notificacion_sin_leer)

def user_context(context):
	if 'user' not in context:
		return None 

	request = context['request']
	user = request.user 

	try:
		user_is_anonymous = user.is_anonymous()
	except TypeError: #para nuevas versiones de django
		user_is_anonymous = user.is_anonymous

	if user_is_anonymous:
		return None 
	return user 