from django import template
from Dashboard.models import Orden

register = template.Library()

@register.filter()
def cart_item_count(usuario):
	if usuario.is_authenticated:
		qs = Orden.objects.filter(usuario=usuario, ordenado=False)
		if qs.exists():
			return qs[0].productos.count()

		return 0
