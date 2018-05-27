import csv
from .models import *
import datetime
from decimal import Decimal

class Importador():
    bill_of_materials   = None
    comp_boss           = None
    price_quote         = None    

    price_quote_header          = [ "tube_assembly_id", "supplier", "quote_date", "annual_usage", "min_order_quantity", "bracket_pricing", "quantity", "cost" ]
    comp_boss_header            = [ "component_id", "component_type_id", "type", "connection_type_id", "outside_shape", "base_type", "height_over_tube", "bolt_pattern_long", "bolt_pattern_wide", "groove", "base_diameter", "shoulder_diameter", "unique_feature", "orientation", "weight" ]
    bill_of_materials_header    = [ "tube_assembly_id", "component_id_1", "quantity_1", "component_id_2", "quantity_2", "component_id_3", "quantity_3", "component_id_4", "quantity_4", "component_id_5", "quantity_5", "component_id_6", "quantity_6", "component_id_7", "quantity_7", "component_id_8", "quantity_8" ]

    def __init__(self, bill_of_materials, price_quote, comp_boss):
        self.bill_of_materials 	= bill_of_materials
        self.comp_boss 		= comp_boss
        self.price_quote 	= price_quote
        
    def format_decimal(self, num ):
        return num.to_integral() if num == num.to_integral() else num.normalize()
    
    def none_to_na(self, txt ):
        return 'NA' if txt is None else txt 

    def limpar_base(self):
        # price_quote
        Supplier.objects.all().delete()
        TubeAssembly.objects.all().delete()
        PriceQuote.objects.all().delete()
        PriceQuoteSupplier.objects.all().delete()
        
        # comp_boss
        Component.objects.all().delete()
        ConnectionType.objects.all().delete()
        ComponentType.objects.all().delete()
     
        # bill_of_materials
        TubeAssemblyComponent.objects.all().delete()
        
    
    def exportar_bill_of_materials(self):
        csv_file = self.bill_of_materials        
        header = self.bill_of_materials_header
        objs = TubeAssemblyComponent.objects.all().select_related().order_by("tube_assembly__pk")
                
        sw = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')        
        sw.writerow( header )
        
        ok = []
        def to_row(tubeassembly, components):
            #print(len(components))
            row = []
            
            # definindo linha
            row.append( "TA-{0:0>5}".format( tubeassembly.id ) )
            for item in components:
                if item[0]:
                    row.append( "C-{0:0>4}".format( item[0].id ) if item[0].id != 9999 else '9999' )
                else:
                    row.append( 'NA' )
                    
                row.append( item[1] if item[1] else 'NA' )
                    
                
            for i in range(0, 8-len(components) ):
                row.append( 'NA' )
                row.append( 'NA' )
            
            ok.append( tubeassembly.id )
            return row

        

        last_tubeassembly = None
        components = []
        for obj in objs:
            #row = []            
            if last_tubeassembly is None:
                last_tubeassembly = obj.tube_assembly

            if last_tubeassembly != obj.tube_assembly:
                sw.writerow( to_row( last_tubeassembly, components ) )
                components = []
                
            components.append( [ obj.component, obj.quantity ] )
            
            last_tubeassembly = obj.tube_assembly

        if last_tubeassembly:
            sw.writerow( to_row( last_tubeassembly, components ) )
        
        
        nok_objs = TubeAssembly.objects.all().exclude( id__in = ok )
        for obj in nok_objs:
            sw.writerow( to_row( obj, [] ) )
                     
                
        csv_file.close()
            
    def exportar_price_quote(self):
        csv_file = self.price_quote        
        header = self.price_quote_header
        objs = PriceQuoteSupplier.objects.all().select_related()
                
        sw = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')        
        sw.writerow( header )
        for obj in objs:
            row = []
            
            # definindo linha
            row.append( "TA-{0:0>5}".format( obj.price_quote.tube_assembly.id ) )
            row.append( "S-{0:0>4}".format( obj.supplier.id ) )
            row.append( obj.price_quote.quote_date.strftime("%Y-%m-%d") )
            row.append( obj.price_quote.annual_usage )
            row.append( obj.min_order_quantity )
            row.append( "Yes" if obj.price_quote.bracket_pricing else "No" )
            row.append( obj.quantity )
            row.append( obj.cost.to_integral() if obj.cost == obj.cost.to_integral() else obj.cost.normalize() )

            sw.writerow( row )
        
        
        csv_file.close()
        
    
    def exportar_comp_boss(self):
        csv_file = self.comp_boss        
        header = self.comp_boss_header
        objs = Component.objects.filter( component_type__isnull = False ).select_related()
                
        sw = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')        
        sw.writerow( header )
        for obj in objs:
            row = []
            
            # definindo linha
            row.append( "C-{0:0>4}".format( obj.id ) )
            row.append( "CP-{0:0>3}".format( obj.component_type.id ) )
            row.append( "Boss" if obj.unique_feature else ( self.none_to_na( obj.connection_type.connection_type ) if obj.connection_type else 'NA' ) )
            row.append( "B-{0:0>3}".format( obj.connection_type.id ) if obj.connection_type else '9999' )
            row.append( self.none_to_na( obj.outside_shape ) )
            row.append( self.none_to_na( obj.base_type ) )
            row.append( self.format_decimal( obj.height_over_tube )  if obj.height_over_tube else 'NA' )
            row.append( self.format_decimal( obj.bolt_pattern_long )  if obj.bolt_pattern_long else 'NA' )
            row.append( self.format_decimal( obj.bolt_pattern_wide )  if obj.bolt_pattern_wide else 'NA' )
            row.append( "Yes" if obj.groove else "No" )
            row.append( self.format_decimal( obj.base_diameter )  if obj.base_diameter else 'NA' )
            row.append( self.format_decimal( obj.shoulder_diameter )  if obj.shoulder_diameter else 'NA' )
            row.append( "Yes" if obj.unique_feature else "No" )
            row.append( "Yes" if obj.orientation else "No" )
            row.append( self.format_decimal( obj.weight )  if obj.weight else 'NA' )

            sw.writerow( row )
        
        
        csv_file.close()
        

    def importar_bill_of_materials(self):
        csv_file = self.bill_of_materials

        header = None
        sr = csv.reader( csv_file, delimiter=',' )
        for row in sr:
            #print(row)
            if not header:
                header = row
                continue

            tube_assembly_id    = row[0]
            component_id_1      = row[1]
            quantity_1          = row[2]
            component_id_2      = row[3]
            quantity_2          = row[4]
            component_id_3      = row[5]
            quantity_3          = row[6]
            component_id_4      = row[7]
            quantity_4          = row[8]
            component_id_5      = row[9]
            quantity_5          = row[10]
            component_id_6      = row[11]
            quantity_6          = row[12]
            component_id_7      = row[13]
            quantity_7          = row[14]
            component_id_8      = row[15]
            quantity_8          = row[16]
            
            # formatando
            tube_assembly_id    = int(tube_assembly_id.replace("TA-", ""))
            component_id_1      = int(component_id_1.replace("C-", "")) if component_id_1 != 'NA' else None
            quantity_1          = int(quantity_1) if quantity_1 != 'NA' else None
            component_id_2      = int(component_id_2.replace("C-", "")) if component_id_2 != 'NA' else None
            quantity_2          = int(quantity_2) if quantity_2 != 'NA' else None
            component_id_3      = int(component_id_3.replace("C-", "")) if component_id_3 != 'NA' else None
            quantity_3          = int(quantity_3) if quantity_3 != 'NA' else None
            component_id_4      = int(component_id_4.replace("C-", "")) if component_id_4 != 'NA' else None
            quantity_4          = int(quantity_4) if quantity_4 != 'NA' else None
            component_id_5      = int(component_id_5.replace("C-", "")) if component_id_5 != 'NA' else None
            quantity_5          = int(quantity_5) if quantity_5 != 'NA' else None
            component_id_6      = int(component_id_6.replace("C-", "")) if component_id_6 != 'NA' else None
            quantity_6          = int(quantity_6) if quantity_6 != 'NA' else None
            component_id_7      = int(component_id_7.replace("C-", "")) if component_id_7 != 'NA' else None
            quantity_7          = int(quantity_7) if quantity_7 != 'NA' else None
            component_id_8      = int(component_id_8.replace("C-", "")) if component_id_8 != 'NA' else None
            quantity_8          = int(quantity_8) if quantity_8 != 'NA' else None


            # criando ojetos em banco
            tube_assembly_obj = TubeAssembly.objects.get_or_create( id = tube_assembly_id )[0]
            
            component_id_1_obj = Component.objects.get_or_create( id = component_id_1 )[0] if component_id_1 else None
            if quantity_1:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_1_obj, quantity = quantity_1 )                            
            component_id_2_obj = Component.objects.get_or_create( id = component_id_2 )[0] if component_id_2 else None
            if quantity_2:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_2_obj, quantity = quantity_2 )
            component_id_3_obj = Component.objects.get_or_create( id = component_id_3 )[0] if component_id_3 else None
            if quantity_3:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_3_obj, quantity = quantity_3 )
            component_id_4_obj = Component.objects.get_or_create( id = component_id_4 )[0] if component_id_4 else None
            if quantity_4:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_4_obj, quantity = quantity_4 )
            component_id_5_obj = Component.objects.get_or_create( id = component_id_5 )[0] if component_id_5 else None
            if quantity_5:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_5_obj, quantity = quantity_5 )
            component_id_6_obj = Component.objects.get_or_create( id = component_id_6 )[0] if component_id_6 else None
            if quantity_6:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_6_obj, quantity = quantity_6 )
            component_id_7_obj = Component.objects.get_or_create( id = component_id_7 )[0] if component_id_7 else None
            if quantity_7:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_7_obj, quantity = quantity_7 )
            component_id_8_obj = Component.objects.get_or_create( id = component_id_8 )[0] if component_id_8 else None
            if quantity_8:                
                TubeAssemblyComponent.objects.create( tube_assembly = tube_assembly_obj, component = component_id_8_obj, quantity = quantity_8 )
                
            
    def importar_price_quote(self):
        csv_file = self.price_quote

        header = None
        sr = csv.reader( csv_file, delimiter=',' )
        for row in sr:
            #print(row)
            if not header:
                header = row
                continue

            tube_assembly      = row[0]
            supplier           = row[1]
            quote_date         = row[2]
            annual_usage       = row[3]
            min_order_quantity = row[4]
            bracket_pricing    = row[5]
            quantity           = row[6]
            cost               = row[7]
            
            # formatando
            quote_date         = datetime.datetime.strptime(quote_date,"%Y-%m-%d").date()
            supplier           = int(supplier.replace("S-", ""))
            tube_assembly      = int(tube_assembly.replace("TA-", ""))
            bracket_pricing    = True if bracket_pricing == "Yes" else False
            annual_usage       = int(annual_usage)
            min_order_quantity = int(min_order_quantity)
            quantity           = int(quantity)            
            cost               = Decimal(cost) 

            # criando ojetos em banco
            supplier_obj         = Supplier.objects.get_or_create( id  = supplier )[0]
            tube_assembly_obj    = TubeAssembly.objects.get_or_create( id = tube_assembly )[0]             
            price_quote_obj      = PriceQuote.objects.get_or_create( quote_date = quote_date, tube_assembly = tube_assembly_obj, annual_usage = annual_usage, bracket_pricing = bracket_pricing )[0]            
            price_quote_supplier = PriceQuoteSupplier.objects.create( price_quote = price_quote_obj, supplier = supplier_obj, quantity = quantity, cost = cost, min_order_quantity = min_order_quantity )            
            

    def importar_comp_boss(self):
        csv_file = self.comp_boss

        header = None
        sr = csv.reader( csv_file, delimiter=',' )
        for row in sr:
            #print(row)
            if not header:
                header = row
                continue

            component_id        = row[0]
            component_type_id   = row[1]
            connection_type     = row[2]
            connection_type_id  = row[3]
            outside_shape       = row[4]
            base_type           = row[5]
            height_over_tube    = row[6]
            bolt_pattern_long   = row[7]
            bolt_pattern_wide   = row[8]
            groove              = row[9]
            base_diameter       = row[10]
            shoulder_diameter   = row[11]
            unique_feature      = row[12]
            orientation         = row[13]
            weight              = row[14]
                        
            # formatando
            component_id        = int(component_id.replace("C-", ""))
            component_type_id   = int(component_type_id.replace("CP-", ""))
            connection_type     = None if connection_type == 'NA' else connection_type
            connection_type_id  = None if connection_type_id == '9999' else int(connection_type_id.replace("B-", ""))
            outside_shape       = None if outside_shape == 'NA' else outside_shape
            base_type           = None if base_type == 'NA' else base_type
            bolt_pattern_long   = None if bolt_pattern_long == 'NA' else bolt_pattern_long
            bolt_pattern_wide   = None if bolt_pattern_wide == 'NA' else bolt_pattern_wide
            groove              = True if groove == 'Yes' else False
            base_diameter       = None if base_diameter == 'NA' else base_diameter
            shoulder_diameter   = None if shoulder_diameter == 'NA' else shoulder_diameter
            unique_feature      = True if unique_feature == 'Yes' else False
            orientation         = True if orientation == 'Yes' else False
            weight              = None if weight == 'NA' else weight                        
            # deixando importar height_over_tube = 9999
            #height_over_tube    = None if height_over_tube == '9999' else height_over_tube

            # criando ojetos em banco
            component_type_obj  = ComponentType.objects.get_or_create( id = component_type_id )[0]
            connection_type_obj = ConnectionType.objects.get_or_create( id = connection_type_id )[0] if connection_type_id else None
            if not unique_feature and connection_type_obj:
                connection_type_obj.connection_type = connection_type
                connection_type_obj.save()
                        
            component_obj       = Component.objects.get_or_create(
                                                                    id = component_id,
                                                                    connection_type   = connection_type_obj,
                                                                    component_type    = component_type_obj,
                                                                    orientation       = orientation,
                                                                    weight            = weight,
                                                                    outside_shape     = outside_shape,
                                                                    base_type         = base_type,
                                                                    height_over_tube  = height_over_tube,
                                                                    bolt_pattern_long = bolt_pattern_long,
                                                                    bolt_pattern_wide = bolt_pattern_wide,
                                                                    groove            = groove,
                                                                    base_diameter     = base_diameter,
                                                                    shoulder_diameter = shoulder_diameter,
                                                                    unique_feature    = unique_feature,
                                                                     
                                                                    )[0]
                    
        
    def exportar(self):
        result = True
        try:
            self.exportar_price_quote()
            self.exportar_comp_boss()
            self.exportar_bill_of_materials()            
        except:
            result = False
            print("Falha na exportacao")
            raise
                    
        return result
    
        
    def importar(self):
        result = True
        try:
            self.importar_price_quote()
            self.importar_comp_boss()
            self.importar_bill_of_materials()            
        except:
            result = False
            print("Falha na importacao")
            raise
                    
        return result
    
    
     

