from django.dispatch import Signal

usuario_logged_in = Signal(providing_args=['request'])