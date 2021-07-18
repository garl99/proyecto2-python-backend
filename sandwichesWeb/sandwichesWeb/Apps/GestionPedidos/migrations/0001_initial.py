# Generated by Django 3.2.5 on 2021-07-18 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=35)),
                ('apellido', models.CharField(max_length=35)),
                ('dni', models.CharField(max_length=35)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Ingrediente_adicional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Individual', 'Individual'), ('Doble', 'Doble'), ('Triple', 'Triple')], max_length=35)),
                ('precio', models.FloatField()),
            ],
            options={
                'db_table': 'ingrediente_adicional',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fk_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionPedidos.cliente')),
            ],
            options={
                'db_table': 'pedido',
            },
        ),
        migrations.CreateModel(
            name='Sandwich',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamaño', models.CharField(max_length=35)),
                ('precio', models.FloatField()),
            ],
            options={
                'db_table': 'sandwich',
            },
        ),
        migrations.CreateModel(
            name='Sandwich_ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.FloatField()),
                ('fk_ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionPedidos.ingrediente_adicional')),
                ('fk_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionPedidos.pedido')),
                ('fk_sandwich', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionPedidos.sandwich')),
            ],
            options={
                'db_table': 'sandwich_ingrediente',
            },
        ),
    ]
