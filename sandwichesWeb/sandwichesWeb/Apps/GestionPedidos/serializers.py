from sandwichesWeb.Apps.GestionPedidos.models import *
from rest_framework import serializers


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'dni']
