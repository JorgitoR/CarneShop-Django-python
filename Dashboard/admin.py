from django.contrib import admin

from .models import Usuario, categoria, OrdenarProducto, Orden, pedidos, Cupon, producto, direccion


class ContentTypeInline(admin.TabularInline):
	model = OrdenarProducto
	extra = 0


class productoAdmin(admin.ModelAdmin):

	inlines = [ContentTypeInline]

admin.site.register(direccion)
admin.site.register(Cupon)
admin.site.register(pedidos)
admin.site.register(OrdenarProducto)
admin.site.register(Orden)
admin.site.register(producto)
admin.site.register(categoria)
admin.site.register(Usuario)