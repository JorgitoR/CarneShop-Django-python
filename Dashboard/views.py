from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils import timezone
from .forms import RegistroForm, CuponForm
from .models import (Usuario, 
					producto, 
					OrdenarProducto, 
					Orden, 
					pedidos,
					Cupon,
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

class DeatilProducto(DetailView):
	model = producto
	template_name= 'dashboard/detail.html'
	


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
		print('pedida', cantidad)
		min_cantidad = 1

		if cantidad >= min_cantidad:
			
			disponible = item.stock - cantidad	
			print('Disponible', disponible)
			

			if  ordenar_producto.cantidad == disponible or ordenar_producto.cantidad < disponible:
				if orden_realizada.productos.filter(pedido__slug=item.slug).exists():
					ordenar_producto.cantidad += 1
					ordenar_producto.save()
					messages.info(request, "La cantidad del producto %s fue actualizada" %(ordenar_producto.content_object.titulo))
					return redirect('check_out')
				else:
					pedido = pedidos.objects.create(
						pedidos = ordenar_producto,
						orden = orden_realizada
					)
					messages.info(request, "Este articulo fue agregado al carrito de compras")
					return redirect('check_out')
			else:
				messages.info(request, "Maxima Cantidad disponible %s" % disponible)
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
				if item_orden.cantidad == 0:
					item_orden.delete()
				else:

					item_orden.save()
			#else:
				#orden.productos.remove(item_orden)
				#item_orden.delete()

			messages.info(request, "La cantidad de este producto fue actualizada")
			return redirect("check_out")
		
		else:
			messages.info(request, "No existe este producto en el carro de compras")
			return redirect("check_out")
	else:
		messages.info(request, "No tienes una orden Activa")
		return redirect("check_out")


def eliminar_del_cart(request, slug):
	item = get_object_or_404(producto, slug=slug)
	orden_qs = Orden.objects.filter(

		usuario=request.user,
		ordenado=False
	)

	if orden_qs.exists():
		orden = orden_qs[0]
		print(orden)

		if orden.productos.filter(pedido__slug=item.slug).exists():

			articulo = OrdenarProducto.objects.filter(
					pedido=item,
					usuario=request.user,
					ordenado=True
			)[0]

			pedido = pedidos.objects.filter(
				pedidos = articulo,
				orden = orden_qs
			)

			articulo.delete()

			messages.info(request, "El producto fue eliminado del carro de compras")
			return redirect("check_out")
		
		else:
			messages.info(request, "Este producto no esta en el carro de compras")
			return redirect("check_out")
	else:
		messages.info(request, "No tienes una orden activa")
		return redirect("check_out")

class CheckView(View):
	def get(self, *args, **kwargs):
		try:
			orden = Orden.objects.get(usuario=self.request.user, ordenado=False)
			address = direccion.objects.filter(usuario=self.request.user).first()

			context = {
				'orden':orden,
				'cuponForm':CuponForm(),
				'direccion':address,
				'DISPLAY_CUPON_FORM':True
			}

			return render(self.request, "dashboard/checkout.html", context) 

		except ObjectDoesNotExist:
			messages.warning(self.request, "No tienes una orden Activa")
			return redirect("/")


def obtener_cupon(request, code):
	try:
		cupon = Cupon.objects.get(codigo=code)
		return cupon
	except ObjectDoesNotExist:
		messages.info(request, "Este cupon no existe")
		return redirect('check_out')

class AddCuponView(View):
	def post(self, *args, **kwargs):
		form = CuponForm(self.request.POST or None)
		if form.is_valid():
			try:
				codigo = form.cleaned_data.get('codigo')
				orden = Orden.objects.get(usuario=self.request.user, ordenado=False)
				orden.cupon = obtener_cupon(self.request, codigo)
				orden.save()
				messages.success(self.request, "El cupon se guardo exitosamente")
				return redirect('check_out')
			except ObjectDoesNotExist:
				messages.info(self.request, "No tienes una orden activa")
				return redirect('check_out')