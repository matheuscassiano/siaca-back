# Generated by Django 4.2.3 on 2023-10-17 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordenacao', '0004_delete_oferta'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='horas_optat',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
