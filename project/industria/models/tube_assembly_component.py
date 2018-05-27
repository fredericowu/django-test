from django.db import models
from .tube_assembly import TubeAssembly
from .component import Component

class TubeAssemblyComponent(models.Model):
    tube_assembly   = models.ForeignKey('TubeAssembly', on_delete=models.CASCADE)
    # quando nulo -> 9999
    component       = models.ForeignKey('Component', on_delete=models.SET_NULL, null=True, default=None, blank = True) 
    quantity        = models.IntegerField(null=True, default=None, blank = True)
    
    def __str__(self):
        return str(self.pk) if self.pk else 'Novo'    


