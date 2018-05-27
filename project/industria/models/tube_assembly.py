from django.db import models

class TubeAssembly(models.Model):

    def __str__(self):
        return str(self.pk) if self.pk else 'Novo'   
