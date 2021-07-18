from rest_framework.response import Response
from sandwichesWeb.Apps.GestionPedidos.models import *
from rest_framework import viewsets
from sandwichesWeb.Apps.GestionPedidos.serializers import ClienteSerializer
from sandwichesWeb.Apps.GestionPedidos.responser import getResp

# Create your views here.


class ClienteViewSet(viewsets.ModelViewSet):

    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(getResp(serializer.data))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(getResp(serializer.data))
