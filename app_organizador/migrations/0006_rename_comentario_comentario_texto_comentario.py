# Generated by Django 4.2.9 on 2024-01-16 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_organizador', '0005_comentario_libro_comentarios'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentario',
            old_name='comentario',
            new_name='texto_comentario',
        ),
    ]