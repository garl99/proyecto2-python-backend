from sandwichesWeb.Apps.GestionPedidos.models import Ingrediente_adicional, Sandwich
from sandwichesWeb.Apps.GestionPedidos.models import Pedido, Cliente, Sandwich_ingrediente
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReporteIngredienteSerializer, ReporteSerializer
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


    def listToString(ingredientesList):
        ingredientesString = ""
        
        for ingrediente in ingredientesList:
            ingredientesString += ingrediente
            ingredientesString += ","
        
        ingredientesString = ingredientesString[:-1:]        
        return ingredientesString
    
    def getGeneral(self):
        result = []
        cliente = Cliente.objects.all()
        for c in cliente:    
            pedido = Pedido.objects.filter(fk_cliente=c.id)
            for p in pedido:
                ingre = []
                bandera = True
                SandIngre = Sandwich_ingrediente.objects.filter(fk_pedido=p.id)
                
                for s in SandIngre:
                    TaSandwich = Sandwich.objects.filter(id=s.fk_sandwich_id).first()
                    ingrediente = Ingrediente_adicional.objects.filter(id=s.fk_ingrediente_id)

                    for i in ingrediente:
                        ingre.append(i.nombre)                      
                    
                    if bandera==True:                        
                        result.append({
                            'id': p.id,
                            'customer': c.nombre + " " + c.apellido,
                            'size': TaSandwich.tamaño, 
                            'ingredients': ingre,
                            'total': s.subtotal, 
                            'date': p.fecha 
                        })  
                        bandera=False  
        
        resultFixed = []
        for item in result:
            item['ingredients'] = PedidoApiView.listToString(item['ingredients'])
            resultFixed.append(item)   
                     
        return resultFixed

    def getByDay(self):
        result = []     
        cliente = Cliente.objects.all()
        for c in cliente:    
            pedido = Pedido.objects.filter(fk_cliente=c.id).order_by('fecha')
            for p in pedido:
                ingre = []
                bandera = True
                SandIngre = Sandwich_ingrediente.objects.filter(fk_pedido=p.id)
                
                for s in SandIngre:
                    TaSandwich = Sandwich.objects.filter(id=s.fk_sandwich_id).first()
                    ingrediente = Ingrediente_adicional.objects.filter(id=s.fk_ingrediente_id)

                    for i in ingrediente:
                        ingre.append(i.nombre)
                   
                    if bandera==True:                      
                        result.append({
                            'id': p.id,
                            'customer': c.nombre + " " + c.apellido,
                            'size': TaSandwich.tamaño, 
                            'ingredients':ingre,
                            'total': s.subtotal, 
                            'date': p.fecha 
                        })  
                        bandera=False    
        
        resultFixed = []
        for item in result:
            item['ingredients'] = PedidoApiView.listToString(item['ingredients'])
            resultFixed.append(item)   
                     
        return resultFixed
    
    def getBySize(self):
        result = [] 
        TaSandwich = Sandwich.objects.all()

        for ta in TaSandwich:                            
            cliente = Cliente.objects.all()
            
            for c in cliente:    
                pedido = Pedido.objects.filter(fk_cliente=c.id)
                
                for p in pedido:
                    ingre = []
                    bandera = True
                    SandIngre = Sandwich_ingrediente.objects.filter(fk_pedido=p.id,fk_sandwich_id=ta.id)
                    
                    for s in SandIngre:                        
                        ingrediente = Ingrediente_adicional.objects.filter(id=s.fk_ingrediente_id)

                        for i in ingrediente:
                            ingre.append(i.nombre)
                    
                        if bandera==True:                        
                            result.append({
                                'id': p.id,
                                'customer': c.nombre + " " + c.apellido,
                                'size': ta.tamaño, 
                                'ingredients':ingre,
                                'total': s.subtotal, 
                                'date': p.fecha 
                            })  
                            bandera=False    
        resultFixed = []
        for item in result:
            item['ingredients'] = PedidoApiView.listToString(item['ingredients'])
            resultFixed.append(item)   
                     
        return resultFixed
    
    def getByIngredients(self):        
        
        # Obtenemos los pedidos
        pedidos = self.getGeneral()   
        
        # Obtenemos los ingredientes adicionales
        ingredientesAdicionales = Ingrediente_adicional.objects.all() 
        
        # Creamos un objeto con los ingredientes como claves
        ingredientesAgrupados = {}
        for item in ingredientesAdicionales:                        
            ingredientesAgrupados[item.nombre] = []  
       
        # Agrupamos los resultados por los ingredientes
        for item in pedidos:
            for item2 in ingredientesAdicionales:
                if item2.nombre in item['ingredients']:   
                    ingredientesAgrupados[item2.nombre].append(item)
                    
        # Devolvemos la lista de elementos agrupados
        pedidosAgrupados = []
        pedidosAgrupados.append(ingredientesAgrupados)
        
        return pedidosAgrupados
    
    def getByClients(self):
        result = []
        # Obtenemos los clientes de mayor a menor (Orden descendente)
        clientes = Cliente.objects.all().order_by('-nombre','-apellido')
        
        for cliente in clientes:    
            pedidos = Pedido.objects.filter(fk_cliente = cliente.id)
            
            for pedido in pedidos:
                ingredientes = []
                bandera = True
                sandwichIngredientes = Sandwich_ingrediente.objects.filter(fk_pedido = pedido.id)
                
                for sandIngre in sandwichIngredientes:
                    TaSandwich = Sandwich.objects.filter(id = sandIngre.fk_sandwich_id).first()
                    ingrediente = Ingrediente_adicional.objects.filter(id = sandIngre.fk_ingrediente_id)

                    for i in ingrediente:
                        ingredientes.append(i.nombre)                      
                    
                    if bandera==True:                        
                        result.append({
                            'id': pedido.id,
                            'customer': cliente.nombre + " " + cliente.apellido,
                            'size': TaSandwich.tamaño, 
                            'ingredients': ingredientes,
                            'total': sandIngre.subtotal, 
                            'date': pedido.fecha 
                        })  
                        bandera=False  
        
        # Transformamos el array de ingredientes a String
        resultFixed = []
        for item in result:
            item['ingredients'] = PedidoApiView.listToString(item['ingredients'])
            resultFixed.append(item)   
                     
        return resultFixed      

    def get(self, request, *args, **kwargs):
        Reporte = []
        reporteGeneral = self.getGeneral()
        reporteDay = self.getByDay()
        reporteSize = self.getBySize()
        reporteIngredientes = self.getByIngredients()
        reporteClientes = self.getByClients()

        serializer = ReporteSerializer(reporteGeneral, many=True)
        serilizerDay = ReporteSerializer(reporteDay, many=True)
        serilizerSize = ReporteSerializer(reporteSize, many=True)
        serializerIngredientes = ReporteIngredienteSerializer(reporteIngredientes, many=True)
        serializerClientes = ReporteSerializer(reporteClientes, many=True)
        
        Reporte.append({
            "General" : serializer.data,
            "Day": serilizerDay.data,
            "Size": serilizerSize.data,
            "Ingredients": serializerIngredientes.data,
            "Clients": serializerClientes.data,
        })   

        return Response(Reporte)
       