# Generated by Django 4.2.5 on 2023-09-27 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coordenacao', '0003_periodo_oferta'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Oferta',
        ),
    ]