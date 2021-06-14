# Generated by Django 3.2.4 on 2021-06-14 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0006_alter_cupon_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='kind_address',
            field=models.CharField(choices=[('CARRERA', 'Carr'), ('CALLE', 'Calle'), ('AVENIDA', 'Avenida')], max_length=20, verbose_name='Tipo de Direccion'),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='direccion', to=settings.AUTH_USER_MODEL),
        ),
    ]
