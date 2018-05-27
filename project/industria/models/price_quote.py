from django.db import models
from .tube_assembly import TubeAssembly
from .supplier import Supplier
from .price_quote_supplier import PriceQuoteSupplier

class PriceQuote(models.Model):    
    tube_assembly   = models.ForeignKey('TubeAssembly', on_delete=models.CASCADE)
    quote_date      = models.DateField()
    annual_usage    = models.IntegerField(null=True, default=None, blank = True)
    bracket_pricing = models.BooleanField(default=False )
    
    price_quote_supplier = models.ManyToManyField('Supplier', through = 'PriceQuoteSupplier')
    
    def __str__(self):
        return str(self.pk) if self.pk else 'Novo'   
    


