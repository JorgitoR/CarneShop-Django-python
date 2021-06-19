from django.contrib import admin

from .models import (
					Usuario, 
					categoria, 
					OrdenarProducto, 
					Orden, 
					pedidos, 
					Cupon, 
					producto, 
					direccion,
					ProductoRelacionado)


class ContentTypeInline(admin.TabularInline):
	model = OrdenarProducto
	extra = 0

class ProductoRelacionadoInline(admin.TabularInline):
	model = ProductoRelacionado
	fk_name = 'item'
	extra = 0

class productoAdmin(admin.ModelAdmin):

	inlines = [ProductoRelacionadoInline]
	class Meta:
		model = producto



admin.site.register(direccion)
admin.site.register(Cupon)
admin.site.register(pedidos)
admin.site.register(OrdenarProducto)
admin.site.register(Orden)
admin.site.register(producto, productoAdmin)
admin.site.register(categoria)
admin.site.register(Usuario)