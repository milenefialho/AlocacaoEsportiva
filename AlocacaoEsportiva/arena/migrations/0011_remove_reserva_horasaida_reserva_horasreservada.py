# Generated by Django 5.0.4 on 2024-07-14 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0010_alter_pagamento_reserva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='horaSaida',
        ),
        migrations.AddField(
            model_name='reserva',
            name='horasReservada',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
