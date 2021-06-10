from django.contrib import admin

from .models import Usuario, categoria, OrdenarProducto, OrdenarPedido, pedidos, Cupon, producto


class ContentTypeInline(admin.TabularInline):
	model = OrdenarProducto
	extra = 0


class productoAdmin(admin.ModelAdmin):

	inlines = [ContentTypeInline]

admin.site.register(producto)
admin.site.register(categoria)
admin.site.register(Usuario)