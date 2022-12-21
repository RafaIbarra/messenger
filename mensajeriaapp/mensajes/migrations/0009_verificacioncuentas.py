# Generated by Django 4.1.3 on 2022-12-11 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0008_alter_usuarios_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificacionCuentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('correo', models.EmailField(max_length=254)),
                ('codigo_identificacion', models.BigIntegerField(default=0)),
                ('fecha_envio', models.DateTimeField(verbose_name='fecha envio')),
                ('autenticado', models.BooleanField(default=False)),
                ('fecha_autenticacion', models.DateTimeField(verbose_name='fecha autenticacion')),
            ],
            options={
                'db_table': 'VerificacionCuentas',
            },
        ),
    ]