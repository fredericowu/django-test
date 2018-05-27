from django.db import models

class ComponentType(models.Model):
    # ilustrar CRUD
    component_type_name = models.CharField(blank=True, null=True, default=None, max_length=45 )

    def __str__(self):
        return str(self.pk) if self.pk else 'Novo'