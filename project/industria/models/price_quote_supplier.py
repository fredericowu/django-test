from django.db import models
from .tube_assembly import TubeAssembly
from .supplier import Supplier

class PriceQuoteSupplier(models.Model):    
    supplier    = models.ForeignKey( 'Supplier', on_delete=models.CASCADE )
    price_quote = models.ForeignKey( 'PriceQuote', on_delete=models.CASCADE )
    
    quantity    = models.IntegerField(default = 1)
    cost        = models.DecimalField(max_digits = 30, decimal_places=20)
    min_order_quantity   = models.IntegerField( default = 1 )
   
    def __str__(self):
        return str(self.pk) if self.pk else 'Novo'   

