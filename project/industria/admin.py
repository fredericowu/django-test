from django.contrib import admin
from .models import *


class TubeAssemblyAdmin(admin.ModelAdmin):
    list_display = ('id', )    
    search_fields = ('id', )


class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'component_type_name', )    
    search_fields = list_display


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'orientation', 'weight', 'outside_shape', 'base_type', 'height_over_tube',  
                    'bolt_pattern_long', 'bolt_pattern_wide', 'groove', 'base_diameter', 'shoulder_diameter', 'unique_feature', 
                     )    
    search_fields = list_display
    
    
class ConnectionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'connection_type', )    
    search_fields = list_display
    
class PriceQuoteSupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier_id', 'tube_assembly_id', 'quantity', 'cost', 'min_order_quantity' )    
    search_fields = ('id', 'supplier__id', 'price_quote__tube_assembly__id', 'quantity', 'cost', 'min_order_quantity' )
    
    
    def supplier_id(self, obj):         
        try:
            result = str( obj.supplier.id )
        except:
            result = ""
        
        return result
      

    def tube_assembly_id(self, obj):
        try:
            result = str( obj.price_quote.tube_assembly.pk )
        except:
            result = ""
            
        return result
    

class PriceQuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'tube_assembly_id', 'quote_date', 'annual_usage', 'bracket_pricing' )    
    search_fields = ('id', 'tube_assembly__id', 'quote_date', 'annual_usage', )
    
    def tube_assembly_id(self, obj):
        try:
            result = str( obj.tube_assembly.pk )
        except:
            result = ""
            
        return result
    

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id',  )    
    search_fields = list_display
    

class TubeAssemblyComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tube_assembly_id', 'component_id', 'quantity', )    
    search_fields = ('id', 'tube_assembly__id', 'component__id', 'quantity', )
    
    def tube_assembly_id(self, obj):
        try:
            result = str( obj.tube_assembly.pk )
        except:
            result = ""
            
        return result

    def component_id(self, obj):
        try:
            result = str( obj.component.pk )
        except:
            result = ""
            
        return result
    
    
    

admin.site.register(TubeAssembly, TubeAssemblyAdmin)
admin.site.register(ComponentType, ComponentTypeAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(ConnectionType, ConnectionTypeAdmin)
admin.site.register(PriceQuoteSupplier, PriceQuoteSupplierAdmin)
admin.site.register(PriceQuote, PriceQuoteAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(TubeAssemblyComponent, TubeAssemblyComponentAdmin)



