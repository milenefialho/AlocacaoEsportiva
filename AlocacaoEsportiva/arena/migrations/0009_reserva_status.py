# Generated by Django 5.0.4 on 2024-07-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0008_remove_cliente_arena'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
