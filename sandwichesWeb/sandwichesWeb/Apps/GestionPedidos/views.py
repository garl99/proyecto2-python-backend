from sandwichesWeb.Apps.GestionPedidos.models import Ingrediente_adicional, Sandwich
from sandwichesWeb.Apps.GestionPedidos.models import Pedido, Cliente, Sandwich_ingrediente
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReporteSerializer
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
                dni=cliente['dni'],
                defaults={
                    "nombre": cliente['name'],
                    "apellido": cliente['lastname']
                })

            for d in detail:
                pedido = Pedido.objects.create(fk_cliente=obj, fecha=date)
                for i in d['ingredients']:
                    Sandwich_ingrediente.objects.create(
                        fk_sandwich_id=d['size'],
                        fk_ingrediente_id=i,
                        fk_pedido=pedido,
                        subtotal=d['subtotal'])

            return Response(
                {
                    "status": "Success",
                    "code": 200,
                    "message": "Pedido creado"
                }, )

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    
    ##Reparar Los ingredientes
    def get_queryset(self):
        result = []
        cliente = Cliente.objects.all()
        for c in cliente:    
            pedido = Pedido.objects.filter(fk_cliente=c.id)
            for p in pedido:
                ingre = []
                bandera = True
                SandIngre= Sandwich_ingrediente.objects.filter(fk_pedido=p.id)
                
                for s in SandIngre:
                    TaSandwich= Sandwich.objects.filter(id=s.fk_sandwich_id).first()
                    ingrediente = Ingrediente_adicional.objects.filter(id=s.fk_ingrediente_id)

                    for i in ingrediente:
                        ingre.append(i.nombre)
                    ##ACOMODAR LOS INGREDIENTES ENVIA UN ARRAY Y DEBE SER UN STRING
                   
                    if bandera==True:
                      
                        result.append({
                            'id': p.id,
                            'customer': c.nombre,
                            'size': TaSandwich.tamaño, 
                            'ingredients':ingre,
                            'total': s.subtotal, 
                            'date': p.fecha 
                                        })  
                        bandera=False    

                                                
            
        return result

    def getdia(self):
        result = []     
        cliente = Cliente.objects.all()
        for c in cliente:    
            pedido = Pedido.objects.filter(fk_cliente=c.id).order_by('fecha')
            for p in pedido:
                ingre = []
                bandera = True
                SandIngre= Sandwich_ingrediente.objects.filter(fk_pedido=p.id)
                
                for s in SandIngre:
                    TaSandwich= Sandwich.objects.filter(id=s.fk_sandwich_id).first()
                    ingrediente = Ingrediente_adicional.objects.filter(id=s.fk_ingrediente_id)

                    for i in ingrediente:
                        ingre.append(i.nombre)
                    ##ACOMODAR LOS INGREDIENTES ENVIA UN ARRAY Y DEBE SER UN STRING
                   
                    if bandera==True:
                      
                        result.append({
                            'id': p.id,
                            'customer': c.nombre,
                            'size': TaSandwich.tamaño, 
                            'ingredients':ingre,
                            'total': s.subtotal, 
                            'date': p.fecha 
                                        })  
                        bandera=False    

                                                
            
        return result
    

    def getsize(self):
        result = [] 
        TaSandwich= Sandwich.objects.all()

        for ta in TaSandwich:
                            
            cliente = Cliente.objects.all()
            for c in cliente:    
                pedido = Pedido.objects.filter(fk_cliente=c.id)
                for p in pedido:
                    ingre = []
                    bandera = True
                    SandIngre= Sandwich_ingrediente.objects.filter(fk_pedido=p.id,fk_sandwich_id=ta.id)
                    
                    for s in SandIngre:
                        
                        ingrediente = Ingrediente_adicional.objects.filter(id=s.fk_ingrediente_id)

                        for i in ingrediente:
                            ingre.append(i.nombre)
                        ##ACOMODAR LOS INGREDIENTES ENVIA UN ARRAY Y DEBE SER UN STRING
                    
                        if bandera==True:
                        
                            result.append({
                                'id': p.id,
                                'customer': c.nombre,
                                'size': ta.tamaño, 
                                'ingredients':ingre,
                                'total': s.subtotal, 
                                'date': p.fecha 
                                            })  
                            bandera=False    
            
        return result

    

    def get(self, request, *args, **kwargs):
        Reporte=[]
        general = self.get_queryset()
        dia = self.getdia()
        size= self.getsize()

        serializer = ReporteSerializer(general, many=True)
        serilizerDia = ReporteSerializer(dia, many=True)
        serilizersize= ReporteSerializer(size, many=True)
        
        
        Reporte.append({
                            "General" : serializer.data,
                            "Dia": serilizerDia.data,
                            "Size": serilizerDia.data
                        })   

        return Response(Reporte)
       