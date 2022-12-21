# Generated by Django 4.1.3 on 2022-11-27 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remitente', models.CharField(max_length=200)),
                ('destinatario', models.CharField(max_length=200)),
                ('fecha_registro', models.DateTimeField(verbose_name='fecha registro')),
            ],
            options={
                'db_table': 'Conversaciones',
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=200)),
                ('apellido_usuario', models.CharField(max_length=200)),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha Nacimiento')),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('correo', models.EmailField(max_length=254)),
                ('activo', models.BooleanField(default=False)),
                ('ultima_conexion', models.DateTimeField(verbose_name='fecha ultma conexion')),
                ('fecha_registro', models.DateTimeField(verbose_name='fecha registro')),
            ],
            options={
                'db_table': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Participantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(verbose_name='fecha registro')),
                ('id_conversacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mensajes.conversaciones')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mensajes.usuarios')),
            ],
            options={
                'db_table': 'Participantes',
            },
        ),
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.CharField(max_length=200)),
                ('leido', models.BooleanField(default=False)),
                ('fecha_registro', models.DateTimeField(verbose_name='fecha registro')),
                ('id_conversacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mensajes.conversaciones')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mensajes.usuarios')),
            ],
            options={
                'db_table': 'Chats',
            },
        ),
    ]