# Generated by Django 4.1.3 on 2022-12-09 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0005_alter_usuarios_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='image',
            field=models.ImageField(blank=True, default='sinperfil.png', upload_to=''),
        ),
    ]
