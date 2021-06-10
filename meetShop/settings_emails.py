import os


EMAIL_TIMEOUT = 3      # seconds
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'true') == 'true'
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'compreki605@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'jorgeluizuribe')


ENVIAR_EMAIL_PROYECTO_A_OPERADOR = os.getenv('TASKS_SEND_EMAILS_TO_ASSIGNED', 'false') == 'true'


TAREA_VIEWER_ENABLED = os.getenv('TASKS_VIEWER_ENABLED', 'false') == 'true'
TAREA_VIEWER_HASH_SALT = os.getenv('TASKS_VIEWER_HASH_SALT', '1two3')   # REENPLAZAMOS EN PRODUCION  !!!
TAREA_VIEWER_ENDPOINT = os.getenv('TASKS_VIEWER_ENDPOINT', 'http://localhost:8888/{number}?t={token}')

MTASKS_EMAIL_WITHOUT_URL = '''\
Nueva tarea creada #{id}.

Titulo:
{titulo}

Usuario Asignado:
{usuario}

Descripcion:
{descripcion}

Tenga en cuenta: No responder este Email. Este correo electrónico se envía desde un buzón desatendido.
No se leerán las respuestas.

---
{sign}
'''


MTASKS_EMAIL_WITH_URL = '''\
New task #{id} created.

Title:
{titulo}

Assigned:
{usuario}

Description:
{descripcion}

Order URL:
{url}

Please note: Do NOT reply to this email. This email is sent from an unattended mailbox.
Replies will not be read.

---
{sign}
'''




CREDENCIALES_USUARIO = '''\

{titulo}: {nombre} {apellido}

Usuario:
{username}


Tenga en cuenta: No responder este Email. Este correo electrónico se envía desde un buzón desatendido.
No se leerán las respuestas.

---
{sign}
'''
