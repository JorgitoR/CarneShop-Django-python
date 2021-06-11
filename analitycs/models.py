from django.db import models

from Dashboard.models import Usuario



class SessionUsuario(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	session_key = models.CharField(max_length=60, null=True, blank=True)
	ip_address= models.GenericIPAddressField(null=True, blank=True)
	ciudad_data = models.TextField(null=True, blank=True)
	ciudad = models.CharField(max_length=120, null=True, blank=True)
	pais = models.CharField(max_length=120, null=True, blank=True)
	activo = models.BooleanField(default=True)
	date = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		ciudad = self.ciudad 
		pais = self.pais
		if pais and ciudad:
			return f"{ciudad}, {pais}"
		elif ciudad and not pais:
			return f"{ciudad}"
		elif pais and not ciudad:
			return f"{pais}"
		return self.usuario.username
		