
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import *

router = routers.DefaultRouter()

# Component
class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = ('id', 'component_type_id', 'connection_type_id', 'orientation', 'weight', 'outside_shape', 'base_type', 'height_over_tube', 'bolt_pattern_long',
                  'bolt_pattern_wide', 'groove', 'base_diameter', 'shoulder_diameter', 'unique_feature',  
                   )

        def component_type_id(self, obj):
            try:
                result = obj.component_type.id
            except: 
                result = None
            return result
        
        def connection_type_id(self, obj):
            try:
                result = obj.connection_type.id
            except: 
                result = None
            return result
        


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer    

router.register(r'component', ComponentViewSet)

# ComponentType
class ComponentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentType
        fields = ('id', )


class ComponentTypeViewSet(viewsets.ModelViewSet):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer    

router.register(r'component_type', ComponentTypeViewSet)


# ConnectionType
class ConnectionTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConnectionType
        fields = ('id', 'connection_type', )


class ConnectionTypeViewSet(viewsets.ModelViewSet):
    queryset = ConnectionType.objects.all()
    serializer_class = ConnectionTypeSerializer    

router.register(r'connection_type', ConnectionTypeViewSet)


# PriceQuoteSupplier
class PriceQuoteSupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PriceQuoteSupplier
        fields = ('id', 'supplier_id', 'price_quote_id', 'quantity', 'cost', 'min_order_quantity', )

        def supplier_id(self, obj):
            try:
                result = obj.supplier.id
            except: 
                result = None
            return result
        
        def price_quote_id(self, obj):
            try:
                result = obj.price_quote.id
            except: 
                result = None
            return result
        

class PriceQuoteSupplierViewSet(viewsets.ModelViewSet):
    queryset = PriceQuoteSupplier.objects.all()
    serializer_class = PriceQuoteSupplierSerializer    

router.register(r'price_quote_supplier', PriceQuoteSupplierViewSet)

# PriceQuote
class PriceQuoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PriceQuote
        fields = ('id', 'tube_assembly_id', 'quote_date', 'annual_usage', 'bracket_pricing',  )

        def tube_assembly_id(self, obj):
            try:
                result = obj.tube_assembly.id
            except: 
                result = None
            return result


class PriceQuoteViewSet(viewsets.ModelViewSet):
    queryset = PriceQuote.objects.all()
    serializer_class = PriceQuoteSerializer    

router.register(r'price_quote', PriceQuoteViewSet)


# Supplier
class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', )

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer    

router.register(r'supplier', SupplierViewSet)

# TubeAssemblyComponent
class TubeAssemblyComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TubeAssemblyComponent
        fields = ('id', 'tube_assembly_id', 'component_id', 'quantity', )
        
        def tube_assembly_id(self, obj):
            try:
                result = obj.tube_assembly.id
            except: 
                result = None
            return result

        def component_id(self, obj):
            try:
                result = obj.component.id
            except: 
                result = None
            return result
        

class TubeAssemblyComponentViewSet(viewsets.ModelViewSet):
    queryset = TubeAssemblyComponent.objects.all()
    serializer_class = TubeAssemblyComponentSerializer    

router.register(r'tube_assembly_component', TubeAssemblyComponentViewSet)

# TubeAssembly
class TubeAssemblySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TubeAssembly
        fields = ('id', )


class TubeAssemblyViewSet(viewsets.ModelViewSet):
    queryset = TubeAssembly.objects.all()
    serializer_class = TubeAssemblySerializer    

router.register(r'tube_assembly', TubeAssemblyViewSet)


urlpatterns = [ 
    url(r'^', include(router.urls)),
]    
