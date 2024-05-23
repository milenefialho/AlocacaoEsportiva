# Generated by Django 5.0.4 on 2024-05-14 02:06

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arena',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.CharField(blank=True, default='S/N', max_length=10)),
                ('complemento', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=20)),
                ('cpf', models.CharField(max_length=20)),
                ('senha', models.CharField(max_length=50)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.CharField(max_length=50)),
                ('arena', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.arena')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arena', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.arena')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horaEntrada', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('horaSaida', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('valor', models.FloatField(default=0.0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Quadra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=20)),
                ('preco', models.FloatField(default=0.0)),
                ('reservado', models.BooleanField(default=False)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma', models.CharField(max_length=20)),
                ('valor', models.FloatField(default=0.0)),
                ('data', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.reserva')),
            ],
        ),
    ]
