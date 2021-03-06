# Generated by Django 3.2.4 on 2021-06-21 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(choices=[('Exito', 'exito'), ('Informacion', 'informacion'), ('Advertencia', 'advertencia'), ('Error', 'error')], default='Informacion', max_length=20)),
                ('no_leido', models.BooleanField(db_index=True, default=True)),
                ('object_id_actor', models.PositiveIntegerField()),
                ('verbo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('publico', models.BooleanField(db_index=True, default=True)),
                ('eliminado', models.BooleanField(db_index=True, default=False)),
                ('emailed', models.BooleanField(db_index=True, default=False)),
                ('data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('actor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificar_actor', to='contenttypes.contenttype')),
                ('destinario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificar_destino', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-timestamp',),
                'abstract': False,
                'index_together': {('destinario', 'no_leido')},
            },
        ),
    ]
