# Generated by Django 3.2.4 on 2021-06-10 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0003_producto_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrdenarPedido',
            new_name='Orden',
        ),
    ]