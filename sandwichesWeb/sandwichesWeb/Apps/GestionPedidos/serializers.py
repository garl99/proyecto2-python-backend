from sandwichesWeb.Apps.GestionPedidos.models import *
from rest_framework import serializers

class ClienteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    lastname = serializers.CharField(max_length=120)
    dni = serializers.IntegerField()

class OrderDetailSerializer(serializers.Serializer):
    size = serializers.IntegerField()
    ingredients = serializers.ListField(child=serializers.IntegerField())
    subtotal = serializers.FloatField()

class SandwichIngredienteSerializer(serializers.Serializer):
    customer = ClienteSerializer()
    orderDetail = OrderDetailSerializer(many=True)
    total = serializers.FloatField()
    date = serializers.DateField()
