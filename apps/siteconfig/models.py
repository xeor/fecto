from django.db import models
from django.utils.translation import ugettext_lazy as _

class Site(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    value = models.TextField(default='')

class Text(models.Model):
    app = models.CharField(default='', max_length=255, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(default='')
    value = models.TextField(default='', db_index=True, null=True, blank=True)
    default = models.TextField(default='')
    varType = models.CharField(max_length=64, default='text')
    permission = models.CharField(default='', max_length=255, db_index=True, null=True, blank=True)

    def is_default(self):
        if self.value == self.default:
            return True
        else:
            return False
    is_default.boolean = True

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.app)
