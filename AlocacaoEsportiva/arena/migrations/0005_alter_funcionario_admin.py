# Generated by Django 5.0.4 on 2024-05-14 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0004_pessoa_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]