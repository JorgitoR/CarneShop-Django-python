from django.db import models

from Dashboard.models import Usuario

from .signals import usuario_logged_in
from .utils import get_address_ip, get_client_city_data



class SessionUsuarioManager(models.Manager):
	def crear_nuevo(self, usuario, session_key=None, ip_address=None, ciudad_data=None):
		nueva_session = self.model()
		nueva_session.usuario = usuario
		nueva_session.session_key = session_key
		if ip_address is not None:
			nueva_session.ip_address = ip_address
			if ciudad_data:
				nueva_session.ciudad_data = ciudad_data
				try:
					ciudad = ciudad_data['city']
				except:
					ciudad = None
				nueva_session.ciudad = ciudad
				try:
					pais = ciudad_data['country_name']
				except:
					pais = None
			nueva_session.pais = pais
			nueva_session.save()
			return nueva_session
		return None

class SessionUsuario(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	session_key = models.CharField(max_length=60, null=True, blank=True)
	ip_address= models.GenericIPAddressField(null=True, blank=True)
	ciudad_data = models.TextField(null=True, blank=True)
	ciudad = models.CharField(max_length=120, null=True, blank=True)
	pais = models.CharField(max_length=120, null=True, blank=True)
	activo = models.BooleanField(default=True)
	date = models.DateTimeField(auto_now_add=True)

	objects = SessionUsuarioManager()

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


def usuario_logged_is_receiver(sender, request, *args, **kwargs):
	usuario = sender
	ip_address = get_address_ip(request)
	ciudad_data = get_client_city_data(ip_address)
	request.session['CITY'] = str(ciudad_data.get('city'))
	session_key = request.session.session_key
	SessionUsuario.objects.crear_nuevo(

		usuario = usuario,
		session_key=session_key,
		ip_address=ip_address,
		ciudad_data=ciudad_data

	)

usuario_logged_in.connect(usuario_logged_is_receiver)