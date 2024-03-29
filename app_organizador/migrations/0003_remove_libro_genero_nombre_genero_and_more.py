# Generated by Django 4.2.9 on 2024-01-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organizador', '0002_rename_generos_autor_rename_autores_genero_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro_genero',
            name='nombre_genero',
        ),
        migrations.RemoveField(
            model_name='libro_genero',
            name='nombre_libro',
        ),
        migrations.AddField(
            model_name='libro',
            name='autores',
            field=models.ManyToManyField(to='app_organizador.autor'),
        ),
        migrations.AddField(
            model_name='libro',
            name='generos',
            field=models.ManyToManyField(to='app_organizador.genero'),
        ),
        migrations.DeleteModel(
            name='Libro_Autor',
        ),
        migrations.DeleteModel(
            name='Libro_Genero',
        ),
    ]
