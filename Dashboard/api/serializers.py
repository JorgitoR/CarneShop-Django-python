from rest_framework import serializers
from Dashboard.models import Usuario

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

import logging
logger = logging.getLogger(__name__)

from meetShop.db.email import send_mail_async as send_mail
from django.conf import settings

class RegistroSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, validators = [UniqueValidator(queryset=Usuario.objects.all())])

	password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = Usuario
		fields = [

			"username",
			"password1",
			"password2",
			"email",
			"first_name",
			"last_name"

		]

		extra_kwargs = {
			'first_name':{"required":True},
			'last_name':{"required":True},
		}

	def validate(self, attrs):
		if attrs['password1'] != attrs['password2']:
			raise serializers.ValidationError({'password':'Las contraseña no concuerdan'})

		return attrs

	def create(self, validated_data):
		usuario = Usuario.objects.create(
			username = validated_data['username'],
			email =  validated_data['email'],
			first_name = validated_data['first_name'],
			last_name = validated_data['last_name'],
			cliente =True
		)

		usuario.set_password(validated_data['password1'])
		usuario.save()


		if usuario:
			self.enviarEmail(usuario)

		return usuario

	def enviarEmail(self, obj):
		email = []
		if obj.email:
			print(obj.email)
			email.append(obj.email)

		if len(email):
			logger.info("[Usuario %s] Enviando credenciales al correo %s", obj.username, obj.email)

			values = {
				'nombre':obj.first_name,
				'apellido':obj.last_name,
				'titulo': 'Credenciales del Registri a CarneShop',
				'username': obj.username,
				'sign':settings.SITIO_HEADER

			}	

		email_template = settings.CREDENCIALES_USUARIO

		try:
			send_mail(

				'[{app}][{usuario}] Credenciales de registro'.format(app=settings.APP_NAME, usuario=obj.username),
				email_template.format(**values),
				settings.APP_EMAIL,
				email
			)

		except Exception as e:
			logger.warning("Error", str(e))