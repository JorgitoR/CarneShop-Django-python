from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .forms import RegistroForm
from .models import (Usuario, 
					producto, 
					OrdenarProducto, 
					Orden, 
					pedidos,
					direccion)

from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import View


def home(request):

	product = producto.objects.all()
	

	context ={
		'product':product,
	}

	return render(request, 'dashboard/home.html', context)


def add_carrito(request, slug):
	item = get_object_or_404(producto, slug=slug)
	ordenar_producto, created = OrdenarProducto.objects.get_or_create(

		content_type = item.get_content_type,
		object_id = item.id,
		usuario = request.user,
		ordenado = True

	)

	order_qs = Orden.objects.filter(usuario=request.user, ordenado=False)

	if order_qs.exists():
		orden_realizada = order_qs[0]


		cantidad_ordenada = OrdenarProducto.objects.filter(pedido__slug=item.slug, ordenado=True).aggregate(cantidad_suma=Sum('cantidad'))
		
		cantidad = cantidad_ordenada['cantidad_suma']
		print(cantidad)
		min_cantidad = 1

		if cantidad >= min_cantidad:
			
			total = item.stock - cantidad	
			print('TOTAL', total)

			if ordenar_producto.cantidad < total:
				if orden_realizada.productos.filter(pedido__slug=item.slug).exists():
					ordenar_producto.cantidad += 1
					ordenar_producto.save()
					messages.info(request, "La cantidad fue actualizada")
					return redirect('check_out')
				else:
					pedido = pedidos.objects.create(
						pedidos = ordenar_producto,
						orden = orden_realizada
					)
					messages.info(request, "Este articulo fue agregado al carrito de compras")
					return redirect('check_out')
			else:
				messages.info(request, "Maxima Cantidad disponible %s" % total)
				return redirect('check_out')

	else:
		date = timezone.now()
		orden = Orden.objects.create(
				usuario = request.user,
				date = date
		)

		pedido = pedidos.objects.create(
			pedidos = ordenar_producto,
			orden=orden
		)

		messages.info(request, "Este articulo fue agregado a su carrito.")
		return redirect("check_out")

def minus_cart(request, slug):
	item = get_object_or_404(producto, slug=slug)

	qs = Orden.objects.filter(usuario=request.user, ordenado=False)

	if qs.exists():
		orden = qs[0]
		print(orden)

		if orden.productos.filter(pedido__slug=item.slug).exists():

			item_orden = OrdenarProducto.objects.filter(

				pedido =item,
				usuario=request.user,
				ordenado=True
			)[0]

			if item_orden.cantidad > 0:
				item_orden.cantidad -= 1
				item_orden.save()
			else:
				orden.productos.remove(item_orden)

			messages.info(request, "La cantidad de este producto fue actualizada")
			return redirect("check_out")
		
		else:
			messages.info(request, "No existe este producto en el carro de compras")
			return redirect("check_out")
	else:
		messages.info(request, "No tienes una orden Activa")
		return redirect("check_out")


class CheckView(View):
	def get(self, *args, **kwargs):
		try:
			orden = Orden.objects.get(usuario=self.request.user, ordenado=False)
			address = direccion.objects.filter(usuario=self.request.user).first()

			context = {
				'orden':orden,
				'direccion':address
			}

			return render(self.request, "dashboard/checkout.html", context) 

		except ObjectDoesNotExist:
			messages.info(self.request, "No tienes una orden Activa")
			return redirect("check_out")
