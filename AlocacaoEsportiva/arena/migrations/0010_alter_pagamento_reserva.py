# Generated by Django 5.0.4 on 2024-07-02 00:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0009_reserva_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='reserva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamento', to='arena.reserva'),
        ),
    ]
