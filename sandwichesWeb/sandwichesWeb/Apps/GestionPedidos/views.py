from sandwichesWeb.Apps.GestionPedidos.models import Pedido, Cliente, Sandwich_ingrediente
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sandwichesWeb.Apps.GestionPedidos import serializers

class PedidoApiView(APIView):

    serializer_class = serializers.SandwichIngredienteSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            cliente = serializer.validated_data.get('customer')
            detail = serializer.validated_data.get('orderDetail')
            date = serializer.validated_data.get('date')

            obj, created = Cliente.objects.get_or_create(
                dni = cliente['dni'],
                defaults = {"nombre":cliente['name'], "apellido":cliente['lastname']}
            )

            for d in detail:
                pedido = Pedido.objects.create(
                    fk_cliente = obj,
                    fecha = date
                )
                for i in d['ingredients']:
                    Sandwich_ingrediente.objects.create(
                        fk_sandwich_id = d['size'],
                        fk_ingrediente_id = i,
                        fk_pedido = pedido,
                        subtotal = d['subtotal']
                    )

            return Response(
                {"status": "Success", "code": 200, "message": "Pedido creado"},
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
