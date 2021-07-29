from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Sandwich(models.Model):
    class Meta:
        db_table = "sandwich"

    tamaño = models.CharField(max_length=35, null=False, blank=False)
    precio = models.FloatField(null=False, blank=False)


class Ingrediente_adicional(models.Model):
    class Meta:
        db_table = 'ingrediente_adicional'

    NOMBRES = (('Individual', 'Individual'),
               ('Doble', 'Doble'), ('Triple', 'Triple'))
    nombre = models.CharField(
        max_length=35, choices=NOMBRES, null=False, blank=False
    )
    precio = models.FloatField(null=False, blank=False)


class Cliente(models.Model):
    class Meta:
        db_table = 'cliente'

    nombre = models.CharField(max_length=35, null=False, blank=False)
    apellido = models.CharField(max_length=35, null=False, blank=False)
    dni = models.CharField(max_length=35, null=False, blank=False)


class Pedido(models.Model):
    class Meta:
        db_table = 'pedido'

    fecha = models.DateField(null=False, auto_now_add=True)
    fk_cliente = models.ForeignKey(Cliente, related_name='pedidos', on_delete=models.CASCADE)


class Sandwich_ingrediente(models.Model):
    class Meta:
        db_table = 'sandwich_ingrediente'

    subtotal = models.FloatField(null=False, blank=False)
    fk_sandwich_id = models.IntegerField(null=False, blank=False)
    fk_ingrediente_id = models.IntegerField(null=False, blank=False)
    fk_pedido = models.ForeignKey(
        Pedido, null=False, blank=False, on_delete=models.CASCADE
    )
