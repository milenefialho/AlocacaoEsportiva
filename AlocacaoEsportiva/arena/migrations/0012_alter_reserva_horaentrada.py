# Generated by Django 5.0.4 on 2024-07-17 19:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0011_remove_reserva_horasaida_reserva_horasreservada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='horaEntrada',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
