# Generated by Django 4.1.3 on 2022-12-11 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0010_alter_verificacioncuentas_fecha_autenticacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificacioncuentas',
            name='fecha_autenticacion',
            field=models.DateTimeField(blank=True, null=True, verbose_name='fecha autenticacion'),
        ),
    ]
