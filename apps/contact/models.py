from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    address = models.TextField(blank=True, null=True, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

