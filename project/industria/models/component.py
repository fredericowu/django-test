from django.db import models

class Component(models.Model):
    # quando nulo -> 9999
    connection_type   = models.ForeignKey('ConnectionType', on_delete = models.SET_NULL, null=True, default=None, blank = True )

    # para importar o bill_of_materials precisa aceitar nulo
    component_type    = models.ForeignKey('ComponentType', on_delete = models.SET_NULL, null=True, default=None, blank = True)

    orientation       = models.BooleanField( default=True )
    weight            = models.DecimalField( null=True, default=None, blank = True, max_digits = 4, decimal_places=3 )
    outside_shape     = models.CharField( blank=True, null=True, default=None, max_length=45 )
    base_type         = models.CharField( blank=True, null=True, default=None, max_length=45 )
    height_over_tube  = models.DecimalField( null=True, default=None, blank = True, max_digits = 6, decimal_places=2 )
    bolt_pattern_long = models.DecimalField( null=True, default=None, blank = True, max_digits = 5, decimal_places=2 )    
    bolt_pattern_wide = models.DecimalField( null=True, default=None, blank = True, max_digits = 5, decimal_places=2 )
    groove            = models.BooleanField( default=False )
    base_diameter     = models.DecimalField( null=True, default=None, blank = True, max_digits = 4, decimal_places=2 )
    shoulder_diameter = models.DecimalField( null=True, default=None, blank = True, max_digits = 4, decimal_places=2 )
    unique_feature    = models.BooleanField( default=False )
     
 
    def __str__(self):
        return str(self.pk) if self.pk else 'Novo'   
