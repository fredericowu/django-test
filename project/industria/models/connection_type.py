from django.db import models

class ConnectionType(models.Model):
    # type -> palavra reservada
    connection_type = models.CharField(blank=True, null=True, default=None, max_length=45 )

    def __str__(self):
        return str(self.pk) if self.pk else 'Novo'